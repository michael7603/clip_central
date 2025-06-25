import librosa
import numpy as np
from moviepy.editor import VideoFileClip
import os

def detect_audio_dips(
    video_path, threshold=0.05, min_duration=5.0, window_size=1.0
):
    print("🔍 Loading audio for dip detection...")

    # Extract and save audio
    clip = VideoFileClip(video_path)
    audio = clip.audio
    temp_audio_path = "temp_audio.wav"
    audio.write_audiofile(temp_audio_path, verbose=False, logger=None)

    # Load with librosa
    y, sr = librosa.load(temp_audio_path)
    os.remove(temp_audio_path)

    # Short-term energy calculation
    frame_len = int(sr * window_size)
    energy = np.array([
        sum(abs(y[i:i+frame_len]**2))
        for i in range(0, len(y), frame_len)
    ])

    # Normalize energy to 0–1
    energy = energy / np.max(energy)

    # Detect dips below threshold
    dip_ranges = []
    start_idx = None
    for i, e in enumerate(energy):
        if e < threshold:
            if start_idx is None:
                start_idx = i
        else:
            if start_idx is not None:
                end_idx = i
                duration = (end_idx - start_idx) * window_size
                if duration >= min_duration:
                    dip_ranges.append((start_idx * window_size, end_idx * window_size))
                start_idx = None

    # Catch trailing dip
    if start_idx is not None:
        end_idx = len(energy)
        duration = (end_idx - start_idx) * window_size
        if duration >= min_duration:
            dip_ranges.append((start_idx * window_size, end_idx * window_size))

    print(f"🕳️ Detected {len(dip_ranges)} low-volume segments below {threshold*100:.0f}% volume.")

    for i, (start, end) in enumerate(dip_ranges, 1):
        print(f"  ⏱️ Dip {i}: {start:.2f}s → {end:.2f}s (Duration: {end - start:.2f}s)")

    return dip_ranges
