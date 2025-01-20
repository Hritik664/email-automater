from flask import Flask, request, send_file, jsonify
from datetime import datetime
import os

# Initialize Flask app
app = Flask(__name__)

# Ensure logs directory exists
LOGS_DIR = "logs"
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

EMAIL_LOG_FILE = os.path.join(LOGS_DIR, "email_opens.txt")

@app.route("/track_open", methods=["GET"])
def track_open():
    tracking_id = request.args.get("tracking_id")
    if not tracking_id:
        return jsonify({"error": "Tracking ID is missing"}), 400

    # Log the event
    log_entry = f"[{datetime.now()}] Tracking ID opened: {tracking_id}\n"
    with open(EMAIL_LOG_FILE, "a") as log_file:
        log_file.write(log_entry)

    # Return a transparent pixel
    return send_file("1x1.png", mimetype="image/png", conditional=True)

@app.route("/download_logs", methods=["GET"])
def download_logs():
    if os.path.exists(EMAIL_LOG_FILE):
        return send_file(EMAIL_LOG_FILE, as_attachment=True)
    else:
        return jsonify({"error": "No logs found"}), 404

# Ensure a transparent pixel exists
if not os.path.exists("1x1.png"):
    from PIL import Image
    img = Image.new("RGBA", (1, 1), (255, 255, 255, 0))
    img.save("1x1.png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
