---
name: tinothamtech-video-outro
description: Add TinoThamTech summary music and the membership ending in Remotion. Use for TinoThamTech outro music, end credits, and membership endings.
---

# Add the TinoThamTech outro

Use the `video-editing` and `talking-head-video` skills for the project workflow.
Preserve the spoken words, their order, and approved cuts. Follow the project's
pacing and render rules.

## Find the example and sources

Ask the user for the channel music and membership clip if they are not already
available in the project. The source media is not bundled with this skill.
Calculate timing and audio levels for each new project.

Use the channel music under the summary and membership ending. Copy an excerpt into the
project so the external drive is not needed for the final export. The source
may have silence at the start. Check for and trim that silence.
Keep the original. Make the excerpt long enough for the summary and ending.

Play the membership clip's picture and spoken message after the presenter's
goodbye. Copy the original into the project.

## Set the timing and audio

1. Find the end of the presenter's goodbye in the source audio. Leave about
   200 ms after the speech, then start the membership clip. Confirm the cut by
   ear rather than relying on transcript timings alone.
2. Start the music at the beginning of the summary. Fade it in over about one
   second and fade it out over the last two seconds of the membership clip.
3. Measure the summary voice and set the music to about 60% of its RMS level
   over a representative interval. In the working example the music gain is
   0.299. Measure again for each source, then adjust by ear.
4. Match the membership voice to the main narration. In the working example,
   the summary measures -14.60 LUFS and the processed membership audio measures
   -15.25 LUFS and -1.88 dBTP. Treat these as reference measurements, not fixed
   targets. Use peak-controlled normalization if needed.
5. Mute the membership video's audio and add the processed audio separately.
   Keep the music and voice on independent layers. Check each source for speech
   and existing music before mixing. Listen to the transition and check the
    combined mix for clipping. Create an alternate mix only if requested.

## Set up Remotion

Put the section sequences on a `Sections` track and the music on a separate
track. Remotion Studio rejects overlapping items on one `Track`. If the
summary duration changes, update the music duration, fade, membership start,
and composition duration. Leave standalone sections unchanged when the user
requests the outro only in `Master`.

Some Chromium builds cannot decode the HEVC membership clip. If Studio cannot
play it, create a named H.264 preview and retain the original. Before final
delivery, prepare a compatible full-resolution source. Do not silently use
the preview for the final export.

Review playback and audio in Studio. Start a final export only when the user
authorizes one.
