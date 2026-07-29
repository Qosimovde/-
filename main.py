import logging
import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
import asyncio

# Tokeningizni shu yerga yozasiz
TOKEN = "BOT_TOKENINGIZNI_SHU_YERGA_YOZING"

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(lambda message: message.text and ("instagram.com" in message.text or "youtu" in message.text))
async def download_video(message: Message):
    await message.answer("📥 Hurmatli foydalanuvchi, videongiz yuklab olinmoqda, iltimos kuting...")
    # Bu yerda video yuklash logikasi bo'ladi
    await asyncio.sleep(2)
    await message.answer("✅ Video yuklash funksiyasi tez orada to'liq ishga tushadi!")

@dp.message()
async def start_handler(message: Message):
    await message.answer("Salom! Menga Instagram yoki boshqa tarmoqlardan video havolasini yuboring.")

async def main():
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
