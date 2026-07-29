import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
import yt_dlp

TOKEN ="8549085903:AAGe2LmXahcCXxZzdOsF0oAB-h0g3j8Ilvg"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(lambda message: message.text and ("instagram.com" in message.text or "youtube.com" in message.text or "youtu.be" in message.text))
async def download_video(message: Message):
    url = message.text.strip()
    msg = await message.answer("📥 Video yuklab olinmoqda, iltimos kuting...")
    
    output_filename = "video.mp4"
    
    ydl_opts = {
    'format': 'best',
    'outtmpl': output_filename,
    'noplaylist': True,
}

    
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if os.path.exists(output_filename):
            video_file = types.FSInputFile(output_filename)
            await message.answer_video(video=video_file, caption="✅ Marhamat, siz so'ragan video!")
            await bot.delete_message(chat_id=message.chat.id, message_id=msg.message_id)
            os.remove(output_filename)
        else:
            await message.answer("❌ Videoni yuklab bo'lmadi. Havolani tekshiring.")
            
    except Exception as e:
        logging.error(f"Xatolik: {e}")
        await message.answer("❌ Xatolik yuz berdi. Bu video juda katta yoki yopiq profilniki bo'lishi mumkin.")
        if os.path.exists(output_filename):
            os.remove(output_filename)

@dp.message()
async def start_handler(message: Message):
    await message.answer("Salom! Menga Instagram yoki YouTube video havolasini yuboring, men uni sizga yuklab beraman! 📥")

async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

