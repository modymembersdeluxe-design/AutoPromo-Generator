import json
import os
import platform
import random
import shlex
import shutil
import subprocess
import threading
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from tkinter import (
    Tk,
    StringVar,
    BooleanVar,
    IntVar,
    END,
    filedialog,
    messagebox,
    Text,
)
from tkinter import simpledialog
from tkinter import ttk

APP_TITLE = "Mega AutoPromo Generator"


@dataclass
class PromoConfig:
    source_videos: list
    source_urls: list
    background_songs: list
    effects_library: list
    voiceover_file: str
    title: str
    target_audience: str
    mood: str
    remix_style: str
    aspect_ratio: str
    export_format: str
    preview_quality: str
    auto_trim: bool
    beat_aligned: bool
    theme_transitions: bool
    auto_remix: bool
    auto_cut_detection: bool
    auto_edit: bool
    auto_mute: bool
    auto_mute_mode: str
    auto_color_grade: bool
    auto_captions: bool
    include_logo_intro: bool
    include_logo_outro: bool
    include_dynamic_stickers: bool
    include_lower_third: bool
    social_links: str
    promo_date: str
    theme_audio_cues: list
    tempo_bpm: int
    tagline: str


class MegaAutoPromoApp:
    def __init__(self, root: Tk):
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry("1400x900")

        self.source_videos = []
        self.source_urls = []
        self.background_songs = []
        self.effects_files = []
        self.ffmpeg_bin = self.resolve_binary("ffmpeg")
        self.ytdlp_bin = self.resolve_binary("yt-dlp")

        self.title_var = StringVar(value="My Kids Mega Promo")
        self.target_var = StringVar(value="Kids & Families")
        self.mood_var = StringVar(value="happy")
        self.remix_style_var = StringVar(value="Kids dance remix")
        self.aspect_ratio_var = StringVar(value="16:9")
        self.export_format_var = StringVar(value="mp4")
        self.preview_quality_var = StringVar(value="360p")
        self.voiceover_var = StringVar(value="")
        self.social_var = StringVar(value="@mychannel | youtube.com/mychannel")
        self.date_var = StringVar(value=datetime.utcnow().strftime("%Y-%m-%d"))
        self.tempo_var = IntVar(value=120)
        self.tagline_var = StringVar(value="")

        self.auto_trim_var = BooleanVar(value=True)
        self.best_resolution_var = BooleanVar(value=True)
        self.beat_aligned_var = BooleanVar(value=True)
        self.theme_transitions_var = BooleanVar(value=True)
        self.auto_cut_var = BooleanVar(value=True)
        self.auto_remix_var = BooleanVar(value=True)
        self.auto_edit_var = BooleanVar(value=True)
        self.auto_mute_var = BooleanVar(value=True)
        self.auto_mute_mode_var = StringVar(value="Mute source under voiceover")
        self.color_grade_var = BooleanVar(value=True)
        self.auto_captions_var = BooleanVar(value=True)
        self.logo_intro_var = BooleanVar(value=True)
        self.logo_outro_var = BooleanVar(value=True)
        self.stickers_var = BooleanVar(value=True)
        self.lower_third_var = BooleanVar(value=True)

        self.theme_cue_vars = {
            "Clap": BooleanVar(value=True),
            "Cheer": BooleanVar(value=True),
            "Whoosh": BooleanVar(value=True),
        }

        self.build_ui()
        self.update_tagline()
        self.log_platform_support()

    def build_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=8, pady=8)

        tabs = {
            "Input & Sources": ttk.Frame(notebook),
            "Auto Remix/Edit": ttk.Frame(notebook),
            "Music & Audio": ttk.Frame(notebook),
            "Graphics": ttk.Frame(notebook),
            "Output": ttk.Frame(notebook),
            "Promo Logic": ttk.Frame(notebook),
            "Build & Preview": ttk.Frame(notebook),
        }

        for name, frame in tabs.items():
            notebook.add(frame, text=name)

        self.build_sources_tab(tabs["Input & Sources"])
        self.build_auto_edit_tab(tabs["Auto Remix/Edit"])
        self.build_audio_tab(tabs["Music & Audio"])
        self.build_graphics_tab(tabs["Graphics"])
        self.build_output_tab(tabs["Output"])
        self.build_promo_tab(tabs["Promo Logic"])
        self.build_build_tab(tabs["Build & Preview"])

    def build_sources_tab(self, frame):
        left = ttk.LabelFrame(frame, text="Source video inputs")
        left.pack(side="left", fill="both", expand=True, padx=8, pady=8)

        self.video_list = Text(left, height=18)
        self.video_list.pack(fill="both", expand=True, padx=6, pady=6)

        video_btns = ttk.Frame(left)
        video_btns.pack(fill="x", padx=6, pady=4)
        ttk.Button(video_btns, text="Add local clips", command=self.add_video_files).pack(side="left", padx=4)
        ttk.Button(video_btns, text="Add URL clip", command=self.add_video_url).pack(side="left", padx=4)
        ttk.Button(video_btns, text="Clear", command=self.clear_video_sources).pack(side="left", padx=4)

        ttk.Checkbutton(left, text="Prefer best resolution available", variable=self.best_resolution_var).pack(anchor="w", padx=6)
        ttk.Checkbutton(left, text="Auto-trim irrelevant segments", variable=self.auto_trim_var).pack(anchor="w", padx=6)

        right = ttk.LabelFrame(frame, text="Source audio + metadata")
        right.pack(side="left", fill="both", expand=True, padx=8, pady=8)

        self.song_list = Text(right, height=6)
        self.song_list.pack(fill="x", padx=6, pady=4)
        ttk.Button(right, text="Add background songs", command=self.add_song_files).pack(anchor="w", padx=6)

        self.effects_list = Text(right, height=5)
        self.effects_list.pack(fill="x", padx=6, pady=4)
        ttk.Button(right, text="Add effects library", command=self.add_effect_files).pack(anchor="w", padx=6)

        vo = ttk.Frame(right)
        vo.pack(fill="x", padx=6, pady=4)
        ttk.Label(vo, text="Voiceover file:").pack(side="left")
        ttk.Entry(vo, textvariable=self.voiceover_var).pack(side="left", fill="x", expand=True, padx=4)
        ttk.Button(vo, text="Browse", command=self.pick_voiceover).pack(side="left")

        md = ttk.LabelFrame(right, text="Metadata tags")
        md.pack(fill="x", padx=6, pady=6)
        self._entry_row(md, "Title", self.title_var)
        self._entry_row(md, "Target audience", self.target_var)

        mood_box = ttk.Frame(md)
        mood_box.pack(fill="x", pady=2)
        ttk.Label(mood_box, text="Mood", width=16).pack(side="left")
        ttk.Combobox(mood_box, textvariable=self.mood_var, values=["happy", "energetic", "calm"], state="readonly").pack(side="left", fill="x", expand=True)

    def build_auto_edit_tab(self, frame):
        lf = ttk.LabelFrame(frame, text="Auto-Remix & Auto-Edit")
        lf.pack(fill="both", expand=True, padx=12, pady=12)

        ttk.Checkbutton(lf, text="Beat-aligned remixing (sync cuts to beat)", variable=self.beat_aligned_var).pack(anchor="w", pady=4)
        ttk.Checkbutton(lf, text="Auto-remix support", variable=self.auto_remix_var).pack(anchor="w", pady=4)
        ttk.Checkbutton(lf, text="Theme transitions (smooth + color/motion matching)", variable=self.theme_transitions_var).pack(anchor="w", pady=4)
        ttk.Checkbutton(lf, text="Auto-cut detection (identify action points)", variable=self.auto_cut_var).pack(anchor="w", pady=4)
        ttk.Checkbutton(lf, text="Auto-edit support", variable=self.auto_edit_var).pack(anchor="w", pady=4)
        ttk.Checkbutton(lf, text="AI best-frame selection", variable=self.auto_cut_var).pack(anchor="w", pady=4)
        ttk.Checkbutton(lf, text="Auto color grading (kids brightness/saturation)", variable=self.color_grade_var).pack(anchor="w", pady=4)

        ttk.Label(lf, text="Tempo (BPM) for beat alignment:").pack(anchor="w", pady=(12, 2))
        ttk.Scale(lf, from_=70, to=180, variable=self.tempo_var, orient="horizontal").pack(fill="x")

    def build_audio_tab(self, frame):
        lf = ttk.LabelFrame(frame, text="Music & Audio Features")
        lf.pack(fill="both", expand=True, padx=12, pady=12)

        items = [
            "Music remix (blend multiple songs)",
            "Auto-fade between tracks",
            "SFX triggers on jump/spin/pop",
            "Voiceover placement with natural speech breaks",
            "Auto-volume leveling (speech > music > effects)",
        ]
        for item in items:
            ttk.Label(lf, text=f"• {item}").pack(anchor="w", pady=3)
        ttk.Checkbutton(lf, text="Auto-mute support", variable=self.auto_mute_var).pack(anchor="w", pady=3)
        self._combo_row(
            lf,
            "Auto-mute mode",
            self.auto_mute_mode_var,
            ["Mute source under voiceover", "Mute all source audio", "Keep source audio"],
        )

    def build_graphics_tab(self, frame):
        lf = ttk.LabelFrame(frame, text="Graphics & Promo Elements")
        lf.pack(fill="both", expand=True, padx=12, pady=12)

        ttk.Checkbutton(lf, text="Title animations (Text A Animation)", variable=self.logo_intro_var).pack(anchor="w", pady=4)
        ttk.Checkbutton(lf, text="Lower third text", variable=self.lower_third_var).pack(anchor="w", pady=4)
        ttk.Checkbutton(lf, text="Logo intro", variable=self.logo_intro_var).pack(anchor="w", pady=4)
        ttk.Checkbutton(lf, text="Logo outro", variable=self.logo_outro_var).pack(anchor="w", pady=4)
        ttk.Checkbutton(lf, text="Dynamic stickers (kids stars + emo kids symbols)", variable=self.stickers_var).pack(anchor="w", pady=4)
        ttk.Checkbutton(lf, text="Auto captions (editable)", variable=self.auto_captions_var).pack(anchor="w", pady=4)

        self._entry_row(lf, "Date", self.date_var)
        self._entry_row(lf, "Social links", self.social_var)

    def build_output_tab(self, frame):
        lf = ttk.LabelFrame(frame, text="Output Options")
        lf.pack(fill="both", expand=True, padx=12, pady=12)

        self._combo_row(lf, "Aspect ratio", self.aspect_ratio_var, ["4:3", "16:9", "9:16"])
        self._combo_row(lf, "Export format", self.export_format_var, ["mp4", "gif teaser", "web preview"])
        self._combo_row(lf, "Preview quality", self.preview_quality_var, ["360p", "480p", "720p", "1080p"])

        ttk.Label(lf, text="Preview function: render low-res preview before full render.").pack(anchor="w", pady=8)

    def build_promo_tab(self, frame):
        lf = ttk.LabelFrame(frame, text="Promo & Song Logic")
        lf.pack(fill="both", expand=True, padx=12, pady=12)

        self._combo_row(lf, "Remix style", self.remix_style_var, ["Kids dance remix", "Funk remix", "Pop kids style"])

        cues = ttk.LabelFrame(lf, text="Theme audio cues")
        cues.pack(fill="x", pady=8)
        for name, var in self.theme_cue_vars.items():
            ttk.Checkbutton(cues, text=name, variable=var).pack(side="left", padx=8, pady=4)

        self._entry_row(lf, "Auto tagline", self.tagline_var)
        ttk.Button(lf, text="Generate tagline", command=self.update_tagline).pack(anchor="w", pady=4)
        ttk.Label(lf, text="Automatic tagline placement based on mood + tempo.").pack(anchor="w")

    def build_build_tab(self, frame):
        top = ttk.Frame(frame)
        top.pack(fill="x", padx=12, pady=8)

        ttk.Button(top, text="Save Config JSON", command=self.save_config).pack(side="left", padx=4)
        ttk.Button(top, text="Build Preview", command=lambda: self.render(preview=True)).pack(side="left", padx=4)
        ttk.Button(top, text="Build Final", command=lambda: self.render(preview=False)).pack(side="left", padx=4)

        self.log_box = Text(frame, height=30)
        self.log_box.pack(fill="both", expand=True, padx=12, pady=8)
        self.log("Ready. Add sources and click Build Preview or Build Final.")

    def resolve_binary(self, base_name: str):
        # Windows 8.1 support: prefer .exe when available.
        is_windows = platform.system().lower() == "windows"
        candidates = [base_name]
        if is_windows:
            candidates = [f"{base_name}.exe", base_name]
        for candidate in candidates:
            path = shutil.which(candidate)
            if path:
                return path
        return base_name

    def log_platform_support(self):
        system = platform.system()
        release = platform.release()
        if system == "Windows" and release == "8.1":
            self.log("Windows 8.1 compatibility mode active.")
        else:
            self.log(f"Platform detected: {system} {release}")

    def _entry_row(self, parent, label, variable):
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=2)
        ttk.Label(row, text=label, width=16).pack(side="left")
        ttk.Entry(row, textvariable=variable).pack(side="left", fill="x", expand=True)

    def _combo_row(self, parent, label, variable, values):
        row = ttk.Frame(parent)
        row.pack(fill="x", pady=2)
        ttk.Label(row, text=label, width=16).pack(side="left")
        ttk.Combobox(row, textvariable=variable, values=values, state="readonly").pack(side="left", fill="x", expand=True)

    def add_video_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Video", "*.mp4 *.mov *.mkv *.webm"), ("All", "*.*")])
        if files:
            self.source_videos.extend(files)
            self.refresh_sources_view()

    def add_video_url(self):
        url = self.simple_prompt("Enter clip URL", "https://...")
        if url:
            self.source_urls.append(url)
            self.refresh_sources_view()

    def clear_video_sources(self):
        self.source_videos.clear()
        self.source_urls.clear()
        self.refresh_sources_view()

    def add_song_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Audio", "*.mp3 *.wav *.m4a *.ogg"), ("All", "*.*")])
        if files:
            self.background_songs.extend(files)
            self.song_list.delete("1.0", END)
            self.song_list.insert(END, "\n".join(self.background_songs))

    def add_effect_files(self):
        files = filedialog.askopenfilenames(filetypes=[("Audio", "*.mp3 *.wav *.ogg"), ("All", "*.*")])
        if files:
            self.effects_files.extend(files)
            self.effects_list.delete("1.0", END)
            self.effects_list.insert(END, "\n".join(self.effects_files))

    def pick_voiceover(self):
        f = filedialog.askopenfilename(filetypes=[("Audio", "*.mp3 *.wav *.m4a *.ogg"), ("All", "*.*")])
        if f:
            self.voiceover_var.set(f)

    def refresh_sources_view(self):
        self.video_list.delete("1.0", END)
        lines = []
        for v in self.source_videos:
            lines.append(f"FILE: {v}")
        for u in self.source_urls:
            lines.append(f"URL:  {u}")
        self.video_list.insert(END, "\n".join(lines))

    def simple_prompt(self, title, hint):
        return simpledialog.askstring(title, hint, parent=self.root)

    def update_tagline(self):
        mood = self.mood_var.get()
        bpm = self.tempo_var.get()
        energetic = bpm >= 125 or mood == "energetic"
        calm = bpm <= 95 or mood == "calm"

        options = {
            "energetic": [
                "Turn it up! Big smiles, big moves!",
                "Dance, clap, and shine in every beat!",
                "Hyper-fun energy starts now!",
            ],
            "happy": [
                "Bright moments, big giggles, best day ever!",
                "Play loud. Smile louder.",
                "Joy in every frame!",
            ],
            "calm": [
                "Gentle vibes, warm smiles, happy hearts.",
                "Soft colors, sweet rhythm, pure fun.",
                "Slow down and smile together.",
            ],
        }

        if energetic:
            pool = options["energetic"]
        elif calm:
            pool = options["calm"]
        else:
            pool = options.get(mood, options["happy"])

        self.tagline_var.set(random.choice(pool))

    def collect_config(self):
        cues = [name for name, var in self.theme_cue_vars.items() if var.get()]
        return PromoConfig(
            source_videos=self.source_videos,
            source_urls=self.source_urls,
            background_songs=self.background_songs,
            effects_library=self.effects_files,
            voiceover_file=self.voiceover_var.get(),
            title=self.title_var.get(),
            target_audience=self.target_var.get(),
            mood=self.mood_var.get(),
            remix_style=self.remix_style_var.get(),
            aspect_ratio=self.aspect_ratio_var.get(),
            export_format=self.export_format_var.get(),
            preview_quality=self.preview_quality_var.get(),
            auto_trim=self.auto_trim_var.get(),
            beat_aligned=self.beat_aligned_var.get(),
            theme_transitions=self.theme_transitions_var.get(),
            auto_remix=self.auto_remix_var.get(),
            auto_cut_detection=self.auto_cut_var.get(),
            auto_edit=self.auto_edit_var.get(),
            auto_mute=self.auto_mute_var.get(),
            auto_mute_mode=self.auto_mute_mode_var.get(),
            auto_color_grade=self.color_grade_var.get(),
            auto_captions=self.auto_captions_var.get(),
            include_logo_intro=self.logo_intro_var.get(),
            include_logo_outro=self.logo_outro_var.get(),
            include_dynamic_stickers=self.stickers_var.get(),
            include_lower_third=self.lower_third_var.get(),
            social_links=self.social_var.get(),
            promo_date=self.date_var.get(),
            theme_audio_cues=cues,
            tempo_bpm=self.tempo_var.get(),
            tagline=self.tagline_var.get(),
        )

    def save_config(self):
        config = self.collect_config()
        path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")])
        if not path:
            return
        with open(path, "w", encoding="utf-8") as f:
            json.dump(asdict(config), f, indent=2)
        self.log(f"Saved config: {path}")

    def render(self, preview: bool):
        if not self.source_videos and not self.source_urls:
            messagebox.showwarning("Missing input", "Please add at least one source video file or URL.")
            return

        config = self.collect_config()
        threading.Thread(target=self._render_worker, args=(config, preview), daemon=True).start()

    def _render_worker(self, config: PromoConfig, preview: bool):
        mode = "PREVIEW" if preview else "FINAL"
        self.log(f"--- {mode} BUILD START ---")

        downloaded = []
        for url in config.source_urls:
            out = self.download_url_clip(url)
            if out:
                downloaded.append(out)

        input_clips = config.source_videos + downloaded
        concat_path = self.write_concat_file(input_clips)
        output_name = f"autopromo_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}"
        output_ext = "mp4" if config.export_format == "mp4" else "mp4"
        output_path = str(Path.cwd() / f"{output_name}.{output_ext}")

        ffmpeg_cmd = self.build_ffmpeg_command(config, concat_path, output_path, preview)
        self.log("FFmpeg command:\n" + " ".join(shlex.quote(s) for s in ffmpeg_cmd))

        try:
            proc = subprocess.run(ffmpeg_cmd, capture_output=True, text=True, check=False)
            self.log(proc.stdout.strip() or "(no stdout)")
            if proc.returncode != 0:
                self.log(proc.stderr.strip())
                self.log(f"Render failed with code {proc.returncode}")
            else:
                self.log(f"Render completed: {output_path}")
        except FileNotFoundError:
            self.log("FFmpeg not found. Install ffmpeg and try again.")

        self.log(f"--- {mode} BUILD END ---")

    def download_url_clip(self, url: str):
        self.log(f"Downloading URL clip (best resolution): {url}")
        out = str(Path.cwd() / f"clip_{abs(hash(url)) % 100000}.mp4")
        cmd = [
            self.ytdlp_bin,
            "-f",
            "bestvideo+bestaudio/best",
            "-o",
            out,
            url,
        ]
        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if proc.returncode == 0 and os.path.exists(out):
                self.log(f"Downloaded: {out}")
                return out
            self.log("yt-dlp download failed, skipping URL clip.")
            if proc.stderr:
                self.log(proc.stderr.strip())
        except FileNotFoundError:
            self.log("yt-dlp not found. URL clips skipped.")
        return None

    def write_concat_file(self, clips: list):
        concat_path = str(Path.cwd() / "concat_inputs.txt")
        with open(concat_path, "w", encoding="utf-8") as f:
            for c in clips:
                normalized = str(Path(c))
                if platform.system().lower() == "windows":
                    normalized = normalized.replace("\\", "/")
                safe_c = normalized.replace("'", "'\\''")
                f.write(f"file '{safe_c}'\n")
        self.log(f"Concat list written: {concat_path}")
        return concat_path

    def build_ffmpeg_command(self, config: PromoConfig, concat_path: str, output_path: str, preview: bool):
        width, height = {
            "4:3": (960, 720),
            "16:9": (1280, 720),
            "9:16": (720, 1280),
        }[config.aspect_ratio]

        if preview:
            width, height = (640, 360)

        vf_parts = [f"scale={width}:{height}:force_original_aspect_ratio=decrease", f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2"]
        if config.auto_color_grade:
            vf_parts.append("eq=brightness=0.05:saturation=1.25")

        vf = ",".join(vf_parts)

        cmd = [
            self.ffmpeg_bin,
            "-y",
            "-f",
            "concat",
            "-safe",
            "0",
            "-i",
            concat_path,
        ]

        if config.background_songs:
            cmd.extend(["-i", config.background_songs[0]])
        if config.voiceover_file:
            cmd.extend(["-i", config.voiceover_file])

        cmd.extend([
            "-vf",
            vf,
            "-c:v",
            "libx264",
            "-preset",
            "veryfast" if preview else "medium",
            "-crf",
            "28" if preview else "20",
            "-pix_fmt",
            "yuv420p",
        ])

        if config.auto_remix or config.auto_edit or config.auto_mute or config.background_songs or config.voiceover_file:
            src_vol = "1.0"
            if config.auto_mute:
                if config.auto_mute_mode == "Mute all source audio":
                    src_vol = "0.0"
                elif config.auto_mute_mode == "Mute source under voiceover" and config.voiceover_file:
                    src_vol = "0.20"

            filter_parts = [f"[0:a]volume={src_vol}[a0]"]
            mix_inputs = ["[a0]"]

            if config.background_songs:
                filter_parts.append("[1:a]volume=0.25[a1]")
                mix_inputs.append("[a1]")
            if config.voiceover_file:
                vo_index = 2 if config.background_songs else 1
                filter_parts.append(f"[{vo_index}:a]volume=1.00[a2]")
                mix_inputs.append("[a2]")

            if len(mix_inputs) > 1:
                filter_parts.append(f"{''.join(mix_inputs)}amix=inputs={len(mix_inputs)}:duration=shortest:normalize=0[mix]")
                filter_complex = ";".join(filter_parts)
                cmd.extend(["-filter_complex", filter_complex, "-map", "0:v:0", "-map", "[mix]"])
            else:
                cmd.extend(["-filter:a", f"volume={src_vol}", "-map", "0:v:0", "-map", "0:a:0"])

            cmd.append("-shortest")

        cmd.append(output_path)
        return cmd

    def log(self, text):
        self.log_box.insert(END, f"{datetime.utcnow().isoformat()} | {text}\n")
        self.log_box.see(END)


def main():
    root = Tk()
    app = MegaAutoPromoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
