from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from dotenv import load_dotenv
from yt_dlp import YoutubeDL
import logging
import random, string
import asyncio
import os

load_dotenv()
bot = Bot(os.getenv('TOKEN'))
dp = Dispatcher()


@dp.message(F.text.startswith('https://'))
async def install(message: Message):
    cid = message.chat.id
    text = message.text
    if 'tiktok.com' in text:
        await bot.send_message(cid, 'Видео скачивается, ждите...')
        filehash = ''.join(random.choices(string.ascii_lowercase, k=8))
        ydl_opts = {
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4',
            'outtmpl': f'cache/video{filehash}',  # Задайте путь к папке и имя файла
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([text])
        if os.path.exists(f'cache/video{filehash}'):
            os.rename(f'cache/video{filehash}', f'cache/video{filehash}.mp4')
        await bot.send_video(cid, FSInputFile(f'cache/video{filehash}.mp4'))
        os.remove(f'cache/video{filehash}')

logging.basicConfig(level=logging.INFO)
asyncio.run(dp.start_polling(bot))
