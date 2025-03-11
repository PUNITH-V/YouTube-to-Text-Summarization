import yt_dlp
import subprocess
import os

def download_youtube_mp3(url, output_path=None):
    output_template = f'{output_path}/%(title)s.%(ext)s' if output_path else '%(title)s.%(ext)s'
    
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
            info = ydl.extract_info(url, download=True)
            mp3_file = ydl.prepare_filename(info).replace('.webm', '.mp3').replace('.m4a', '.mp3')
        
        print(f"MP3 download completed: {mp3_file}")
        return mp3_file
        
    except Exception as e:
        print(f"An error occurred while downloading MP3: {str(e)}")
        return None

def convert_mp3_to_wav(mp3_file):
    if not os.path.exists(mp3_file):
        print("MP3 file not found.")
        return None
    
    wav_file = mp3_file.replace('.mp3', '.wav')
    
    try:
        command = ['ffmpeg', '-i', mp3_file, wav_file, '-y']
        subprocess.run(command, check=True)
        print(f"Conversion to WAV completed: {wav_file}")
        return wav_file
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while converting to WAV: {e}")
        return None

if __name__ == "_main_":
    video_url = input("Enter YouTube URL: ")
    mp3_file = download_youtube_mp3(video_url)
    
    if mp3_file:
        wav_file = convert_mp3_to_wav(mp3_file)
        if wav_file:
            print(f"Final WAV file: {wav_file}")
        else:
            print("WAV conversion failed.")
    else:
        print("MP3 download failed.")