# The World Through My Eyes

A free, open-source production workspace for a short animated film about an 11-year-old boy with Level 1 autism, his love of facts, his chickens, and his Boxer dog Dante.

## Visual continuity
Use the uploaded reference image as the visual reference when creating assets locally. Keep the same character in every scene:
- 11-year-old boy; tousled brown hair, freckles, large expressive brown eyes.
- Black hoodie and blue jeans unless a scene requires different clothing.
- Dante: the boy's Boxer dog. Match his coat pattern and markings to the approved Dante reference once added.
- Chickens: recurring backyard flock.

**Tone:** warm, respectful, hopeful, and emotionally honest. Autism is part of the boy's identity, not a problem to be fixed. Avoid stereotypes and do not imply every autistic child has the same experience.

## Free production workflow
This repository does not call paid AI APIs or require subscriptions. It provides:
1. Scene briefs and narration in `story/`.
2. Asset folders for artwork, narration, music, and subtitles.
3. A Python + FFmpeg assembler that turns scene artwork and optional voice recordings into an MP4.
4. A GitHub Actions workflow that can render the video and attach it as a downloadable workflow artifact.

The assembler creates a polished **still-image animatic** with slow camera movement, scene transitions, narration, optional music, and subtitles. It does not generate new AI animation or artwork by itself. Create or draw the scene images with a free tool, then add them to `assets/images/`. For genuine character animation, use free Blender projects and render the clips into `assets/clips/`; the assembler can use those clips instead of still images.

## Quick start
Requirements: Python 3.10+ and FFmpeg.

```bash
python -m pip install -r requirements.txt
python scripts/render_video.py
```

Output: `output/the-world-through-my-eyes.mp4`

### Add assets
- Still images: `assets/images/scene-01.jpg` through `scene-07.jpg`
- Optional rendered video clips: `assets/clips/scene-01.mp4` through `scene-07.mp4` (clips take priority over stills)
- Optional narration: `assets/audio/narration.wav`
- Optional background music: `assets/audio/music.mp3`
- Subtitles: edit `story/subtitles.srt`

If images or clips are missing, the script reports which files are needed and exits without pretending a finished film was rendered.

## GitHub Actions
Open **Actions → Render short film → Run workflow**. The rendered MP4 is uploaded as an artifact when the required scene assets have been committed to the repository.

## Respect and privacy
Only add images, voices, and personal details that you have permission to use. If the story is based on a real child, keep identifying details private unless the family has explicitly approved sharing them.