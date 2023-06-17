from datetime import datetime
from decimal import Decimal
from re import match

from aiogram.types import CallbackQuery, Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext
from sqlalchemy import select, bindparam, insert

from bot.base import dp, bot
from bot.keybord import inline_menu
from database.models import User, Expense
from database.connection import Session


class ExpenseForm(StatesGroup):
    amount = State()
    name = State()

cost_pattern = r'^\d{1,10}\.\d{2}$'


@dp.callback_query_handler(lambda c: c.data == 'add_expense')
async def add_expense(callback_query: CallbackQuery):
    '''
    Get info about amount
    '''
    await ExpenseForm.amount.set()
    await bot.send_message(
        callback_query.from_user.id,
        'How much did you spend?',
    )


@dp.message_handler(lambda message: not match(cost_pattern, message.text), 
                    state=ExpenseForm.amount)
async def process_name(message: Message, state: FSMContext):
    '''
    Wrong format for amount
    '''
    error_msg = f'Wrong amount format. Please provide amount \n'\
                f'in xxxx.xx format for example: 1984.32'
    await message.reply(error_msg)


@dp.message_handler(lambda message: match(cost_pattern, message.text), 
                    state=ExpenseForm.amount)
async def process_name(message: Message, state: FSMContext):
    '''
    Get info about expense subject
    '''
    async with state.proxy() as data:
        data['cost'] = message.text

    await ExpenseForm.next()
    await message.reply("What did you buy?")


@dp.message_handler(state=ExpenseForm.name)
async def process_name(message: Message, state: FSMContext):
    '''
    Get info about expense subject
    '''
    async with state.proxy() as data:
        data['name'] = message.text
        __inser_expense(username=message.from_user.username, **data)

    await state.finish()
    await message.reply("Expense is recorded", reply_markup=inline_menu)


def __inser_expense(*, username, cost, name):
    with Session.begin() as session:
        scalar_subq = (
            select(User.id)
            .where(User.tg_username == bindparam("username"))
            .scalar_subquery()
        )
        session.execute(
            insert(Expense).values(user_id=scalar_subq),
            [
                {
                    "username": username,
                    "cost": Decimal(cost),
                    "created_at": datetime.now(),
                    "name": name
                },
            ],
        )
