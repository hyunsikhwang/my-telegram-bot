from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 환경변수에서 텔레그램 토큰을 가져옵니다.
TOKEN = os.environ.get('TELEGRAM_TOKEN')

@app.route('/', methods=['GET'])
def home():
    return "Vercel Python Bot is Running!"

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    if "message" in data:
        chat_id = data["message"]["chat"]["id"]
        text = data["message"].get("text", "")

        # 사용자가 보낸 메시지를 그대로 반사(Echo)
        send_message(chat_id, f"Vercel 봇입니다: {text}")

    return jsonify({"status": "ok"}), 200

def send_message(chat_id, text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": chat_id, "text": text}
    requests.post(url, json=payload)

# Vercel이 이 app 객체를 실행합니다.