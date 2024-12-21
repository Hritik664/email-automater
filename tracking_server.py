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

@app.route("/")
def home():
    return jsonify({"status": "Server is running"}), 200

@app.route("/track/<email_id>.png")
def track_email(email_id):
    """
    Tracks email opens via a tracking pixel.
    - Logs the email ID, timestamp, and request metadata.
    """
    # Log the event
    with open(EMAIL_LOG_FILE, "a") as log_file:
        log_entry = f"[{datetime.now()}] Email opened: {email_id}\n"
        log_file.write(log_entry)
        print(log_entry.strip())  # For debugging locally or on Render logs

    # Send a 1x1 transparent pixel
    return send_file(
        "1x1.png",  # Use an actual 1x1 transparent image
        mimetype="image/png",
        conditional=True
    )

@app.route("/logs", methods=["GET"])
def get_logs():
    """
    Returns the log file containing tracked email opens.
    """
    if os.path.exists(EMAIL_LOG_FILE):
        with open(EMAIL_LOG_FILE, "r") as log_file:
            logs = log_file.read()
        return jsonify({"logs": logs}), 200
    else:
        return jsonify({"error": "No logs found"}), 404

@app.route("/download_logs", methods=["GET"])
def download_logs():
    """
    Endpoint to download the email opens log file.
    """
    if os.path.exists(EMAIL_LOG_FILE):
        return send_file(EMAIL_LOG_FILE, as_attachment=True)
    else:
        return jsonify({"error": "No logs found"}), 404

# Ensure a 1x1 transparent image exists
if not os.path.exists("1x1.png"):
    from PIL import Image
    img = Image.new("RGBA", (1, 1), (255, 255, 255, 0))  # Transparent pixel
    img.save("1x1.png")

# Run the server
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Render uses $PORT; locally defaults to 5000
    app.run(host="0.0.0.0", port=port)
