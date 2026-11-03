#!/usr/bin/env python3
"""Assemble scene clips or still images into an MP4 using FFmpeg.

This is an offline editor/assembler, not an AI image or video generator.
"""
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
IMAGE_DIR = ROOT / "assets" / "images"
CLIP_DIR = ROOT / "assets" / "clips"
AUDIO_DIR = ROOT / "assets" / "audio"
OUTPUT_DIR = ROOT / "output"
OUTPUT = OUTPUT_DIR / "the-world-through-my-eyes.mp4"
SCENES = range(1, 8)
SCENE_SECONDS = 12


def run(cmd):
    subprocess.run(cmd, check=True)


def main():
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        sys.exit("FFmpeg is required. Install FFmpeg and ensure it is on PATH.")

    OUTPUT_DIR.mkdir(exist_ok=True)
    inputs = []
    for n in SCENES:
        clip = CLIP_DIR / f"scene-{n:02d}.mp4"
        image = next((IMAGE_DIR / f"scene-{n:02d}{ext}" for ext in (".jpg", ".jpeg", ".png", ".webp") if (IMAGE_DIR / f"scene-{n:02d}{ext}").exists()), None)
        if clip.exists():
            inputs.append(("clip", clip))
        elif image:
            inputs.append(("image", image))
        else:
            print(f"Missing scene {n:02d}: add {clip.relative_to(ROOT)} or scene-{n:02d}.jpg/png to assets/images/.")
    if len(inputs) != len(list(SCENES)):
        sys.exit("Render stopped: add all seven scene assets first.")

    # Normalize each scene to 1920x1080, 24 fps, H.264, and a common pixel format.
    normalized = []
    for idx, (kind, path) in enumerate(inputs, start=1):
        target = OUTPUT_DIR / f"normalized-{idx:02d}.mp4"
        if kind == "clip":
            video_filter = "scale=1920:1080:force_original_aspect_ratio=decrease,pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=24,format=yuv420p"
            run([ffmpeg, "-y", "-i", str(path), "-vf", video_filter, "-an", "-t", str(SCENE_SECONDS), "-c:v", "libx264", "-preset", "medium", "-crf", "21", str(target)])
        else:
            # Gentle zoom/pan gives still artwork a cinematic animatic feel.
            video_filter = (
                "scale=2200:1238:force_original_aspect_ratio=increase,"
                "crop=1920:1080,"
                "zoompan=z='min(zoom+0.0005,1.08)':d=288:s=1920x1080:fps=24,"
                "format=yuv420p"
            )
            run([ffmpeg, "-y", "-loop", "1", "-i", str(path), "-vf", video_filter, "-t", str(SCENE_SECONDS), "-an", "-c:v", "libx264", "-preset", "medium", "-crf", "21", str(target)])
        normalized.append(target)

    concat_file = OUTPUT_DIR / "concat.txt"
    concat_file.write_text("".join(f"file '{p.as_posix()}'\n" for p in normalized), encoding="utf-8")
    silent = OUTPUT_DIR / "silent.mp4"
    run([ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", str(concat_file), "-c", "copy", str(silent)])

    narration = AUDIO_DIR / "narration.wav"
    music = AUDIO_DIR / "music.mp3"
    audio_inputs = []
    if narration.exists():
        audio_inputs += ["-i", str(narration)]
    if music.exists():
        audio_inputs += ["-i", str(music)]
    if audio_inputs:
        cmd = [ffmpeg, "-y", "-i", str(silent), *audio_inputs]
        if narration.exists() and music.exists():
            cmd += ["-filter_complex", "[1:a]volume=1.0[n];[2:a]volume=0.16[m];[n][m]amix=inputs=2:duration=first:dropout_transition=2[a]", "-map", "0:v", "-map", "[a]"]
        elif narration.exists():
            cmd += ["-map", "0:v", "-map", "1:a"]
        else:
            cmd += ["-filter_complex", "[1:a]volume=0.18[a]", "-map", "0:v", "-map", "[a]"]
        cmd += ["-shortest", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", str(OUTPUT)]
        run(cmd)
    else:
        shutil.copy2(silent, OUTPUT)

    print(f"Video created: {OUTPUT}")


if __name__ == "__main__":
    main()
