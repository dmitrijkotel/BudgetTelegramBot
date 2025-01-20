from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup



cancelKeyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='cancel_button')],
])

backKeyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back_button')],
])

finance_budget_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Расходы', callback_data='expenses_budget_button'),
    InlineKeyboardButton(text='Доходы', callback_data='income_budget_button')],
    [InlineKeyboardButton(text='Назад', callback_data='back_button')],
])
