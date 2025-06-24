import os
import cv2
import numpy as np
from moviepy.editor import VideoFileClip, clips_array
import cvlib as cv

def detect_face_bounds_multi_frames(video_path, sample_times=[3, 5, 7]):
    clip = VideoFileClip(video_path)
    height = clip.h
    candidate_bounds = []

    for t in sample_times:
        if t >= clip.duration:
            continue
        frame = clip.get_frame(t)
        faces, _ = cv.detect_face(frame)

        if not faces:
            continue

        largest_face = max(faces, key=lambda box: (box[2]-box[0]) * (box[3]-box[1]))
        x1, y1, x2, y2 = largest_face

        pad = 30
        y1 = max(0, y1 - pad)
        y2 = min(height, y2 + pad)
        candidate_bounds.append((y1, y2))

    if not candidate_bounds:
        return None

    avg_y1 = int(np.mean([b[0] for b in candidate_bounds]))
    avg_y2 = int(np.mean([b[1] for b in candidate_bounds]))
    return (avg_y1, avg_y2)

def create_clips_with_facecam(video_path, clip_ranges, output_dir="clips"):
    os.makedirs(output_dir, exist_ok=True)
    clip_paths = []

    face_bounds = detect_face_bounds_multi_frames(video_path)

    for i, (start, end) in enumerate(clip_ranges, 1):

        print(f"✂️  Clipping from {start:.2f}s to {end:.2f}s...")

        clip = VideoFileClip(video_path).subclip(start, end)

        short_width = 1080
        short_height = 1920

        if face_bounds:
            y1, y2 = face_bounds

            gameplay_clip = clip.crop(y1=0, y2=y1).resize(height=960)
            facecam_clip = clip.crop(y1=y1, y2=y2).resize(height=960)

            gameplay_clip = gameplay_clip.resize(width=short_width)
            facecam_clip = facecam_clip.resize(width=short_width)

            final_clip = clips_array([[gameplay_clip], [facecam_clip]])
        else:
            clip_resized = clip.resize(width=short_width)
            h = clip_resized.h

            if h < short_height:
                pad_top = (short_height - h) // 2
                clip_resized = clip_resized.margin(top=pad_top, bottom=pad_top, color=(0, 0, 0))
            elif h > short_height:
                clip_resized = clip_resized.crop(y_center=h // 2, height=short_height)

            final_clip = clip_resized

        filename = f"clip_{i:03d}.mp4"
        output_path = os.path.join(output_dir, filename)
        final_clip.write_videofile(output_path, codec="libx264", audio_codec="aac", verbose=False, logger=None)

        print(f" ✅ Saved: {output_path}")
        clip_paths.append(output_path)

    return clip_paths
