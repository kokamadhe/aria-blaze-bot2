import os
from aiogram import Bot, Dispatcher, executor, types
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Aria Blaze is running!"

# Your bot code
API_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def start_cmd(message: types.Message):
    await message.reply("Hi! I'm Aria Blaze.")

if __name__ == "__main__":
    import threading
    threading.Thread(target=lambda: app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))).start()
    executor.start_polling(dp, skip_updates=True)

