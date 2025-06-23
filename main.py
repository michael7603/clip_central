#Written By: Michael Carson 2025
#Contains all the main functions required to import, clip, export 
from utils.download import download_video
from utils.audio_detect import detect_audio_spikes
from utils.video_editor import clip_video

# === User Input ===
video_url = input("Paste the video URL: ").strip()
clip_duration = float(input("Clip duration in seconds (e.g. 5, 10): "))

# === Step 1: Download the Video ===
print("\n Downloading video...")
video_path = download_video(video_url)

# === Step 2: Analyze Audio for Spikes ===
print("\n Detecting audio spikes...")
spike_times = detect_audio_spikes(video_path, chunk_duration=600)  # 10-minute chunks

if not spike_times:
    print(" No spikes found. Try lowering the threshold or check audio quality.")
else:
    print(f"Found {len(spike_times)} highlight-worthy moments.")

# === Step 3: Create Clips ===
print("\n✂️ Creating highlight clips...")
clip_video(video_path, spike_times, clip_length=clip_duration)

print("\n Done! All clips saved in the 'clips/' folder.")
