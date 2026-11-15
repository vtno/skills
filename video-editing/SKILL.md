---
name: video-editing
description: Shared local Python/ffmpeg tools for speech-led video editing in 16:9, 9:16, square or source dimensions. Use for project setup, transcription, source-to-program timeline mapping, pause cutting, audio mastering, matte processing, JSON edit lists, compositing, previews and MP4 exports. Also use as the shared implementation for talking-head-video and talking-head-reels.
---

# Video editing — shared production tools

This is the implementation layer, not a fixed visual style. For fast vertical
editorial reels read the sibling `talking-head-reels/SKILL.md`; for YouTube and
other talking-head formats read `talking-head-video/SKILL.md`. Both depend on this
folder; install/distribute it alongside either preset. Do not duplicate its scripts.

Resolve `VIDEO_EDITING` to this skill's absolute directory. Run every command with
the same Python environment. Keep user media and generated output in a separate
project folder, never inside the skill.

## Bundled versus project-specific

- `scripts/`: setup, transcription, pause cutting, preserving timelines, audio,
  optional Apple Vision masks, clip sheets, EDL validation and a numpy/libass renderer.
- `assets/`: Anton font (OFL), a portrait halftone texture and a **vertical-only** example EDL.
- `references/edl-schema.md`, `renderer.md`, `broll-sourcing.md`: shared documentation.
- `references/formats.md`: format rules, preset differences and limitations.
- Project references, brand fonts, footage, music and B-roll are supplied or sourced
  per project. No example footage or archival reference videos are bundled.

## Intake and capability check

Confirm source path, project folder, language, output format, whether content may
be cut, visual direction/references, audio policy and asset permissions. Ask only
for missing material decisions. Never infer permission to spend money or publish.

```bash
python3 "$VIDEO_EDITING/scripts/check_setup.py" --profile video
```

## GPU-first review encoding

User preference: **use GPU encoding for review cuts/previews when available**.
For a request to split an existing review video, **cut that existing export first**;
do not rebuild the edit from raw or create full-quality intermediates merely to
isolate sections. Use stream copy when keyframe-aligned; otherwise one direct GPU
encode for exact boundaries. Clearly label inherited older pacing/graphics, and
keep completed newer section masters. Rebuild from raw only when production
quality or a different approved timeline actually requires it.
Before a large job run `check_setup.py --profile video --check-gpu`. It performs
a real NVENC encode, not just an encoder-list check. See
`references/gpu-encoding.md` for settings, fallback and timing/quality validation.

The bundled renderer supports GPU-first encoding explicitly:

```bash
python3 "$VIDEO_EDITING/scripts/render_video.py" PROJECT/edl.json \
  --out PROJECT/render/review_vN.mp4 --encoder auto --nvenc-cq 18 --workers 2
```

`auto` uses working NVIDIA NVENC or reports a CPU fallback. Explicit
`--encoder h264_nvenc` fails clearly if unusable. Existing master default remains
`libx264`; do not silently replace approved master settings or overwrite outputs.
NVENC CQ and x264 CRF are not equivalent. Compare a short representative sample
before changing final-master encoding. Preserve dimensions, fps, colour metadata,
audio and timeline. GPU encoding is **not** GPU decoding or GPU compositing;
Python/numpy/libass and browser effects may still be CPU-bound. Do not promise a
whole-render speedup from an encoding-only benchmark.

Requires Python 3.9+, numpy and ffmpeg with libass; faster-whisper for transcription.
macOS has Didot/Helvetica Neue and optional Apple Vision mattes. Linux uses installed
fontconfig serif/sans fonts: these are explicit substitutions, not the identical
Mac look. Inspect the generated EDL's font names with the user. Supply additional
licensed fonts via `REEL_FONT_FILES` (OS path-separated font file paths), then set
the role-to-PostScript-name mapping in EDL `fonts`. Do not install system packages
or claim cutouts work without a matte backend. Windows is not verified.

## Shared workflow

Read `references/formats.md` and `references/edl-schema.md` before planning layouts.

```bash
python3 "$VIDEO_EDITING/scripts/prepare_project.py" INPUT --project PROJECT --profile video --format 16:9
python3 "$VIDEO_EDITING/scripts/transcribe.py" PROJECT --language en
```

Choose **one** timeline policy:

```bash
# Already-cut footage / visual finishing: no timeline or speech changes
python3 "$VIDEO_EDITING/scripts/prepare_timeline.py" PROJECT
# OR, only when content editing is authorized:
python3 "$VIDEO_EDITING/scripts/cut_pauses.py" PROJECT --pause-sentence 0.45 --pause-mid 0.25
```

For visual-only edits preserve `audio/program_raw.wav`; do not master approved
sound unnecessarily. If audio processing is requested, run `master_audio.py PROJECT`
(approximately -14 LUFS). Optional: `presenter_mattes.py PROJECT` on macOS.

## Edit with a preview and render from the original

Use this workflow when the user wants to edit in Remotion before the final
render. Keep the original footage and every approved draft unchanged.

1. If the user authorizes pause cuts, prepare and review the cut timeline first.
   Otherwise, preserve the existing timing. Save the source-to-program mapping,
   selected words, and approved audio for the chosen timeline.
2. Create a lightweight preview of that same cut for Remotion Studio. Prefer
   GPU encoding when it passes a real encode test. Label the preview and keep
   graphics, B-roll, and sound effects as separate editable layers. Preserve the
   cut boundaries and duration. Use the final frame rate when practical.
3. Build and review the graphics and B-roll against the preview. If a later
   pacing change moves a cut, map the affected layers through source time and
   review their sync again. Do not assume that two cut versions align.
4. Before the final render, rebuild the approved cut from the original footage
   at the target resolution and frame rate. Use a verified lossless intermediate
   where practical, or document any lossy generation. Relink the presenter
   video and approved audio without changing the reviewed layer timing. Keep
   the preview for future editing and do not upscale it as the final source.
5. Compare matched source frames and check frame timestamps, audio sync, and
   transition boundaries. Render short samples of representative graphics and
   cuts. Confirm the actual encoder in the render log, and check the final
   export's dimensions, frame rate, audio peaks, and full decode. Inspect motion
   and listen to the result. Report any checks that remain incomplete.

When a review export already exists and the user asks only to split it, follow
the GPU-first review encoding procedure above. Do not rebuild from the original
until the user requests production quality or a different timeline.

```bash
python3 "$VIDEO_EDITING/scripts/init_edl.py" PROJECT
```

Plan beats against `analysis/program_words.json`, show the plan before expensive
sourcing, and edit the starter EDL. Read `broll-sourcing.md` when sourcing; generation
is optional and needs permission/budget. Keep sources and licences in the project.
Do not reuse the portrait example's coordinates for a landscape edit.

```bash
python3 "$VIDEO_EDITING/scripts/validate_edl.py" PROJECT/edl.json
python3 "$VIDEO_EDITING/scripts/render_video.py" PROJECT/edl.json --stills 0.5 1.2 --out-dir PROJECT/qa/v1
python3 "$VIDEO_EDITING/scripts/render_video.py" PROJECT/edl.json --out PROJECT/render/NAME_v1.mp4
```

Inspect stills for each layout and transition. Then check the actual MP4 in motion
and listen: transitions, source take boundaries, caption sync, masks, sound, no
black/frozen frames or stretching. Probe dimensions, fps, duration and decoding.
Stills/metrics do not substitute for playback; report checks not possible here.
Long videos cost proportionally more time, disk and memory; test a short project
before committing to a full-length export. The renderer isn't a streaming NLE.

## SVG graphics in browser-based edits

For reusable inline SVGs in Remotion or other React video compositions, give
each mounted instance unique, stable IDs for gradients, masks, clip paths,
filters, and other referenced definitions. Never reuse hard-coded document IDs
across icons or sections: Studio may mount hidden scenes alongside the current
scene, causing `url(#...)` references to resolve to another instance and making
graphics disappear or look wrong. Generate a per-instance ID with React `useId()`
and use that same ID in both the definition and every reference; do not generate
random IDs on each frame. Test repeated graphics both in standalone sections and
in the combined composition, including Studio playback and an actual render when
rendering is authorized. Treat ID collisions as a possible diagnosis, not a
confirmed cause until the fix is visually verified.

## Revisions and delivery

Collect numbered notes without changing anything until the user says go. Save the
current EDL as `edl_vN.json` before changing it; use a new render filename every
round. Never overwrite reviewed work. Deliver MP4, editable JSON/project assets or
an exact external dependency list, sources/licences, and remaining limitations.
Create an alternate mix only when the user requests it. An EDL/code project is **not** a
native Premiere/Resolve project; say so.
