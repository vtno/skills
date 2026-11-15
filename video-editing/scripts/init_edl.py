#!/usr/bin/env python3
"""Create a dimension-aware starter EDL without overwriting an existing edit."""
import argparse
import os

from common import project_config, save_json
from textass import default_fonts
from video_format import dimensions, profile_settings


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('project')
    a = ap.parse_args()
    cfg = project_config(a.project)
    P = cfg['project_dir']
    path = os.path.join(P, 'edl.json')
    if os.path.exists(path):
        ap.error('edl.json already exists; edit or version the existing EDL instead')
    w, h = dimensions({}, cfg)
    profile = cfg.get('profile', 'reel')
    audio = cfg.get('audio') or 'audio/program_raw.wav'
    edl = dict(name=cfg['name'], W=w, H=h, fps=cfg['fps'], profile=profile,
               audio=audio, presenter={}, inserts=[], text=[], logos={},
               fonts=default_fonts(), look=profile_settings(profile, w, h))
    save_json(edl, path)
    print('Starter EDL: %s (%dx%d, %s)' % (path, w, h, profile))


if __name__ == '__main__':
    main()
