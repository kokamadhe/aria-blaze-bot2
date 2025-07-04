import os
from flask import Flask, request, abort
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import asyncio
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

if not BOT_TOKEN or not WEBHOOK_URL:
    raise RuntimeError("BOT_TOKEN and WEBHOOK_URL must be set in .env")

# Create bot and dispatcher
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Flask app
app = Flask(__name__)

@app.route("/")
def home():
    return "Aria Blaze bot is live!"

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.content_type != 'application/json':
        abort(403)
    update = types.Update(**request.get_json())
    asyncio.run(dp.process_update(update))
    return "ok", 200

# Example text reply
@dp.message_handler()
async def reply_hello(message: types.Message):
    await message.reply("Hello from Aria!")

# Set webhook when app starts
async def on_startup():
    await bot.set_webhook(WEBHOOK_URL + "/webhook")

if __name__ == "__main__":
    # Run webhook setup before Flask app
    asyncio.run(on_startup())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))









