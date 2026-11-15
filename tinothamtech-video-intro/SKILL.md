---
name: tinothamtech-video-intro
description: Add the TinoThamTech channel introduction after a spoken video intro in Remotion. Use for the fade to black, channel clip, and matching audio levels.
---

# Add the TinoThamTech channel introduction

Use the `video-editing` and `talking-head-video` skills for the project workflow.
Preserve the spoken words and their order. Do not cut a word to meet a timestamp.
Follow the project's pacing and render rules.

## Find the example and source

Ask the user for the channel intro clip if it is not already in the project.
The clip is not bundled with this skill. Copy the original into the project
and calculate the timing and audio levels for the new edit.

## Add the transition and match the audio

1. Find the end of the last spoken word in the intro. Preserve the full sentence.
2. Fade the picture to black near the end of the intro. Start the channel clip
   after the word ends. Avoid a long black hold or a shot after the fade.
   In the working example, the fade lasts 0.2 seconds and the clip starts at
   0:44.4. Use the new project's speech to choose its timing.
3. Measure the channel clip's audio against representative main narration.
   If its peaks are already high, normalize loudness with peak control rather
   than applying gain alone. In the working example, main speech measured
   -14.22 LUFS and the processed channel audio measured -15.66 LUFS and
   -1.45 dBTP. Use these as reference measurements, not fixed targets.
4. Mute the channel video's audio. Add the processed audio as a separate layer.
   Listen to the transition and check the combined true peak before delivery.

## Set up Remotion

If the user asks for the change in `Master` only, leave the standalone intro
composition unchanged. Add the fade to `Master`, then shift each later section
and the composition end to account for the channel clip.

Some Chromium builds cannot decode HEVC. If Studio cannot play the source,
create a named H.264 preview and retain the original. Before final delivery,
prepare a compatible full-resolution source. Do not silently use the preview
for the final export.

Remotion Studio rejects overlapping items on one `Track`. Use separate tracks
for clips that must overlap. Review the transition and the next section in
Studio. Start a final export only when the user authorizes one.
