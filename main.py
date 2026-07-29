import os
import asyncio
from aiohttp import web, ClientSession
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import yt_dlp

TOKEN ="8549085903:AAFbdwg8vyEEn4vOml7AzfCGZsBhkiRIg2I"
bot = Bot(token=TOKEN)
dp = Dispatcher()

# --- 1. 5 SEKUNDDA BIR O'ZINI O'ZI UYG'OTISH ---
async def handle(request):
    return web.Response(text="Bot 10 sekundda bir tinimsiz ishlamoqda!")

async def self_ping():
    await asyncio.sleep(5)
    url = os.environ.get("RENDER_EXTERNAL_URL")
    if not url:
        return
    while True:
        try:
            async with ClientSession() as session:
                async with session.get(url) as response:
                    await response.text()
        except Exception:
            pass
        await asyncio.sleep(10)

async def start_web_server():
    app = web.Application()
    app.add_routes([web.get('/', handle)])
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    
    asyncio.create_task(self_ping())

# --- 2. YUKLASH FUNKSIYASI ---
def download_media(url: str) -> str:
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'quiet': True,
        'no_warnings': True,
    }
    os.makedirs('downloads', exist_ok=True)
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    await message.answer("Assalomu alaykum! Menga Instagram yoki YouTube havolasini yuboring.")

@dp.message()
async def download_handler(message: types.Message):
    url = message.text.strip()
    if not url.startswith("http"):
        await message.answer("Iltimos, to'g'ri havola yuboring!")
        return

    processing_msg = await message.answer("Qosimovde videoingizni yuklamoqda...")

    try:
        loop = asyncio.get_running_loop()
        file_path = await loop.run_in_executor(None, download_media, url)
        
        if file_path.endswith(('.mp4', '.mkv', '.mov', '.webm')):
            await message.answer_video(types.FSInputFile(file_path))
        elif file_path.endswith(('.jpg', '.jpeg', '.png', '.webp')):
            await message.answer_photo(types.FSInputFile(file_path))
        else:
            await message.answer_document(types.FSInputFile(file_path))
            
        await bot.delete_message(message.chat.id, processing_msg.message_id)
        
        if os.path.exists(file_path):
            os.remove(file_path)
            
    except Exception as e:
        await message.answer(f"Xatolik yuz berdi: Havola yopiq yoki yaroqsiz bo'lishi mumkin.")
        try:
            await bot.delete_message(message.chat.id, processing_msg.message_id)
        except:
            pass

async def main():
    asyncio.create_task(start_web_server())
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
