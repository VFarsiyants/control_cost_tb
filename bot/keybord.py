from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


inline_btn_add_expense = InlineKeyboardButton(
    'Add expense', 
    callback_data='add_expense'
)

inline_btn_cancel = InlineKeyboardButton(
    'Cancel', 
    callback_data='cancel'
)

inline_menu = InlineKeyboardMarkup().add(
    inline_btn_add_expense
)

cancel_menu = InlineKeyboardMarkup().add(
    inline_btn_cancel
)
