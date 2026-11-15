# Formats and profiles

## Setup

`prepare_project.py` supports:

| Option | Dimensions |
|---|---|
| `--format 16:9` | 1920x1080 |
| `--format 9:16` | 1080x1920 |
| `--format 1:1` | 1080x1080 |
| `--format source` | Source display dimensions, rounded down to even pixels |
| `--width W --height H` | Custom positive even dimensions; overrides format |

Without an explicit format: `--profile reel` defaults to 9:16; `--profile video`
uses source dimensions. Frame rate comes from the source. EDL W/H override project
W/H; both planner and validator use the same fallback. Existing EDLs without a
profile retain reel behaviour. Do not resize a completed EDL by changing W/H alone:
coordinates, font sizes, rectangles and insert composition need redesign.

## Defaults

`reel`: original alternating wide/tight shots, slow push, halftone, grain, vignette,
fast-pacing warnings and centre-stack typography guidance.

`video`: steady wide framing (explicit `zoom` can add tight shots), no automatic
slow push, no halftone/grain/vignette and no presenter-hold warnings. Inserts default
to `trans: cut`, clips retain colour without the reel colour treatment, and clip
zoom defaults to `[1, 1]`. Explicit `color: false` opts into B&W. Optional
`look.insert_grain` and `look.insert_brightness` control insert noise/brightness
(video defaults 0 and 1; reel defaults 5 and 0.9). Specialized UI/split insert kinds
still have their own animations; choose them only when they fit the direction.
This is a reusable editorial renderer, not an arbitrary effect graph.

## Layout starting points (pixels)

| Canvas | Headline size | Caption size | Caption centre | Safe margin |
|---|---|---|---|---|
| 1920x1080 | 80–140 | 44–60 | (960, 940) | at least 96 horizontal / 54 vertical |
| 1080x1920 reel | 130–270 | 80–100 | project-dependent centre stack | see reel style guide |
| 1080x1080 | 70–120 | 44–60 | (540, 920) | at least 54 |

These are starting points, not guaranteed bounds; measure and render previews.
Keep text away from faces and important interfaces. `max_w` is in canvas pixels.
Fonts may need wider margins for non-Latin scripts. Confirm glyph coverage.

## Current limits

- `layout: split` stacks insert above presenter, even on landscape. Side-by-side
  presenter layouts are not implemented. `vsplit` likewise stacks two B-roll clips.
- Footage is **cover cropped**, not stretched. Pick matching-aspect B-roll and
  inspect `fx` (horizontal focus). To retain a whole portrait demonstration inside
  landscape use `kind: frame` with a matching-aspect `rect` and a deliberate background.
- UI bars use canvas-relative defaults; cards cap their height to the insert area.
  At small sizes, custom UI text/geometry may still require manual layout.
- Halftone texture tiles/crops at its native scale, rather than stretching dots.
- Preview sheets preserve output aspect ratio; frame PNG filenames identify time.
- Apple Vision masks require macOS. On other platforms, supply compatible mattes
  or omit behind-head, silhouette and cutout effects. Fontconfig substitutions are
  not Didot/Helvetica Neue; disclose and approve them.
- Long timelines can produce large libass files/caches. Test performance on a short
  representative edit; no full-length YouTube performance claim is made.
