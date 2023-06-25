from datetime import datetime
import os

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from dotenv import load_dotenv

from bot.services.categorize_ai import categorize_ai

load_dotenv()

timezone = os.getenv('TIMEZONE', 'Europe/Moscow')
categorization_time = os.getenv('CATEGORIZATION_TIME', '00:00')
categorization_time = datetime.strptime(categorization_time, '%H:%M').time()


scheduler = AsyncIOScheduler(timezone='Europe/Moscow')
scheduler.add_job(
    categorize_ai, 
    trigger='cron',
    hour=categorization_time.hour,
    minute=categorization_time.minute,
    start_date=datetime.now()
)
