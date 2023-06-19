from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

from bot.base import dp, bot
from bot.keybord import inline_menu


@dp.callback_query_handler(lambda c: c.data == 'cancel', state='*')
async def cancel(callback_query: CallbackQuery, state: FSMContext):
    '''
    Cancel any action and return to main menu
    '''
    await state.finish()
    await bot.send_message(
        callback_query.from_user.id,
        'What you would like to do?',
        reply_markup=inline_menu
    )
