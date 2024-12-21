from flask import Flask, request
import datetime

app = Flask(__name__)

@app.route('/track_open', methods=['GET'])
def track_open():
    email = request.args.get('email')
    with open('logs/email_opens.txt', 'a') as f:
        f.write(f"Email opened by: {email} at {datetime.datetime.now()}\n")
    return b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\xf0\x00\x00\xff\xff\xff\x00\x00\x00!\xf9\x04\x01\x00\x00\x00\x00,\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02\x44\x01\x00;'

if __name__ == "__main__":
    app.run(port=5000)
