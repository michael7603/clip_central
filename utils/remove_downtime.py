import os
from moviepy.editor import VideoFileClip, concatenate_videoclips

def remove_downtime(video_path, downtime_segments, output_path="cleaned_output.mp4"):
    print("📼 Loading video...")
    video = VideoFileClip(video_path)
    duration = video.duration

    print("⏳ Calculating non-downtime segments...")
    # Calculate inverse (non-downtime) segments
    good_segments = []
    prev_end = 0

    for start, end in sorted(downtime_segments):
        if start > prev_end:
            good_segments.append((prev_end, start))
        prev_end = max(prev_end, end)

    # Add final tail segment if video doesn't end in downtime
    if prev_end < duration:
        good_segments.append((prev_end, duration))

    if not good_segments:
        print("⚠️ No content to keep — all video is considered downtime.")
        return None

    print(f"🎬 Extracting {len(good_segments)} non-downtime segment(s)...")
    clips = [video.subclip(start, end) for start, end in good_segments]

    print("🔗 Concatenating clips...")
    final_clip = concatenate_videoclips(clips)

    print(f"💾 Writing output to: {output_path}")
    final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac")

    return output_path
