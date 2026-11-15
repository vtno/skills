"""Shared explicit encoding policy; NVENC availability requires a real encode."""
import subprocess


def nvenc_available(ffmpeg):
    try:
        result = subprocess.run([
            ffmpeg, '-v', 'error', '-f', 'lavfi', '-i',
            'testsrc2=size=320x180:rate=30', '-frames:v', '3', '-an',
            '-c:v', 'h264_nvenc', '-preset', 'p5', '-pix_fmt', 'yuv420p',
            '-f', 'null', '-'], capture_output=True, timeout=20)
        return result.returncode == 0, result.stderr.decode(errors='replace').strip()
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, str(exc)


def select_encoder(ffmpeg, requested):
    if requested == 'libx264':
        return requested
    if requested not in ('auto', 'h264_nvenc'):
        raise ValueError('Unknown encoder: ' + requested)
    ok, reason = nvenc_available(ffmpeg)
    if ok:
        return 'h264_nvenc'
    if requested == 'h264_nvenc':
        raise RuntimeError('NVENC smoke test failed: ' + reason)
    print('NVENC unavailable; auto falling back to libx264: ' + reason, flush=True)
    return 'libx264'


def encoder_args(encoder, cq=18):
    if encoder == 'h264_nvenc':
        return ['-c:v', encoder, '-preset', 'p5', '-tune', 'hq',
                '-rc', 'vbr', '-cq', str(cq), '-b:v', '0']
    if encoder == 'libx264':
        return ['-c:v', encoder, '-preset', 'medium', '-crf', '12']
    raise ValueError('Encoder must be resolved before creating arguments')
