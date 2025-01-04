from flask import Flask, request, jsonify
from tiktok_uploader.tiktok import upload_video  # Adjust this import if necessary based on repo structure

app = Flask(__name__)

# Secure API key
API_KEY = "A9vX3kL5T7N8qW2pJ6M4R1yZ0C"

@app.route('/upload', methods=['POST'])
def upload():
    # Validate API key
    if request.headers.get("Authorization") != f"Bearer {API_KEY}":
        return jsonify({"error": "Unauthorized"}), 401

    # Check if a video file was provided
    video_file = request.files.get('file')
    if not video_file:
        return jsonify({"error": "No video file provided"}), 400

    # Save the file to a temporary location
    video_path = f"/tmp/{video_file.filename}"
    video_file.save(video_path)

    # Attempt to upload the video to TikTok
    try:
        response = upload_video(video_path)  # Ensure this function exists in the TikTok uploader
        return jsonify({"message": "Video uploaded successfully", "response": response}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
