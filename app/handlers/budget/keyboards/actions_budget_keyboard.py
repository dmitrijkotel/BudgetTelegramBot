from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

actions_budget_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Финансы', callback_data='finance_button')],

    [InlineKeyboardButton(text='Удалить', callback_data='delete_budget_button'),
    InlineKeyboardButton(text='Изменить', callback_data='edit_budget_button')],

    [InlineKeyboardButton(text='Oтчёт', callback_data='report_budget_button')],
    [InlineKeyboardButton(text='Отмена', callback_data='cancel_button')],
])