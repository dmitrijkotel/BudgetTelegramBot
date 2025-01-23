from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

back_edit_name_budget_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='back_edit_name_budget_button')],
])

back_complete_edit_name_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вернуться назад', callback_data='back_menu_budget_button')],
])

back_edit_description_budget_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Отмена', callback_data='back_edit_description_budget_button')],
])

back_complete_edit_description_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вернуться назад', callback_data='back_menu_budget_button')],
])