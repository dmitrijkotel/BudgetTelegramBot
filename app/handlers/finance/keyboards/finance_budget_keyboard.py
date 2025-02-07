from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

finance_budget_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Расходы', callback_data='expenses_budget_button'),
    InlineKeyboardButton(text='Доходы', callback_data='income_budget_button')],
    [InlineKeyboardButton(text='Назад', callback_data='back_finance_button')],
])

back_income_categories_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back_income_categories_button')]
])

skip_description_income_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Пропустить', callback_data='skip_income_categories_button')],
    [InlineKeyboardButton(text='Назад', callback_data='back_description_income_button')],
])

back_expenses_categories_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back_expenses_categories_button')]
])

skip_description_expenses_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Пропустить', callback_data='skip_expenses_categories_button')],
    [InlineKeyboardButton(text='Назад', callback_data='back_description_expenses_button')],
])