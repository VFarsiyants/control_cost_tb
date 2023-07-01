from aiogram import executor
from aiogram.types import BotCommand

from bot.base import dp, bot
from bot import handlers
from bot.scheduler import scheduler


async def on_startup(_):
    scheduler.start()
    bot_commands = [
        BotCommand(command='/start', description='Expense managment'),
        BotCommand(command='/statistic', 
                   description='Statistic information about expense'),
    ]
    await bot.set_my_commands(bot_commands)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
