# GPU encoding for reviews

## Policy

Prefer hardware encoding for review/section cuts after a real smoke test. Keep
completed masters and their settings unchanged. For final masters compare source
detail, text edges, gradients, colour and motion before choosing GPU settings.
No silent quality downgrade, resolution reduction, speed change or audio mastering.

## Detect and verify

```bash
python3 scripts/check_setup.py --profile video --check-gpu
nvidia-smi --query-gpu=name,utilization.gpu,utilization.encoder,utilization.decoder,memory.used --format=csv
```

The selected ffmpeg must actually open the encoder. An encoder listed by ffmpeg
can still fail because of drivers, device permissions, unsupported hardware or
session limits. Do not install drivers/change desktop config without permission.
Other platforms may use VideoToolbox/VAAPI after separate validation; the bundled
selector currently implements NVIDIA NVENC and libx264 only.

## Settings

For NVIDIA H.264 review cuts:

```text
-c:v h264_nvenc -preset p5 -tune hq -rc vbr -cq 18 -b:v 0
-pix_fmt yuv420p -color_primaries bt709 -color_trc bt709 -colorspace bt709
```

Use these BT.709 tags only for BT.709 projects; do not mislabel HDR/other sources.
Use AAC 320k when re-encoding approved delivery audio; preserve original audio
where container/format allows. Avoid repeated lossy generations; reuse original
or high-quality section assets. High-quality working intermediates can start at
CQ14; this is not lossless. CQ18 is not equivalent to CRF18. Use new cache keys
when changing encoders/settings, and do not reuse interrupted files as valid media.

The shared renderer's `--encoder auto --nvenc-cq 18` performs the smoke test and
records the selected encoder in its working plan. `auto` reports fallback to CPU;
`--encoder h264_nvenc` requires success. It caps NVENC workers at 2 to limit
session/VRAM pressure. The existing libx264 master default remains unchanged.

## Remotion and other renderers

Hardware H.264 encoding is distinct from browser GPU acceleration. Check the
installed Remotion version's actual supported options before adding flags.
Software WebGL/SwiftShader may still be required by an effect; test a short range
before switching browser backends. NVENC cannot accelerate numpy, libass, PNG
staging, browser layout or every decoder. Do not claim all-GPU rendering.

## Validate and measure

1. Compare the same 2–5 second raw-derived segment, dimensions, fps and audio.
2. Time encoding separately from compositing and decoding. Report preset/CQ/CRF.
3. Decode the output; inspect motion, text and gradients. PSNR/SSIM are supplementary,
   not proof of perceptual equivalence.
4. Verify exact frame count/duration, BT.709 tags where applicable, audio alignment
   and peaks. Verify section-only boundaries before publishing review files.
5. Watch encoder/decoder utilization while the relevant stage is active. Total GPU
   use from desktop/other apps does not prove the video pipeline uses NVENC.
6. On failure leave completed work intact, report the problem and fall back only
   when allowed. Stop only identified owned jobs when switching active workflows.

## Local test, 2026-11-08

RTX 3060, 1080p30 talking-head source, 2-second sample: x264 slow CRF14 with
2 threads took 18.198s; NVENC p5 CQ18 took 1.510s (~12.05× encoding-test speedup).
SSIM versus source: .994244 CPU, .993105 GPU. Both decoded successfully. This is
one sample under current machine load, not a guaranteed end-to-end speedup.
Project evidence: `Videos/ai_usage_level_for_non_dev/qa/gpu-encoding/benchmark.json`.
