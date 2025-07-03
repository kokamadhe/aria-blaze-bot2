import os
import logging
import threading
from aiogram import Bot, Dispatcher, executor, types
from flask import Flask

# Set up logging
logging.basicConfig(level=logging.INFO)

# Flask app for Render's web service detection
web_app = Flask(__name__)

@web_app.route("/")
def home():
    return "Aria Blaze is running on Render!"

# Load environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in environment variables.")

# Set up bot
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# Example command handler
@dp.message_handler(commands=["start", "help"])
async def start_handler(message: types.Message):
    await message.reply("🔥 Hello! I'm Aria Blaze. I'm live and ready to chat!")

# Optional custom command
@dp.message_handler(commands=["moan"])
async def moan_handler(message: types.Message):
    await message.reply("Ahh~ 💦")

# Start Flask app in separate thread
def run_web():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    executor.start_polling(dp, skip_updates=True)


