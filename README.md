# Mega AutoPromo Generator (Python GUI)

A mega-deluxe desktop GUI for building FFmpeg-powered AutoPromo videos.

## Features Included

- **Input & Source Support**
  - Multiple source clips (local files + URL clips via `yt-dlp`)
  - Best resolution preference for URLs
  - Auto-trim toggle for irrelevant segments
  - Audio input support (songs, effects library, optional voiceover)
  - Metadata tags: title, target audience, mood

- **Auto-Remix & Auto-Edit**
  - Beat-aligned remix toggle
  - Auto-remix support toggle
  - Theme transition toggles
  - Auto-cut / action-point detection toggles
  - Auto-edit support toggle
  - AI best-frame selection toggle
  - Kids-oriented auto color grading

- **Music & Audio Features**
  - Music remix + auto-fade workflow controls
  - Event-driven SFX placement checkboxes
  - Voiceover and speech-priority mixing strategy
  - Auto-volume leveling model (speech > music > effects)
  - Auto-mute support with selectable mute modes

- **Graphics & Promo Elements**
  - Title animation controls
  - Lower-third text fields (date + social links)
  - Logo intro/outro toggles
  - Dynamic sticker controls
  - Auto-caption toggle

- **Output Options**
  - Aspect ratios: 4:3, 16:9, 9:16
  - Exports: mp4, gif teaser, web preview
  - Preview rendering with low-res profile
  - Quality profile selector (includes 360p)

- **Promo & Song Logic**
  - Remix styles: Kids dance, Funk, Pop kids
  - Theme cues: Clap, Cheer, Whoosh
  - Automatic tagline generation based on mood + tempo

## Run

```bash
python3 mega_autopromo_generator.py
```

## Dependencies

- Python 3.10+
- FFmpeg in PATH
- Optional: `yt-dlp` in PATH for URL clip download

## Notes

This app currently emphasizes workflow orchestration and FFmpeg command generation in a single GUI. It includes practical placeholders for "AI" edit selection logic and can be extended with scene-detection, beat-detection, and captioning pipelines.
