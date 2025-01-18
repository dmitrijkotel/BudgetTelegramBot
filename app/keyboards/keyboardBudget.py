from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

addBudgetDescriptionKeyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Пропустить', callback_data='skip_budget_description_button')],
    [InlineKeyboardButton(text='Отмена', callback_data='cancel_button')],
])

cancelKeyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='cancel_button')],
])

backKeyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back_button')],
])

actionsBudget = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Финансы', callback_data='finance_button')],

    [InlineKeyboardButton(text='Удалить', callback_data='delete_budget_button'),
    InlineKeyboardButton(text='Изменить', callback_data='edit_budget_button')],

    [InlineKeyboardButton(text='Oтчёт', callback_data='report_budget_button')],
    [InlineKeyboardButton(text='Отмена', callback_data='cancel_button')],
])

edit_budget_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Название', callback_data='edit_title_budget_button')],
    [InlineKeyboardButton(text='Описание', callback_data='edit_description_button')],
    [InlineKeyboardButton(text='Назад', callback_data='back_button')],
])

finance_budget_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Расходы', callback_data='expenses_budget_button'),
    InlineKeyboardButton(text='Доходы', callback_data='income_budget_button')],
    [InlineKeyboardButton(text='Назад', callback_data='back_button')],
])
