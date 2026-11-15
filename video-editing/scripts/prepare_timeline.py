#!/usr/bin/env python3
"""Keep an already-edited source intact; create the identity source-to-program map.

    python3 scripts/prepare_timeline.py PROJECT

Run transcribe.py first if word timing is wanted. Unlike cut_pauses.py this never
shortens pauses, trims the ends, fades the audio, or changes take order.
"""
import argparse
import os
import shutil

from common import load_json, project_config, save_json


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('project')
    a = ap.parse_args()
    cfg = project_config(a.project)
    P = cfg['project_dir']
    cuts_path = os.path.join(P, 'analysis', 'cuts.json')
    if os.path.exists(cuts_path):
        ap.error('cuts.json already exists; preserve the previous project before rebuilding its timeline')
    duration = cfg['src_dur']
    if duration <= 0:
        ap.error('source duration must be positive')
    save_json([dict(src_t0=0.0, src_t1=duration, prog_t0=0.0)], cuts_path)
    asr = os.path.join(P, 'analysis', 'asr.json')
    words = [w for s in load_json(asr) for w in s['words']] if os.path.exists(asr) else []
    save_json(words, os.path.join(P, 'analysis', 'program_words.json'))
    shutil.copyfile(os.path.join(P, 'audio', 'source_48k.wav'), os.path.join(P, 'audio', 'program_raw.wav'))
    cfg.update(program_dur=duration, timeline_mode='preserve')
    save_json(cfg, os.path.join(P, 'project.json'))
    print('Preserved source timeline: %.3f s, %d words. No speech or pauses removed.' % (duration, len(words)))


if __name__ == '__main__':
    main()
