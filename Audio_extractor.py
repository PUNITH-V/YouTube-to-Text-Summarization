import yt_dlp

# Function to download YouTube audio as WAV
def download_youtube_wav(url):
    print("Starting download...")
    
    # Setup options for downloading
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',  # Set format to WAV
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
    }
    
    # Try to download
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        print("Download complete! WAV file saved.")
    except Exception as e:
        print(f"Error: {e}")

# Get YouTube URL from user
video_url = input("Enter YouTube URL: ")

# Download the video as WAV
download_youtube_wav(video_url)