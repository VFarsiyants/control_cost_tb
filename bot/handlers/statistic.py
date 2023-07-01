from datetime import datetime
from dateutil.relativedelta import relativedelta
from re import match

from aiogram.types import (CallbackQuery, Message, 
                           InlineKeyboardMarkup, InlineKeyboardButton)
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

from bot.base import dp, bot
from bot.keybord import cancel_menu, inline_btn_cancel
from bot.services import get_expenses_by_categories, get_expenses_list


class StatisticForm(StatesGroup):
    period = State()
    statistic_type = State()

month_pattern = r'^\d{2}$'
month_year_pattern = r'^\d{2}\.\d{4}$'
day_pattern = r'^\d{2}\.\d{2}\.\d{4}$'
period_pattern = r'^\d{2}\.\d{2}\.\d{4}-\d{2}\.\d{2}\.\d{4}$'

patterns = [day_pattern, month_pattern, month_year_pattern, period_pattern]

periods_msg = \
        'Reply with period for expenses statistic in different formats:\n'\
        'MM - will show statistic in month of current year;\n'\
        'MM.YYYY - will show statistic in month of dedicated year;\n'\
        'DD.MM.YYYY - wil show statistic in desired day;\n'\
        'DD.MM.YYYY-DD.MM.YYYY - will show statistic in inserted period\n'

def _period_match(string: str, patterns: list):
    for pattern in patterns:
        if match(pattern, string):
            return True
    return False

def _get_month_period(month: str):
    year = datetime.now().year
    from_date = datetime(day=1, month=int(month), year=year)
    to_date = from_date + relativedelta(months=1)
    return (from_date, to_date)
    
def _get_day_period(day: str):
    from_date = datetime.strptime(day, '%d.%m.%Y')
    to_date = from_date + relativedelta(days=1)
    return (from_date, to_date)

def _get_month_year(month_year: str):
    from_date = datetime.strptime(month_year, '%m.%Y')
    to_date = from_date + relativedelta(months=1)
    return (from_date, to_date)

def _get_period_days(period: str):
    days_str = period.split('-')
    if len(days_str) < 2:
        raise ValueError
    from_date = datetime.strptime(days_str[0], '%d.%m.%Y')
    to_date = datetime.strptime(days_str[1], '%d.%m.%Y') + relativedelta(days=1)
    return (from_date, to_date)

period_patterns_map = {
    month_pattern: _get_month_period,
    month_year_pattern: _get_month_year,
    day_pattern: _get_day_period,
    period_pattern: _get_period_days
}

statistic_type_menu = InlineKeyboardMarkup()

inline_btn_statistic_by_categories = InlineKeyboardButton(
    'Statistic by categories', 
    callback_data='statistic_by_categories'
)

inline_btn_expenses_list = InlineKeyboardButton(
    'Expenses_list', 
    callback_data='expenses_list'
)

statistic_type_menu.add(inline_btn_statistic_by_categories)
statistic_type_menu.add(inline_btn_expenses_list)
statistic_type_menu.add(inline_btn_cancel)


@dp.message_handler(commands=['statistic'])
async def statistic_menu(message: Message, state: FSMContext):
    '''
    Get info about period
    '''
    await StatisticForm.period.set()
    await bot.send_message(
        message.from_user.id, periods_msg, reply_markup=cancel_menu)


@dp.message_handler(lambda message: _period_match(message.text, patterns), 
                    state=StatisticForm.period)
async def select_statistic_type(message: Message, state: FSMContext):
    '''
    Get info about statistic type
    '''
    period = None
    for pattern, function in period_patterns_map.items():
        if match(pattern, message.text):
            try:
                period = function(message.text)
            except ValueError:
                return await wrong_period_format(message, state)
    async with state.proxy() as data:
        data['period'] = period
    await StatisticForm.next()
    await bot.send_message(
        message.from_user.id,
        'Select type of statistic report',
        reply_markup=statistic_type_menu
    )


@dp.message_handler(lambda message: not _period_match(message.text, patterns), 
                    state=StatisticForm.period)
async def wrong_period_format(message: Message, state: FSMContext):
    '''
    Handler for wrong period inserted
    '''
    await bot.send_message(
        message.from_user.id,
        'Period not match any pattern\n\n' + periods_msg,
        reply_markup=cancel_menu
    )


@dp.callback_query_handler(lambda c: c.data == 'statistic_by_categories',
                           state=StatisticForm.statistic_type)
async def add_expense(callback_query: CallbackQuery, state: FSMContext):
    '''
    Get info about amount
    '''

    state_data = dict()
    async with state.proxy() as data:
        state_data = data
    expenses_by_categories, total = get_expenses_by_categories(
        callback_query.from_user.username, state_data['period']
    )
    expenses_table_str = '\n'.join(
        [f'{item["category_name"]}: '
         f'{item["expenses_sum"]} ({item["fraction"]} %)' 
         for item in expenses_by_categories])
    expenses_msg = (f'Your expenses by category:\n\n' 
                    + expenses_table_str
                    + f'\n\nTotal expenses: {total}')
    await state.finish()
    await bot.send_message(
        callback_query.from_user.id,
        expenses_msg,
    )


@dp.callback_query_handler(lambda c: c.data == 'expenses_list',
                           state=StatisticForm.statistic_type)
async def add_expense(callback_query: CallbackQuery, state: FSMContext):
    '''
    Get info about amount
    '''
    state_data = dict()
    async with state.proxy() as data:
        state_data = data
    expenses_list, total = get_expenses_list(
        callback_query.from_user.username, state_data['period'])
    expenses_table_str = '\n'.join(
        [f'{item["date"]}. {item["name"]} - {item["cost"]}' 
         for item in expenses_list])
    expenses_msg = (f'Your expenses:\n\n' 
                    + expenses_table_str
                    + f'\n\ntotal expenses {total}')
    await state.finish()
    await bot.send_message(
        callback_query.from_user.id,
        expenses_msg,
    )
