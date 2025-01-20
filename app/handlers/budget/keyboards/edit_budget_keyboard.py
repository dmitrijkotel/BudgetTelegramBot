from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


edit_budget_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Название', callback_data='edit_name_budget_button')],
    [InlineKeyboardButton(text='Описание', callback_data='edit_description_button')],
    [InlineKeyboardButton(text='Назад', callback_data='back_button')],
])