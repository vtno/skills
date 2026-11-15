"""Run with: python3 -m unittest discover -s tests -v

Requires numpy and ffmpeg/libass. Uses only synthetic local media; no model/API calls.
"""
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

SCRIPTS = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(SCRIPTS))
from common import load_json, probe, save_json
from video_format import dimensions, output_size, profile_settings, valid_fps


class FormatTests(unittest.TestCase):
    def test_dimensions_fallback_and_override(self):
        self.assertEqual(dimensions({}, {'W': 1920, 'H': 1080}), (1920, 1080))
        self.assertEqual(dimensions({'W': 1280, 'H': 720}, {'W': 1920, 'H': 1080}), (1280, 720))
        self.assertEqual(dimensions({}), (1080, 1920))

    def test_bad_dimensions(self):
        for value in (0, -2, 1919, 1080.0, True, '1920'):
            with self.assertRaises(ValueError):
                dimensions({'W': value, 'H': 1080})

    def test_output_formats(self):
        self.assertEqual(output_size('16:9', 320, 180), (1920, 1080))
        self.assertEqual(output_size('9:16', 320, 180), (1080, 1920))
        self.assertEqual(output_size('1:1', 320, 180), (1080, 1080))
        self.assertEqual(output_size('source', 321, 181), (320, 180))
        self.assertEqual(output_size('16:9', 320, 180, 1280, 720), (1280, 720))
        with self.assertRaises(ValueError):
            output_size('16:9', 320, 180, 1280)

    def test_profiles(self):
        self.assertIsNone(profile_settings('video', 1920, 1080)['halftone'])
        self.assertEqual(profile_settings('reel', 1080, 1920)['grain'], 4)
        self.assertFalse(valid_fps(float('nan')))
        self.assertFalse(valid_fps(0))
        self.assertTrue(valid_fps(29.97))


@unittest.skipUnless(shutil.which('ffmpeg'), 'ffmpeg required')
class PipelineTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory(prefix='video_editing_test_',
                                             dir='/tmp/opencode' if Path('/tmp/opencode').is_dir() else None)
        cls.root = Path(cls.tmp.name)
        cls.source = cls.root / 'source.mp4'
        subprocess.run(['ffmpeg', '-v', 'error', '-y', '-f', 'lavfi', '-i',
                        'testsrc2=size=320x180:rate=6:duration=3', '-f', 'lavfi', '-i',
                        'sine=frequency=440:sample_rate=48000:duration=3', '-c:v', 'libx264',
                        '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-shortest', str(cls.source)], check=True)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def command(self, script, *args, ok=True):
        p = subprocess.run([sys.executable, str(SCRIPTS / script), *map(str, args)], capture_output=True, text=True)
        if ok:
            self.assertEqual(p.returncode, 0, p.stdout + p.stderr)
        else:
            self.assertNotEqual(p.returncode, 0, p.stdout + p.stderr)
        return p

    def project(self, name, w=320, h=180, profile='video'):
        P = self.root / name
        self.command('prepare_project.py', self.source, '--project', P, '--profile', profile,
                     '--width', w, '--height', h)
        self.command('prepare_timeline.py', P)
        self.command('init_edl.py', P)
        return P

    def test_preserved_timeline_and_no_overwrite(self):
        P = self.project('preserved')
        self.assertEqual(load_json(P / 'analysis/cuts.json'), [dict(src_t0=0.0, src_t1=3.0, prog_t0=0.0)])
        self.assertEqual((P / 'audio/program_raw.wav').read_bytes(), (P / 'audio/source_48k.wav').read_bytes())
        self.command('prepare_project.py', self.source, '--project', P, ok=False)
        self.command('prepare_timeline.py', P, ok=False)
        self.command('init_edl.py', P, ok=False)

    def test_planner_uses_project_geometry(self):
        from reel_plan import build_plan
        P = self.project('fallback', 1920, 1080)
        edl = load_json(P / 'edl.json')
        del edl['W'], edl['H']
        save_json(edl, P / 'edl.json')
        plan = build_plan(str(P / 'edl.json'))
        self.assertEqual((plan['W'], plan['H']), (1920, 1080))
        self.assertEqual(plan['pieces'][0]['s0'], plan['pieces'][0]['s1'])
        self.assertIsNone(plan['look']['halftone'])
        edl['inserts'] = [dict(id='neutral', kind='full', t0=0, t1=1,
                               clips=[dict(src=str(self.source))])]
        save_json(edl, P / 'edl.json')
        neutral = build_plan(str(P / 'edl.json'))['inserts'][0]
        self.assertEqual(neutral['trans'], 'cut')
        self.assertTrue(neutral['clips'][0]['color'])
        self.assertEqual(neutral['clips'][0]['zoom'], [1, 1])
        result = self.command('validate_edl.py', P / 'edl.json')
        self.assertIn('0 error(s)', result.stdout)
        edl['W'] = 1919
        save_json(edl, P / 'edl.json')
        self.command('validate_edl.py', P / 'edl.json', ok=False)

    def test_reel_legacy_defaults(self):
        from reel_plan import build_plan
        P = self.project('legacy', 1080, 1920, 'reel')
        edl = load_json(P / 'edl.json')
        del edl['profile']
        save_json(edl, P / 'edl.json')
        cfg = load_json(P / 'project.json')
        del cfg['profile']
        save_json(cfg, P / 'project.json')
        plan = build_plan(str(P / 'edl.json'))
        self.assertAlmostEqual(plan['pieces'][0]['s1'] / plan['pieces'][0]['s0'], 1.03)
        self.assertEqual(plan['look']['grain'], 4)

    def test_three_formats_render_text_inserts_and_previews(self):
        for label, w, h in (('landscape', 320, 180), ('portrait', 180, 320), ('square', 240, 240)):
            with self.subTest(format=label):
                P = self.project(label, w, h)
                edl = load_json(P / 'edl.json')
                edl['inserts'] = [
                    dict(id='full', kind='full', t0=0, t1=0.8, trans='cut', clips=[dict(src=str(self.source), color=True)]),
                    dict(id='split', kind='full', layout='split', t0=0.8, t1=1.8,
                         clips=[dict(src=str(self.source), color=True)]),
                    dict(id='bar', kind='bar', t0=1.8, t1=3, trans='cut', label='TEST'),
                ]
                edl['text'] = [dict(font='sub', text='TEST', t0=0, t1=0.6, x=w/2, y=h*0.8,
                                    size=20, anim='pop', keep_t1=True)]
                save_json(edl, P / 'edl.json')
                self.command('validate_edl.py', P / 'edl.json')
                self.command('render_video.py', P / 'edl.json', '--stills', 0.5, 1.5, 2.5,
                             '--out-dir', P / 'qa/stills', '--workers', 1)
                stills = list((P / 'qa/stills').glob('*.png'))
                self.assertEqual(len(stills), 3)
                for still in stills:
                    info = probe(str(still))
                    self.assertEqual((info['w'], info['h']), (w, h))
                sheet = probe(str(P / 'qa/stills/sheet.jpg'))
                self.assertAlmostEqual(sheet['w'] / sheet['h'] / 3, w / h, delta=0.02)
                out = P / 'render/v1.mp4'
                self.command('render_video.py', P / 'edl.json', '--out', out, '--workers', 1)
                info = probe(str(out))
                self.assertEqual((info['w'], info['h']), (w, h))
                self.assertAlmostEqual(info['dur'], 3, delta=0.2)
                self.assertTrue(info['audio'])
                subprocess.run(['ffmpeg', '-v', 'error', '-i', str(out), '-f', 'null', '-'], check=True)
                self.command('render_video.py', P / 'edl.json', '--out', out, '--workers', 1, ok=False)


if __name__ == '__main__':
    unittest.main()
