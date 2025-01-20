from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

budget_menu_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Создание бюджета', callback_data='create_budget_button')],
    [InlineKeyboardButton(text='Просмотр бюджета', callback_data='view_budget_button')]
])