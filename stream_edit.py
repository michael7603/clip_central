import os
import uuid
from utils.download import download_video
from utils.detect_audio_dips import detect_audio_dips
from utils.remove_downtime import remove_downtime

def main():
    # Step 1: Get user input
    url = input("🎥 Enter a YouTube URL to clean: ")

    # Step 2: Download the video
    video_path = download_video(url)

    # Step 3: Detect quiet (downtime) segments
    downtime_segments = detect_audio_dips(
        video_path,
        threshold=0.05,
        min_duration=5.0,
        window_size=1.0
    )

    # Step 4: Create output directory
    output_dir = "stream_cleaned"
    os.makedirs(output_dir, exist_ok=True)

    # Step 5: Generate random filename
    random_name = f"{uuid.uuid4().hex[:8]}.mp4"
    output_path = os.path.join(output_dir, random_name)

    # Step 6: Remove downtime and save cleaned video
    result = remove_downtime(video_path, downtime_segments, output_path)

    # Step 7: Final message
    if result:
        print(f"\n✅ Cleaned video saved to: {result}")
    else:
        print("\n❌ No valid content found to keep. Adjust dip threshold or check source.")

if __name__ == "__main__":
    main()

