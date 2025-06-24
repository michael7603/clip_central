import os
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

def create_zoomed_clips(video_path, clip_ranges, output_dir="clips_zoomed"):
    os.makedirs(output_dir, exist_ok=True)
    clip_paths = []

    for i, (start, end) in enumerate(clip_ranges, 1):
        print(f"🔍 Zooming + clipping from {start:.2f}s to {end:.2f}s...")

        clip = VideoFileClip(video_path).subclip(start, end)

        # Zoom in by 25%
        zoomed_clip = clip.resize(1.25)

        # Convert to 9:16 short format
        final_clip = crop_to_9x16(zoomed_clip)

        # Save
        filename = f"zoomed_clip_{i:03d}.mp4"
        output_path = os.path.join(output_dir, filename)
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)

        print(f" ✅ Saved: {output_path}")
        clip_paths.append(output_path)

    return clip_paths
