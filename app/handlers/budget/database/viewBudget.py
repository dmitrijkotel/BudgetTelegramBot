import aiosqlite
from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


async def get_budgets_from_db(user_id):
    async with aiosqlite.connect('tgBotDb.db') as conn:
        async with conn.execute("SELECT id, budget_name FROM budgets WHERE user_id = ?", (user_id,)) as cursor:
            buttons = await cursor.fetchall()  # Получаем список с id и name
    return buttons  # Возвращаем полученные данные


async def create_keyboard(budgets):
    keyboard = InlineKeyboardBuilder()
    back = InlineKeyboardButton(text="Назад", callback_data="back_button")

    for budget_id, budget_name in budgets:
        button = InlineKeyboardButton(text=budget_name, callback_data=str(budget_id))
        keyboard.add(button)  # Добавляем кнопку в клавиатуру

    keyboard.add(back)
    return keyboard.adjust(1).as_markup()  # Настраиваем клавиатуру на 2 кнопки в строке