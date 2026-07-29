import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
import yt_dlp

TOKEN ="8549085903:AAGe2LmXahcCXxZzdOsF0oAB-h0g3j8Ilvg"
bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(lambda message: message.text and ("instagram.com" in message.text or "youtu" in message.text))
async def download_video(message: Message):
    url = message.text.strip()
    msg = await message.answer("⏳ Qosimovde videongizni yuklayapti...")

    output_filename = "video.mp4"

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': output_filename,
        'noplaylist': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        }
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        if os.path.exists(output_filename):
            video_file = types.FSInputFile(output_filename)
            await message.answer_video(
                video=video_file, 
                caption="✅ Marhamat, siz so'ragan video!",
                supports_streaming=True
            )
            await bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
            os.remove(output_filename)
        else:
            await msg.edit_text("❌ Videoni yuklab bo'lmadi. Havolani tekshiring.")

    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await msg.edit_text("❌ Xatolik yuz berdi. Bu video juda katta yoki yopiq profilniki bo'lishi mumkin.")
        if os.path.exists(output_filename):
            os.remove(output_filename)

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


