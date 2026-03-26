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
  - Mega Deluxe controls for Width, Height, FPS, 360p preview profile, bitrate

- **Promo & Song Logic**
  - Remix styles: Kids dance, Funk, Pop kids
  - Theme cues: Clap, Cheer, Whoosh
  - Automatic tagline generation based on mood + tempo
  - Build modes: Promo / Remix / Songs

- **Mega Deluxe Generation Settings**
  - Min Clip / Max Clip / Total Clips for promo-remix-song generation
  - Random seed for automatic generation behavior
  - Transition seconds, Dance Intensity, Promo Intensity
  - Promo mode, Songs mode, Remix mode, Songs remix mode
  - Intro library and Outro library insertion
  - Generated naming preset: `Generated Mega Deluxe Promo & Remix & Songs`

## Run

```bash
python3 mega_autopromo_generator.py
```

On Windows:

```bat
run_windows.bat
```

## Dependencies

- Python 3.8+ (recommended for Windows 8.1 compatibility)
- FFmpeg in PATH
- Optional: `yt-dlp` in PATH for URL clip download

## Windows 8.1 support

- The app includes Windows-specific compatibility behavior:
  - prefers `ffmpeg.exe` / `yt-dlp.exe` resolution when available
  - normalizes concat file paths for FFmpeg on Windows
  - logs Windows 8.1 compatibility mode at startup

## Notes

This app now generates a longer FFmpeg pipeline including metadata overlays, drawtext promo elements, audio loudness/limiter chain, optional background-song + voiceover remix, transition fades, color enhancement, and mode-aware export behavior for promo/remix/songs.
