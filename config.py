# config.py

# Percentile threshold for audio spikes (higher = fewer clips)
AUDIO_THRESHOLD_PERCENTILE = 90

# Minimum seconds between clips to avoid duplicates
CLIP_MIN_GAP = 30

# Default chunk size in seconds for long videos (10 mins)
CHUNK_DURATION = 600  # 600 seconds = 10 minutes

# Default output folders (can be changed in main if needed)
CLIPS_DIR = "clips"
MEDIA_DIR = "media"
