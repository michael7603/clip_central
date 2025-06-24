from utils.download import download_video
from utils.audio_detect import detect_audio_spikes
from utils.detect_facecam import create_clips_with_facecam
from utils.zoomed_video import create_zoomed_clips
def main():
    url = input("🎥 Enter a YouTube URL to clip: ").strip()
    video_path = download_video(url)

    print("🔍 Analyzing audio for spikes...")
    clip_ranges = detect_audio_spikes(video_path)

    if not clip_ranges:
        print("⚠️ No clips detected.")
        return

       # Extract only (start, end) from each rated clip
    clip_ranges = [(clip["start"], clip["end"]) for clip in clip_ranges]

    print("📦 Creating clips with facecam formatting...")
    clip_paths = create_zoomed_clips(video_path, clip_ranges)

    print(f"✅ {len(clip_paths)} clips saved.")

if __name__ == "__main__":
    main()
