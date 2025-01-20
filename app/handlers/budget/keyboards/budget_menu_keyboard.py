from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

mainKeyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создание бюджета', callback_data='create_budget_button')],
    [InlineKeyboardButton(text='Просмотр бюджета', callback_data='view_budget_button')]
])

registrationKeyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Зарегистрироваться', callback_data='reg')]
])