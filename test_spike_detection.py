from utils.download import download_video
from utils.audio_detect import detect_audio_spikes

# Step 1: Ask user for a URL
url = input("🎥 Enter a YouTube URL to analyze: ")

# Step 2: Download the video using your existing function
video_path = download_video(url)

# Step 3: Analyze the downloaded video file
clips = detect_audio_spikes(video_path)

# Step 4: Optional – print returned clip data again
print("\nReturned clip data:")
for clip in clips:
    print(clip)
