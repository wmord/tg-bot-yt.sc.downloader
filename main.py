import asyncio
import os
from os import getenv
from yt_dlp import YoutubeDL
from aiogram import Dispatcher, Bot, F, BaseMiddleware
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, LinkPreviewOptions, TelegramObject
from aiogram.enums import ParseMode
from typing import Callable, Dict, Any, Awaitable

dp = Dispatcher()

ALLOWED_USERS = {}

class AccessControlMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        if user and user.id not in ALLOWED_USERS:
            return
        return await handler(event, data)
dp.message.outer_middleware(AccessControlMiddleware())

DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok = True)

def downloader(url: str) -> str:
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': os.path.join(DOWNLOAD_DIR, '%(title)s.%(ext)s'),
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'quiet': True,
    }
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        base, _ = os.path.splitext(filename)
        return f"{base}.mp3"

@dp.message(F.text.regexp(r'(https?://(?:www\.)?(?:youtube\.com|youtu\.be|soundcloud\.com)/[^\s]+)'))
async def muslink(message: Message):
    url = message.text
    status = await message.answer("downloading file, please wait...")
    try:
        file_path = await asyncio.to_thread(downloader, url)
        if os.path.exists(file_path):
            await status.edit_text("file downloaded. sending...")
            downloadedfile = FSInputFile(file_path)
            await message.answer_audio(audio=downloadedfile, caption = "your mp3 file")
            await status.delete()
            await asyncio.sleep(1)
            try:
                os.remove(file_path)
            except Exception as file_err:
                print(f"failed to delete file {file_path}. error message: {file_err}")
        else:
            await status.edit_text("failed to download mp3!")
    except Exception as e:
        print(f"error processing link {e}")
        await message.answer("an unknown error occurred")

@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    await message.answer(f"hello, <b>{message.from_user.full_name}</b>, im a music downloader bot. type /help for more info", parse_mode=ParseMode.HTML)

@dp.message(Command("help"))
async def cmd_help(message: Message) -> None:
    options_1 = LinkPreviewOptions(is_disabled = True)
    await message.answer("copy & paste link in\nhttps://soundcloud.com/some_symbols\nor\nhttps://youtu.be/some_symbols\nformat", link_preview_options = options_1)

async def main() -> None:
    token = getenv("TOKEN")
    bot = Bot(token=token)
    print("starting bot...")
    try:
        await dp.start_polling(bot)
    finally:
        print("bot stopped")

if __name__ == "__main__":
    asyncio.run(main())
