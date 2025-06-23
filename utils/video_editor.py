#Written By: Michael Carson 
# utils/video_editor.py

import os
from moviepy.editor import VideoFileClip

def create_clips(video_path, clip_ranges, output_dir="clips"):
    os.makedirs(output_dir, exist_ok=True)

    clip_paths = []

    for i, (start, end) in enumerate(clip_ranges, 1):
        print(f"✂️  Clipping from {start:.2f}s to {end:.2f}s...")

        # Load only the needed subclip (saves time)
        clip = VideoFileClip(video_path).subclip(start, end)

        # Save path
        filename = f"clip_{i:03d}.mp4"
        output_path = os.path.join(output_dir, filename)

        # Write the clip to disk
        clip.write_videofile(output_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)

        print(f"✅ Saved: {output_path}")
        clip_paths.append(output_path)

    return clip_paths

