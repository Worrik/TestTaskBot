import asyncio
import logging

from aiogram import Dispatcher
from aiogram.dispatcher.filters import CommandStart
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message, WebAppInfo
from aiogram.utils import executor
from aiohttp import web

from config import ENDPOINT, dp

logging.basicConfig(level=logging.ERROR)


# /web-start
async def web_start(request):
    return web.FileResponse('web/start/start.html')


app = web.Application()
app.add_routes([
    web.get('/web-start', web_start),
])


async def on_startup(dps: Dispatcher):
    loop = asyncio.get_event_loop()
    loop.create_task(web._run_app(app, host="0.0.0.0", port=8080))


async def on_shutdown(dps: Dispatcher):
    await dps.storage.close()
    await dps.storage.wait_closed()


@dp.message_handler(CommandStart())
@dp.throttled(rate=2)
async def cmd_start(msg: Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Open web app", web_app=WebAppInfo(url=f"{ENDPOINT}/web-start")
        )]
    ])
    await msg.reply("TEST WEB APP", reply_markup=keyboard)


def main():
    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)


if __name__ == "__main__":
    main()
