from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

add_budget_description_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Пропустить', callback_data='skip_budget_description_button')],
    [InlineKeyboardButton(text='Отмена', callback_data='cancel_button')],
])