import yt_dlp

def download_youtube_mp3(url, output_path=None):
    # Set output location
    output_template = f'{output_path}/%(title)s.%(ext)s' if output_path else '%(title)s.%(ext)s'
    
    # Configure options specifically for MP3 extraction
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_template,
        'noplaylist': True,
    }
    
    try:
        print(f"Downloading and converting to MP3: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print("MP3 download and conversion completed successfully!")
        return True
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    video_url = input("Enter YouTube URL: ")
    download_youtube_mp3(video_url)