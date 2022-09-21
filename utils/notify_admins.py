import logging

from aiogram import Dispatcher

from decouple import config


async def on_startup_notify(dp: Dispatcher):
    admin = config('ADMIN')
    try:
        await dp.bot.send_message(admin, "Bot ishga tushdi")

    except Exception as err:
        logging.exception(err)
