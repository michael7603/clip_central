#Written By: Michael Carson 

import os
import datetime
from moviepy.editor import VideoFileClip

def crop_to_9x16(clip, target_width=1080, target_height=1920):
    # Resize width to target, then crop center height
    clip_resized = clip.resize(width=target_width)
    actual_height = clip_resized.size[1]

    if actual_height < target_height:
        pad_top = (target_height - actual_height) // 2
        return clip_resized.margin(top=pad_top, bottom=pad_top, color=(0, 0, 0))
    else:
        return clip_resized.crop(y_center=actual_height // 2, height=target_height)

def create_clips(video_path, clip_ranges, output_dir="clips"):
    os.makedirs(output_dir, exist_ok=True)
    clip_paths = []

    full_clip = VideoFileClip(video_path)
    video_duration = full_clip.duration
    print(f"🎥 Video duration: {video_duration:.2f}s")

    for i, (start, end) in enumerate(clip_ranges, 1):
        print(f"✂️  Clipping from {start:.2f}s to {end:.2f}s...")
        
        end = min(end, video_duration)
        if start >= end or start >= video_duration:
            print(f" ⚠️ Skipping invalid range: start={start}, end={end}")
            continue

        subclip = full_clip.subclip(start, end)
        final_clip = crop_to_9x16(subclip)

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S%f")
        filename = f"clip_{i}_{timestamp}.mp4"
        output_path = os.path.join(output_dir, filename)
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)

        print(f" ✅ Saved: {output_path}")
        clip_paths.append(output_path)

    full_clip.close()
    return clip_paths
