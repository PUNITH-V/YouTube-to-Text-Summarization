import yt_dlp
import subprocess
import os

def download_youtube_audio_as_wav(url, output_path=None):
    # Step 1: Download audio using yt_dlp (in best format)
    output_template = f'{output_path}/%(title)s.%(ext)s' if output_path else '%(title)s.%(ext)s'
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_template,
        'noplaylist': True,
    }
    
    try:
        print(f"Downloading audio from: {url}")
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            audio_file = ydl.prepare_filename(info)
        
        # Step 2: Convert to WAV using ffmpeg
        wav_file = audio_file.rsplit('.', 1)[0] + '.wav'
        command = ['ffmpeg', '-i', audio_file, wav_file, '-y']
        subprocess.run(command, check=True)
        
        # Step 3: Remove original audio file after conversion
        os.remove(audio_file)
        
        print(f"WAV download and conversion completed: {wav_file}")
        return wav_file
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

if __name__ == "_main_":
    video_url = input("Enter YouTube URL: ")
    wav_file = download_youtube_audio_as_wav(video_url)
    
    if wav_file:
        print(f"Final WAV file: {wav_file}")
    else:
        print("WAV download failed.")