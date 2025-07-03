import os
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def reply(message: types.Message):
    user_input = message.text
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    }
    data = {
        "model": "openai/gpt-3.5-turbo",
        "messages": [{"role": "user", "content": user_input}]
    }
    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
    reply_text = response.json()["choices"][0]["message"]["content"]
    await message.reply(reply_text)

if __name__ == "__main__":
    executor.start_polling(dp)
