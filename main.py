from aiogram import executor

from bot.base import dp
from bot import handlers
from bot.scheduler import scheduler


async def on_startup(_):
    scheduler.start()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
