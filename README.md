# Mega AutoPromo Generator V2 (Python GUI)

A mega-deluxe desktop GUI for building FFmpeg-powered AutoPromo videos.

## Features Included

- **Input & Source Support**
  - Multiple source clips (local files + URL clips via `yt-dlp`)
  - Bulk URL import (paste one URL per line)
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
  - Kids-oriented auto color grading

- **Music & Audio Features**
  - Music remix + auto-fade workflow controls
  - Event-driven SFX placement checkboxes
  - Voiceover and speech-priority mixing strategy
  - Auto-volume leveling model (speech > music > effects)
  - Auto-mute support with selectable mute modes

- **Output Options**
  - Aspect ratios: 4:3, 16:9, 9:16
  - Exports: mp4, gif teaser, web preview
  - Preview rendering with low-res profile
  - Quality profile selector (includes 360p)
  - Mega Deluxe controls for Width, Height, FPS, 360p preview profile, bitrate

- **Build Modes**
  - Promo / Remix / Songs

- **Mega Deluxe Generation Settings**
  - Min Clip / Max Clip / Total Clips for promo-remix-song generation
  - Random seed for automatic generation behavior
  - Transition seconds, Dance Intensity, Promo Intensity
  - Promo mode, Songs mode, Remix mode, Songs remix mode
  - Intro library and Outro library insertion
  - Generated naming preset: `Generated Mega Deluxe Promo & Remix & Songs`
  - **V2 Long-Form Engine**: target duration + auto-expanded clip sequencing for longer promos

## Run

```bash
python3 mega_autopromo_generator.py
```

On Windows:

```bat
run_windows.bat
```

## Config JSON

- Use **Save Config JSON** to export all current generation settings.
- Use **Import Config JSON** to restore a previously saved setup (sources, modes, output settings, and mega-deluxe options).

## Dependencies

- Python 3.8+ (recommended for Windows 8.1 compatibility)
- FFmpeg in PATH
- Optional: `yt-dlp` in PATH for URL clip download
- Optional but recommended: `ffprobe` in PATH for media-duration probing, auto-trim in/out points, and long-form timeline estimation

## Windows 8.1 support

- The app includes Windows-specific compatibility behavior:
  - prefers `ffmpeg.exe` / `yt-dlp.exe` resolution when available
  - normalizes concat file paths for FFmpeg on Windows
  - logs Windows 8.1 compatibility mode at startup

## Notes

This app now generates a longer FFmpeg pipeline including metadata overlays, drawtext promo elements, audio loudness/limiter chain, optional background-song + voiceover remix, transition fades, color enhancement, and mode-aware export behavior for promo/remix/songs.

V2 introduces a long-form expansion mode that can repeat selected clips to reach a target runtime, then applies runtime-aware fade-out timing and explicit output duration controls. It now uses `ffprobe` metadata for better clip-duration estimation and concat trimming behavior.
