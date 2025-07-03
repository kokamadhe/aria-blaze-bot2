import os
from flask import Flask, request, Response
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware

API_TOKEN = os.getenv("TELEGRAM_TOKEN")
WEBHOOK_PATH = f"/webhook/{API_TOKEN}"
WEBHOOK_URL_BASE = os.getenv("WEBHOOK_URL_BASE")  # Your Render HTTPS URL like https://yourapp.onrender.com
WEBHOOK_URL = f"{WEBHOOK_URL_BASE}{WEBHOOK_PATH}"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

app = Flask(__name__)

@dp.message_handler(commands=["start", "help"])
async def send_welcome(message: types.Message):
    await message.answer("Hello! I'm your bot running on webhook.")

@dp.message_handler()
async def echo_message(message: types.Message):
    await message.answer(f"You said: {message.text}")

@app.route("/")
def index():
    return "Bot is running!"

@app.route(WEBHOOK_PATH, methods=["POST"])
def webhook():
    if request.content_type == "application/json":
        update = types.Update(**request.get_json())
        # Process update with Aiogram dispatcher
        dp.loop.create_task(dp.process_update(update))
        return Response(status=200)
    else:
        return Response(status=403)

if __name__ == "__main__":
    # Set webhook on startup
    import asyncio

    async def on_startup():
        await bot.set_webhook(WEBHOOK_URL)
        print(f"Webhook set to {WEBHOOK_URL}")

    loop = asyncio.get_event_loop()
    loop.run_until_complete(on_startup())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))




