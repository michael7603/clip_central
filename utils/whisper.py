# utils/whisper.py

import whisper
import os

# Load model once
model = whisper.load_model("base")  # or "small", "medium", etc.

def transcribe_clip(clip_path):
    print(f"📝 Transcribing {os.path.basename(clip_path)}...")
    result = model.transcribe(clip_path)
    transcript = result["text"].strip()
    print(f"🗣 Transcript: {transcript[:60]}{'...' if len(transcript) > 60 else ''}")
    return transcript
