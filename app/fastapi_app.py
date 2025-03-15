from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import yt_dlp
import os
import re

print("🚀 FastAPI is starting...")  # Debugging message

app = FastAPI()

# Mount static files BEFORE any routes
app.mount("/static", StaticFiles(directory="static"), name="static")

class VideoUrl(BaseModel):
    url: str

# Function to sanitize filenames (removes special characters)
def sanitize_filename(title):
    # More thorough filename sanitization
    # Remove or replace problematic characters
    title = re.sub(r'[^\w\s-]', '_', title)
    # Replace multiple spaces/underscores with single underscore
    title = re.sub(r'[-\s]+', '_', title)
    return title.strip('_')

# Function to download and convert YouTube audio to WAV
def download_youtube_wav(url):
    output_dir = "static/audio_files"
    os.makedirs(output_dir, exist_ok=True)

    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
            'preferredquality': '192',
        }],
        'outtmpl': f'{output_dir}/%(title)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            # Extract info first
            info = ydl.extract_info(url, download=False)
            # Sanitize the title before downloading
            sanitized_title = sanitize_filename(info["title"])
            # Update output template with sanitized title
            options['outtmpl'] = f'{output_dir}/{sanitized_title}.%(ext)s'
            
            # Download with updated options
            with yt_dlp.YoutubeDL(options) as ydl2:
                ydl2.download([url])
            
            filename = f"{sanitized_title}.wav"
            file_path = os.path.join(output_dir, filename)

            if os.path.exists(file_path):
                return filename
            else:
                print(f"⚠️ Error: File {file_path} not found after extraction.")
                return None
    except Exception as e:
        print(f"⚠️ YouTube Download Error: {e}")
        return None

@app.get("/")
def home():
    return {"message": "FastAPI is working!"}

@app.post("/extract_audio/")
async def extract_audio(data: VideoUrl):
    filename = download_youtube_wav(data.url)
    
    if filename:
        # Return just the filename, let Flask handle the full path
        return {"audio_url": filename}
    
    return {"error": "Audio extraction failed"}

if __name__ == "__main__":
    import uvicorn
    print("🚀 Starting FastAPI server...")
    uvicorn.run("app.fastapi_app:app", host="127.0.0.1", port=8000, reload=True)


