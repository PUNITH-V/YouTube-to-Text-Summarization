from flask import render_template, request, jsonify, send_from_directory
from . import flask_app
import os
import yt_dlp
import re
from datetime import datetime

# Constants for file paths
AUDIO_FILES_DIR = os.path.join("static", "audio_files")

def sanitize_filename(title: str) -> str:
    """Sanitize the filename by removing special characters and spaces."""
    return re.sub(r'[-\s]+', '_', re.sub(r'[^\w\s-]', '_', title)).strip('_')

def download_youtube_wav(url: str) -> str | None:
    """Download YouTube video and convert to WAV format.
    
    Args:
        url: YouTube video URL
        
    Returns:
        str: Filename of the downloaded audio, or None if download fails
    """
    os.makedirs(AUDIO_FILES_DIR, exist_ok=True)

    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': os.path.join(AUDIO_FILES_DIR, '%(title)s.%(ext)s'),
        'restrictfilenames': True,
        'noplaylist': True,
        'nocheckcertificate': True,
        'ignoreerrors': False,
        'quiet': True,
        'no_warnings': True
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            # Extract video info
            info_dict = ydl.extract_info(url, download=False)
            if not info_dict:
                return None
            
            # Get video title and sanitize it
            video_title = info_dict.get('title', f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            sanitized_title = sanitize_filename(video_title)
            
            # Update output template and download
            options['outtmpl'] = os.path.join(AUDIO_FILES_DIR, f"{sanitized_title}.%(ext)s")
            with yt_dlp.YoutubeDL(options) as ydl_download:
                ydl_download.download([url])
            
            # Verify the output file exists
            filename = f"{sanitized_title}.wav"
            return filename if os.path.exists(os.path.join(AUDIO_FILES_DIR, filename)) else None
                
    except Exception as e:
        print(f"⚠️ YouTube Download Error: {str(e)}")
        return None

@flask_app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@flask_app.route('/static/audio_files/<path:filename>')
def serve_audio(filename):
    """Serve audio files from the audio directory."""
    return send_from_directory(
        os.path.join(os.path.dirname(os.path.dirname(__file__)), AUDIO_FILES_DIR),
        filename
    )

@flask_app.route('/extract', methods=['POST'])
def extract_audio():
    """Extract audio from YouTube video URL."""
    video_url = request.json.get('video_url')
    if not video_url:
        return jsonify({
            "status": "error",
            "message": "No video URL provided."
        })

    if filename := download_youtube_wav(video_url):
        return jsonify({
            "status": "success",
            "audio_url": f"/static/audio_files/{filename}"
        })

    return jsonify({
        "status": "error",
        "message": "Failed to extract audio. Please make sure the YouTube URL is valid and the video is accessible."
    })
