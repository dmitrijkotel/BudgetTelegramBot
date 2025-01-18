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
    cancel = InlineKeyboardButton(text="Отмена", callback_data="cancel_button")

    for budget_id, budget_name in budgets:
        button = InlineKeyboardButton(text=budget_name, callback_data=str(budget_id))
        keyboard.add(button)  # Добавляем кнопку в клавиатуру

    keyboard.add(cancel)
    return keyboard.adjust(1).as_markup()  # Настраиваем клавиатуру на 2 кнопки в строке


# Пример функции для отображения бюджета
async def view_budget(message: types.Message, user_id):
    budgets = await get_budgets_from_db(user_id)  # Получаем бюджеты из базы данных

    cancel = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Отмена', callback_data='cancel_button')],
    ])

    if not budgets:  # Проверяем, если нет доступных бюджетов
        return await message.answer("Нет доступных бюджетов.", reply_markup=cancel)


    keyboard = await create_keyboard(budgets)  # Создаем клавиатуру с бюджетами

    await message.answer("Выберите бюджет:", reply_markup=keyboard)  # Отправляем сообщение с клавиатурой