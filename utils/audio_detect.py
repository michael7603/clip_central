#detects audio spikes to clip notable moments 
#rates clips based on avg audio level / length of clip 


import librosa
import numpy as np
from moviepy.editor import VideoFileClip
import os

def detect_audio_spikes(
    video_path, threshold=0.9, pre_clip=90, post_wait=15, window_size=1.0
):
    print(" Loading audio for analysis...")

    # Load video and extract audio
    clip = VideoFileClip(video_path)
    audio = clip.audio

    # Save audio to temporary file
    temp_audio_path = "temp_audio.wav"
    audio.write_audiofile(temp_audio_path, verbose=False, logger=None)

    # Load audio using librosa
    y, sr = librosa.load(temp_audio_path)
    os.remove(temp_audio_path)

    # Calculate short-term energy (volume)
    frame_len = int(sr * window_size)
    energy = np.array([
        sum(abs(y[i:i+frame_len]**2))
        for i in range(0, len(y), frame_len)
    ])

    # Normalize to 0–1
    energy = energy / np.max(energy)

    # Detect spikes > 90%
    spike_indices = np.where(energy > threshold)[0]
    spike_seconds = [i * window_size for i in spike_indices]

    print(f" Detected {len(spike_seconds)} spike(s) above {threshold*100:.0f}% volume.")

    # Create raw clip ranges (start 90s before, end 15s after)
    raw_ranges = []
    for spike_time in spike_seconds:
        start = max(0, spike_time - pre_clip)
        end = spike_time + post_wait
        raw_ranges.append((start, end))

    # Merge overlapping/nearby clips
    merged_ranges = merge_overlapping_ranges(raw_ranges)

    # Rate each clip by avg volume in that window
    rated_clips = []
    for start, end in merged_ranges:
        start_idx = int(start // window_size)
        end_idx = int(end // window_size)
        avg_rating = float(np.mean(energy[start_idx:end_idx]))
        rated_clips.append({
            "start": round(start, 2),
            "end": round(end, 2),
            "rating": round(avg_rating, 3)
        })

    return rated_clips


def merge_overlapping_ranges(ranges, buffer=5):
    """Merge overlapping or nearby (within `buffer` seconds) clip ranges."""
    if not ranges:
        return []

    ranges.sort()
    merged = [ranges[0]]

    for current in ranges[1:]:
        prev_start, prev_end = merged[-1]
        curr_start, curr_end = current

        if curr_start <= prev_end + buffer:
            merged[-1] = (prev_start, max(prev_end, curr_end))
        else:
            merged.append(current)

    return merged




