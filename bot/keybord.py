from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_btn_add_expense = InlineKeyboardButton(
    'Add expense', 
    callback_data='add_expense'
)

inline_menu = InlineKeyboardMarkup().add(
    inline_btn_add_expense
)
