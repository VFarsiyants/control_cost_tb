from aiogram import types
from bot.base import dp

from database.models import User
from database.base import Session


@dp.message_handler(commands=['start'])
async def register_user(message: types.Message):
    user_info = message.from_user
    with Session.begin() as session:
        user = session.query(User).filter(
            User.tg_username == user_info.username).\
            first()
        if user:
            return await message.answer(f'Привет, {user.name}')
        user = User(
            name=user_info.first_name,
            surname=user_info.last_name,
            tg_username=user_info.username
        )
        session.add(user)
        session.commit()
    await message.answer(f'Привет, {user.name}, ты зарегистрирован')