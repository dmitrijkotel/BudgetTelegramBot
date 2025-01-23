from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

finance_budget_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Расходы', callback_data='expenses_budget_button'),
    InlineKeyboardButton(text='Доходы', callback_data='income_budget_button')],
    [InlineKeyboardButton(text='Назад', callback_data='back_button')],
])

view_income_categories_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить категорию', callback_data='add_income_categories_button')],
    [InlineKeyboardButton(text='Назад', callback_data='back_button')],
])

view_expense_categories_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Добавить категорию', callback_data='add_expense_categories_button')],
    [InlineKeyboardButton(text='Назад', callback_data='back_button')],
])
