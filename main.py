import os
import requests
from flask import Flask, request
from aiogram import Bot, Dispatcher, types
from aiogram.utils.executor import start_webhook

# Load environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

app = Flask(__name__)

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

# Webhook settings
WEBHOOK_PATH = f'/{TELEGRAM_TOKEN}'
WEBHOOK_URL = f'https://aria-blaze-bot2.onrender.com{WEBHOOK_PATH}'  # Your Render URL
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.environ.get('PORT', 5000))


# OpenRouter AI chat
def ask_openrouter(message_text):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "openrouter/chatgpt",  # Or any other available model
        "messages": [
            {"role": "system", "content": "You are Aria Blaze, an AI chatbot."},
            {"role": "user", "content": message_text}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return "Sorry, I couldn't process that."


@dp.message_handler()
async def handle_message(message: types.Message):
    reply = ask_openrouter(message.text)
    await message.answer(reply)


@app.route("/", methods=["GET"])
def index():
    return "Bot is live!"


@app.route(WEBHOOK_PATH, methods=["POST"])
async def webhook():
    update = types.Update.de_json(request.get_json(force=True))
    await dp.process_update(update)
    return "ok"


async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL)


async def on_shutdown(dp):
    await bot.delete_webhook()


if __name__ == "__main__":
    from aiogram import executor
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=True,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )





