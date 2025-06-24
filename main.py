#Written By: Michael Carson 2025
#Contains all the main functions required to import, clip, export 
# main.py

import os
from utils.download import download_video
from utils.audio_detect import detect_audio_spikes
from utils.video_editor import create_clips
from utils.detect_facecam import create_clips_with_facecam

def main():
    # Step 1: Get user input
    url = input("🎥 Enter a YouTube URL to clip: ")

    # Step 2: Download the video
    video_path = download_video(url)

    # Step 3: Detect loud segments
    rated_clips = detect_audio_spikes(video_path)

    # Step 4: Convert to (start, end) pairs
    clip_ranges = [(clip["start"], clip["end"]) for clip in rated_clips]

    # Step 5: Generate and save clips
    output_dir = "clips"
    created_files = create_clips(video_path, clip_ranges, output_dir=output_dir)

    # Step 6: Summary
    print(f"\n🎬 {len(created_files)} clips saved to '{output_dir}/' folder.")
    for path in created_files:
        print(f" - {path}")

if __name__ == "__main__":
    main()
