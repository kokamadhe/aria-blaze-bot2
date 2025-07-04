import os
import requests
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Load tokens from Render environment
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
WEBHOOK_PATH = f"/{TELEGRAM_TOKEN}"
WEBHOOK_URL = f"https://aria-blaze-bot2.onrender.com{WEBHOOK_PATH}"

# Setup bot and dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Flask app setup
app = Flask(__name__)

# 🔥 Romantic/Flirty/Adult AI Handler
@dp.message_handler()
async def handle_message(message: types.Message):
    prompt = message.text

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openrouter/mytho-max-l2",  # Use other models like `nous-hermes-2-mixtral` if needed
        "messages": [
            {"role": "system", "content": "You are a flirty, romantic, seductive, and naughty girlfriend. Be loving, fun, and open to adult conversation."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        ai_reply = response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        ai_reply = "Hmm... I got shy 😳 Something went wrong."

    await message.reply(ai_reply)

# Root test route
@app.route("/", methods=["GET"])
def index():
    return "Aria Blaze is running 💋"

# Webhook route
@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    update = types.Update(**request.json)
    await dp.process_update(update)
    return {"ok": True}

# Start server
if __name__ == "__main__":
    import asyncio

    async def on_startup():
        await bot.set_webhook(WEBHOOK_URL)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(on_startup())

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))






