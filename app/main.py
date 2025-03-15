from flask import Flask, render_template, request, jsonify, send_from_directory
from app import flask_app
import os
import requests
import urllib.parse

@flask_app.route('/')
def index():
    return render_template('index.html')

@flask_app.route('/static/audio_files/<filename>')
def serve_audio(filename):
    audio_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "audio_files")
    # URL decode the filename
    decoded_filename = urllib.parse.unquote(filename)
    return send_from_directory(audio_dir, decoded_filename)

@flask_app.route('/extract', methods=['POST'])
def extract_audio():
    video_url = request.json.get('video_url')

    response = requests.post("http://127.0.0.1:8000/extract_audio/", json={"url": video_url})

    if response.status_code == 200:
        audio_url = response.json().get("audio_url")
        # Ensure the audio URL is properly formatted for the frontend
        if audio_url and not audio_url.startswith('/'):
            audio_url = f"/static/audio_files/{os.path.basename(audio_url)}"
        return jsonify({"status": "success", "audio_url": audio_url})

    return jsonify({"status": "error", "message": "Audio extraction failed."})
