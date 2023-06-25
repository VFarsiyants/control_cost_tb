import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from dotenv import load_dotenv
import openai


load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)

bot_token = os.getenv('API_TOKEN')
openai.api_key = os.getenv('OPEN_AI_KEY', None)

# Initialize bot and dispatcher
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
