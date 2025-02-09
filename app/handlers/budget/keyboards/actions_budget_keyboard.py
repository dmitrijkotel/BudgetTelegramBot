from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

actions_budget_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Расходы', callback_data='expenses_budget_button'),
    InlineKeyboardButton(text='Доходы', callback_data='income_budget_button')],

    [InlineKeyboardButton(text='Удалить', callback_data='delete_budget_button'),
    InlineKeyboardButton(text='Изменить', callback_data='edit_budget_button')],

    [InlineKeyboardButton(text='Oтчёт', callback_data='report_budget_button')],
    [InlineKeyboardButton(text='Назад', callback_data='back_menu_budget_button')],
])