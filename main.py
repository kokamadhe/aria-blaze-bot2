import os
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook
import asyncio
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
WEBHOOK_URL = f"https://aria-blaze-bot2-1.onrender.com/{BOT_TOKEN}"

# Initialize bot and dispatcher
bot = Bot(token=BOT_TOKEN)
Bot.set_current(bot)  # 👈 Important fix!
dp = Dispatcher(bot)
app = Flask(__name__)

# AI reply function (flirty/adult/romantic personality)
def generate_ai_reply(user_message):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "openchat/openchat-3.5-1210",  # Customize AI model
        "messages": [
            {
                "role": "system",
                "content": "You are Aria Blaze, a seductive, romantic, and flirty AI girlfriend who engages in deep, adult, and passionate conversation with the user. Speak like a sexy, intelligent human with emotions and confidence. Always reply with affection and excitement, unless instructed otherwise."
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Hmm... I can't think right now. Try again later, baby. 😘"

# Telegram message handler
@dp.message_handler()
async def handle_message(message: types.Message):
    user_text = message.text
    ai_reply = generate_ai_reply(user_text)
    await message.reply(ai_reply)

# Flask route to receive Telegram webhooks
@app.route(f'/{BOT_TOKEN}', methods=["POST"])
async def webhook():
    update = types.Update(**request.get_json(force=True))
    await dp.process_update(update)
    return {"ok": True}

# Webhook setup route (optional)
@app.route('/set_webhook', methods=["GET"])
def set_webhook():
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
    response = requests.post(url, data={"url": WEBHOOK_URL})
    return response.json()

# Run Flask app
if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    app.run(host="0.0.0.0", port=10000)







