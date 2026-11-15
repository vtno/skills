# Local regression tests

From this skill's directory, with Python containing numpy and ffmpeg/libass on PATH:

```bash
python3 -m unittest discover -s tests -v
```

The suite checks output dimensions and invalid sizes, profile defaults, configuration
fallbacks, identity timeline/audio preservation, legacy reel framing, overwrite
protection, and real short renders/previews at landscape, portrait and square sizes.
Synthetic test patterns and sine audio are generated locally. No paid services,
transcription models, user footage or Apple Vision are used. Temporary test projects
are removed when the suite completes.

This does not certify artistic quality, long-video performance, non-Latin glyph
coverage, transcription or macOS matte processing. Review actual project footage
and full exports independently.
