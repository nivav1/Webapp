from flask import Blueprint, request, jsonify, send_file
from pytubefix import YouTube
from pathlib import Path
import os

yt_blueprint = Blueprint('ytDownloader', __name__)


@yt_blueprint.route('/download', methods=['POST'])
def download():
    try:
        data = request.get_json()
        yt_get = data.get('youtube_get')
        if not yt_get:
            return jsonify({"error": "YouTube URL Address is required"}), 400

        if not ('youtube.com' in yt_get or 'youtu.be' in yt_get):
            return jsonify({"error": "Invalid YouTube URL"}), 400

        downloads_path = Path.home() / 'Downloads'
        downloads_path.mkdir(parents=True, exist_ok=True)

        yt = YouTube(yt_get)
        yd = yt.streams.get_highest_resolution()
        downloaded_file = yd.download(output_path=str(downloads_path))

        title = yt.title.replace('"', "'").replace('|', '-')
        response = send_file(
            downloaded_file,
            as_attachment=True,
            download_name=f"{title}.mp4",
            mimetype='video/mp4'
        )
        os.remove(downloaded_file)  # Clean up
        return response
    except Exception as e:
        return jsonify({"error": str(e)}), 500
