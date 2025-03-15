import yt_dlp


def download_youtube_wav(url):
    print("Starting download...")
    
    
    options = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',  
            'preferredquality': '192',
        }],
        'outtmpl': '%(title)s.%(ext)s',
    }
    
    
    try:
        with yt_dlp.YoutubeDL(options) as ydl:
            ydl.download([url])
        print("Download complete! WAV file saved.")
    except Exception as e:
        print(f"Error: {e}")


video_url = input("Enter YouTube URL: ")


download_youtube_wav(video_url)