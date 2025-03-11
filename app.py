import yt_dlp

def download_youtube_video(url, output_path=None, format='best'):
    output_template = f'{output_path}/%(title)s.%(ext)s' if output_path else '%(title)s.%(ext)s'
    
    ydl_opts = {
        'format': format,
        'outtmpl': output_template,
        'noplaylist': True,
        'progress_hooks': [lambda d: print(f"Downloading: {d['_percent_str']} of {d['_total_bytes_str']}") 
                          if d['status'] == 'downloading' else None],
    }
    
    try:
        with yt_dlp.YoutubeDL({'quiet': True}) as ydl:
            info = ydl.extract_info(url, download=False)
            print(f"Title: {info.get('title')}")
            print(f"Duration: {info.get('duration')} seconds")
            print(f"Available formats: {len(info.get('formats', []))} different formats")
        
        print("Starting download...")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print(f"Download completed successfully!")
        return True
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return False

if __name__ == "__main__":
    video_url = input("Enter YouTube video URL: ")
    download_youtube_video(video_url)