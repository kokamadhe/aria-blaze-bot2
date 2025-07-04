import os
from flask import Flask, request, abort
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
import asyncio

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is missing!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

app = Flask(__name__)

@app.route("/")
def home():
    return "Aria Blaze Bot is running!"

@app.route("/webhook", methods=["POST"])
def webhook():
    if request.content_type != "application/json":
        abort(400)
    update = types.Update(**request.json)
    asyncio.run(dp.process_update(update))
    return "", 200

# Example handler: reply "Hello!" to any text message
@dp.message_handler()
async def echo_message(message: types.Message):
    await message.reply("Hello!")

if __name__ == "__main__":
    # For local testing only, Render uses gunicorn so this is not used in deploy
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
s







