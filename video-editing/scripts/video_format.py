"""Output geometry and preset defaults shared by setup, planning and validation."""
import math

FORMATS = {'9:16': (1080, 1920), '16:9': (1920, 1080), '1:1': (1080, 1080)}


def dimensions(edl, cfg=None):
    cfg = cfg or {}
    w, h = edl.get('W', cfg.get('W', 1080)), edl.get('H', cfg.get('H', 1920))
    if any(isinstance(v, bool) or not isinstance(v, int) or v < 2 or v % 2 for v in (w, h)):
        raise ValueError('W and H must be positive even integers (H.264 yuv420p)')
    return w, h


def output_size(format_name, source_w, source_h, width=None, height=None):
    if (width is None) != (height is None):
        raise ValueError('--width and --height must be provided together')
    if width is not None:
        return dimensions({'W': width, 'H': height})
    if format_name == 'source':
        return dimensions({'W': source_w - source_w % 2, 'H': source_h - source_h % 2})
    return FORMATS[format_name]


def profile_settings(profile, w, h):
    if profile == 'reel':
        return dict(halftone='assets/halftone_1080x1920.png', halftone_opacity=24, vignette=42, grain=4)
    return dict(halftone=None, halftone_opacity=0, vignette=0, grain=0)


def valid_fps(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value) and value > 0
