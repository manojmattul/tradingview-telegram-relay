from flask import Flask, request
import requests
import os
import json

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        raw = request.get_data(as_text=True)
        print(f"Received raw: {raw}")

        # Clean the message - remove anything before first {
        if "{" in raw:
            raw = raw[raw.index("{"):]

        try:
            data = json.loads(raw)
            text = data.get("message", raw)
        except Exception as parse_err:
            print(f"JSON parse error: {parse_err}")
            # Fallback: try to extract message= value
            if "message=" in raw:
                text = raw.split("message=")[-1]
            else:
                text = raw

        print(f"Sending to Telegram: {text}")

        resp = requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text},
            timeout=10
        )
        print(f"Telegram response: {resp.status_code} {resp.text}")
        return "OK", 200

    except Exception as e:
        print(f"Error: {e}")
        return "Error", 500

@app.route("/", methods=["GET"])
def home():
    return "Relay server is running!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
