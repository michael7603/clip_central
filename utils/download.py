#Written By: Michael Carson 
import yt_dlp
import os
import hashlib

def download_video(url, output_dir="media"):
    os.makedirs(output_dir, exist_ok=True)

    # Create a unique filename based on the URL hash
    video_id = hashlib.md5(url.encode()).hexdigest()[:8]
    filename = f"video_{video_id}.mp4"
    output_path = os.path.join(output_dir, filename)

    # Skip download if file already exists
    if os.path.exists(output_path):
        print(f" Video already downloaded at: {output_path}")
        return output_path

    # Set yt-dlp options
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'outtmpl': output_path,
        'quiet': False,
        'merge_output_format': 'mp4'
    }

    # Download the video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    print(f" Downloaded to: {output_path}")
    return output_path
