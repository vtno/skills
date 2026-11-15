---
name: talking-head-video
description: Edit or visually finish talking-to-camera videos for YouTube and other formats, including landscape 16:9, vertical 9:16, square and source dimensions. Use for interviews, tutorials, explainers and longer talking-head videos with captions, B-roll and graphics. Adapts pacing and style to project references; uses the shared video-editing Python/ffmpeg pipeline.
---

# Talking-head video

Turn a presenter recording into a finished video without assuming it is a short
vertical reel. **First read sibling `video-editing/SKILL.md`** for executable
workflow, capability checks, versioning and delivery. Resolve its directory as
`VIDEO_EDITING`; all scripts and shared assets live there.

## Project decisions

Ask only for missing details: footage, language/script, output destination/format,
whether the footage is already cut, desired pacing, project references/brand
direction, audio changes, asset permissions and project folder.

- Default to preserving speech, order, pauses and duration for already-cut footage.
  Do not tighten or rewrite content without permission.
- Keep source dimensions by default. If the user asks for normal YouTube, choose
  1920x1080 (`--format 16:9`); avoid unnecessary upscaling and discuss a lower custom
  size for small sources. `--width` and `--height` set even custom dimensions.
- Setup uses `--profile video`, **not** the reel default. Example:
  `prepare_project.py INPUT --project PROJECT --profile video --format 16:9`.
- Style references are per-project inputs. Do not force archival B&W, red accents,
  Anton headlines, grain, flashing, music or an end CTA onto every project.
- With no references, propose a restrained direction: camera colour, readable
  captions when requested, clear chapter graphics and relevant illustrative footage.

## Edit direction

Read `video-editing/references/formats.md`. Landscape layouts are designed anew,
not stretched vertical compositions. Use negative space around the presenter for
titles; maintain headroom, readable labels and player-safe caption margins. Show a
beat/section plan before expensive sourcing. For long videos plan chapter by chapter.

Let speech lead pacing. Hold on the presenter when useful; insert B-roll to explain
an idea, demonstrate a step or cover an approved cut. No mandatory 2–4-second visual
change. Keep full-frame demonstrations visible long enough to understand them.
Use restrained transitions by default; use the supplied animated treatments only
when they fit the approved reference direction.

The current renderer's `layout: split` is **top/bottom in every aspect ratio**.
Do not promise side-by-side presenter layouts. In 16:9 prefer full-frame inserts or
framed demonstrations until a real side-by-side implementation exists.

Follow the shared workflow: transcript → approved timeline policy → optional audio
and mattes → starter EDL → footage → validation → stills → MP4 → motion/audio QA.
Use format-specific text coordinates and sizes; verify a 16:9 still early. Preserve
approved sound for visual-only changes. Deliver a versioned MP4 and editable
project/dependencies, with honest capability and QA limitations.
