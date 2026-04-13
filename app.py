from flask import Flask, request
import requests
import os

app = Flask(__name__)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        message = request.get_data(as_text=True)
        print(f"Received: {message}")

        # Try to parse JSON and extract message field
        import json
        try:
            data = json.loads(message)
            text = data.get("message", message)
        except:
            text = message

        requests.post(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            json={"chat_id": CHAT_ID, "text": text}
        )
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
