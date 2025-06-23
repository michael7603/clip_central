#Written By: Michael Carson 2025
#Contains all the main functions required to import, clip, export 
# main.py

import os
from utils.download import download_video
from utils.audio_detect import detect_audio_spikes
from utils.video_editor import create_clips
# from utils.whisper import transcribe_clip  # Optional

def main():
    print(" CLIP CENTRAL - Automated Clipping Tool\n")

    # Step 1: Input video source
    video_input = input(" Input the video URL or local file path: ").strip()

    # Step 2: Download if it's a URL
    if video_input.startswith("http"):
        print("\n⬇  Downloading video...")
        video_path = download_video(video_input)
    else:
        print("\n Using local video file.")
        video_path = video_input

    print(f" Video ready: {video_path}")

    # Step 3: Analyze audio for spikes
    print("\n Analyzing audio for highlights...")
    timestamps = detect_audio_spikes(video_path)
    print(f" Found {len(timestamps)} spike(s) at: {timestamps}")

    # Step 4: Create video clips
    print("\n✂️  Creating video clips...")
    clips = create_clips(video_path, timestamps)
    print(f" Created {len(clips)} clip(s):")
    for clip in clips:
        print(f"   - {clip}")

    # Step 5: Auto-save clips to output folder
    print("\n All clips saved to the 'clips/' folder.")
    print(" Done! Ready to share your content!")

if __name__ == "__main__":
    main()
