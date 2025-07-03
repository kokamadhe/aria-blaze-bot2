import os
from flask import Flask, request
from aiogram import Bot, Dispatcher, executor, types
import logging

# Enable logging
logging.basicConfig(level=logging.INFO)

# Bot token from environment variable (make sure to set this in Render's dashboard)
API_TOKEN = os.getenv("TELEGRAM_TOKEN")

if not API_TOKEN:
    raise RuntimeError("TELEGRAM_TOKEN environment variable is missing")

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Flask app
app = Flask(__name__)

# Simple route for Render healthcheck or browser visit
@app.route("/", methods=["GET"])
def index():
    return "Aria Blaze Bot is running!"

# Telegram message handler example
@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.reply("Hello! I am Aria Blaze Bot. How can I help you?")

# Add your other handlers here...

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    # Run Flask app on all interfaces with port from Render or default 10000
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Start Flask app in a separate thread or process if needed
    # But simplest here is just to run Flask and Aiogram polling concurrently

    import threading

    # Run Flask in background thread
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.start()

    # Start Aiogram polling (Telegram bot)
    executor.start_polling(dp, skip_updates=True)



