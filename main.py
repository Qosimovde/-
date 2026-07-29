import os
import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import yt_dlp

TOKEN = "8549085903:AAFbdwg8vyEEn4vOml7AzfCGZsBhkiRIg2I"

bot = Bot(token=TOKEN)
dp = Dispatcher()

logging.basicConfig(level=logging.INFO)

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Salom! Menga Instagram havolasini yuboring, men uni videoni o'z holatida (pleyerda) yuklab beraman.")

@dp.message()
async def download_video(message: types.Message):
    url = message.text.strip()
    
    if not ("instagram.com" in url or "instagr.am" in url):
        await message.answer("Iltimos, faqat Instagram havolasini yuboring!")
        return

    msg = await message.answer("⏳ Video yuklanmoqda, biroz kuting...")
    
    output_filename = f"video_{message.from_user.id}.mp4"

    ydl_opts = {
        'format': 'best',
        'outtmpl': output_filename,
        'noplaylist': True,
        'http_headers': {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
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
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())



