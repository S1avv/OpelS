import aiogram
from aiogram import F, Dispatcher, Bot
from aiogram.types import Message

from chatgpt4_telegram.settings.bot_settings import BOT_TOKEN

import asyncio
import g4f

bot = Bot(token=BOT_TOKEN, parse_mode="Markdown")
dp = Dispatcher()


@dp.message(F.text.startswith("/icc"))
async def reply_message(message: Message):
    user_id = str(message.from_user.id)
    file_path = "chatgpt4_telegram/settings/user_waiting.txt"

    with open(file_path, "r") as file:
        dats = file.read()

    if user_id in dats:
        await message.delete()
        return False

    with open(file_path, "a") as file:
        file.write(str(user_id) + "\n")


    g4f.debug.logging = False
    g4f.debug.version_check = False

    response = await g4f.ChatCompletion.create_async(
        model=g4f.models.gpt_4,
        messages=[{"role": "You are an AI assistant, a large language model trained. Follow the user's instructions carefully. Respond using markdown. My name is ChatGPT", "content": message.text[3:]}],
    )

    await message.reply(text=response.replace("Bing", "OpelS").replace("Source", "Источник").replace("$$", "*").replace("**", "*"))

    with open(file_path, "r") as file:
        lines = file.readlines()

    with open(file_path, "w") as file:
        for line in lines:
            if line.strip() != str(user_id):
                file.write(line)

async def main():
    await bot.delete_webhook(True)
    await dp.start_polling(bot)
    

if __name__ == "__main__":
    asyncio.run(main())