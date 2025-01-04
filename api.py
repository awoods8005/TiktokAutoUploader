from flask import Flask, request, jsonify
from tiktok_uploader.tiktok import upload_to_tiktok_wrapper  # Import the wrapper function

app = Flask(__name__)

# Secure API key
API_KEY = "A9vX3kL5T7N8qW2pJ6M4R1yZ0C"

@app.route('/upload', methods=['POST'])
def upload():
    """
    API endpoint to upload videos to TikTok.
    """
    # Validate API key
    if request.headers.get("Authorization") != f"Bearer {API_KEY}":
        return jsonify({"error": "Unauthorized"}), 401

    # Check if a video file was provided
    video_file = request.files.get('file')
    if not video_file:
        return jsonify({"error": "No video file provided"}), 400

    # Check if a username was provided
    username = request.form.get('username')
    if not username:
        return jsonify({"error": "No username provided"}), 400

    # Check if a title was provided
    title = request.form.get('title')
    if not title:
        return jsonify({"error": "No title provided"}), 400

    # Save the file to a temporary location
    video_path = f"/tmp/{video_file.filename}"
    video_file.save(video_path)

    # Attempt to upload the video to TikTok
    response = upload_to_tiktok_wrapper(video_path, username, title)

    # Return the result of the upload
    if response.get("success"):
        return jsonify(response), 200
    else:
        return jsonify(response), 400


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
