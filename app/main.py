from flask import Flask, render_template, request, jsonify, url_for
import os
import yt_dlp
from datetime import datetime

flask_app = Flask(__name__, template_folder="templates", static_folder="../static")

AUDIO_FILES_DIR = os.path.join(flask_app.static_folder, "audio_files")
os.makedirs(AUDIO_FILES_DIR, exist_ok=True)  

@flask_app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')  

def download_youtube_wav(url: str) -> str | None:
    """Download YouTube video and convert to optimized WAV format for ASR."""
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '0',  # Highest quality for PCM
        }],
        'postprocessor_args': [
            '-ac', '1',          # Mono audio (better for ASR)
            '-ar', '16000',       # 16kHz sample rate (standard for speech)
            '-sample_fmt', 's16', # 16-bit PCM (best for ASR)
        ],
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
            info_dict = ydl.extract_info(url, download=False)
            if not info_dict:
                return None

            video_title = info_dict.get('title', f"audio_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            filename = f"{video_title}.wav"
            final_path = os.path.join(AUDIO_FILES_DIR, filename)

            # Skip if file already exists
            if os.path.exists(final_path):
                return filename

            options['outtmpl'] = os.path.join(AUDIO_FILES_DIR, f"{video_title}.%(ext)s")
            with yt_dlp.YoutubeDL(options) as ydl_download:
                ydl_download.download([url])

            # Verify file was created
            if os.path.exists(final_path):
                print(f"✅ Downloaded: {filename} ({os.path.getsize(final_path)/1024/1024:.1f}MB)")
                return filename
            return None

    except Exception as e:
        print(f"⚠ Error: {str(e)}")
        return None

@flask_app.route('/extract', methods=['POST'])
def extract_audio():
    """Extract optimized audio from YouTube video URL."""
    video_url = request.json.get('video_url')
    if not video_url:
        return jsonify({"status": "error", "message": "No video URL provided."})

    if filename := download_youtube_wav(video_url):
        audio_url = url_for('static', filename=f"audio_files/{filename}")
        return jsonify({
            "status": "success",
            "audio_url": audio_url,
            "message": "Audio optimized for ASR (16kHz mono 16-bit WAV)"
        })

    return jsonify({"status": "error", "message": "Failed to extract audio. Please check the YouTube URL."})

if __name__ == '_main_':
    flask_app.run(debug=True)