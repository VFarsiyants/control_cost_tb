import os
import logging

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv


load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

bot_token = os.getenv('API_TOKEN')

# Initialize bot and dispatcher
bot = Bot(token=bot_token)
dp = Dispatcher(bot)
