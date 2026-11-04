import os
from flask import Flask, render_template, request, jsonify, send_file
from clipping import fetch_youtube_data
from reels import parse_instagram_input, generate_reel_ai_pack
from scheduler import get_next_slot
from youtube_auth import upload_short_to_youtube

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api/fetch-youtube", methods=["POST"])
def api_fetch_youtube():
    data = request.json
    url = data.get("url")
    result = fetch_youtube_data(url)
    return jsonify(result)

@app.route("/api/fetch-reels", methods=["POST"])
def api_fetch_reels():
    data = request.json
    url = data.get("url")
    reels = parse_instagram_input(url)
    ai_pack = generate_reel_ai_pack(reels)
    return jsonify({"reels": reels, "ai_pack": ai_pack})

@app.route("/api/schedule", methods=["POST"])
def api_schedule():
    data = request.json
    mode = data.get("mode") # 'mode_1_clipping' or 'mode_2_reels'
    custom_time = data.get("custom_time")
    upload_now = data.get("upload_now", False)
    
    slot = get_next_slot(mode, custom_time_str=custom_time, upload_now=upload_now)
    return jsonify({"scheduled_time": slot})

@app.route("/api/upload-youtube", methods=["POST"])
def api_upload_youtube():
    data = request.json
    video_path = data.get("video_path")
    title = data.get("title")
    description = data.get("description", "")
    tags = data.get("tags", ["Shorts"])
    publish_iso = data.get("publish_iso")
    
    try:
        video_id = upload_short_to_youtube(video_path, title, description, tags, publish_iso)
        return jsonify({"success": True, "video_id": video_id})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
