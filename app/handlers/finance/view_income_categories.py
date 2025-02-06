from aiogram import Router, F
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
import aiosqlite
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from app.handlers.budget.database.viewBudget import get_budgets_from_db, create_keyboard
import app.handlers.budget.edit_budget_directory.action_budget_directory.actions_budget_keyboards as actions_kb

view_income_category_router = Router()

async def get_income_categories_from_db(budget_id: int):
    async with aiosqlite.connect('tgBotDb.db') as conn:
        async with conn.execute(
            "SELECT id, name FROM categories WHERE budget_id = ? AND type = ?",
            (budget_id, 'income')
        ) as cursor:
            return await cursor.fetchall()

async def create_income_categories_keyboard(categories):
    keyboard = InlineKeyboardBuilder()

    # Создаем кнопки для каждой категории
    for category_id, category_name in categories:
        button = InlineKeyboardButton(text=category_name, callback_data=f"category_{category_id}")
        keyboard.add(button)
        
        keyboard.adjust(1)  # 1 кнопка в ряд

    # Добавить кнопки "Добавить категорию" и "Назад" в новую строку
    keyboard.row(
        InlineKeyboardButton(text="Добавить категорию", callback_data="add_income_category_button"),
        InlineKeyboardButton(text="Назад", callback_data="back_income_categories_button")
    )

    # Возвращаем клавиатуру
    return keyboard.as_markup()

async def view_income_categories(message: Message, budget_id: int):
    categories = await get_income_categories_from_db(budget_id)
    keyboard = await create_income_categories_keyboard(categories)

    if not categories:
        await message.answer("Нет доступных категорий доходов.", reply_markup=keyboard)
    else:
        await message.answer("Выберите категорию дохода:", reply_markup=keyboard)

async def menu_budgets(callback):
    telegram_id = callback.from_user.id

    await callback.answer()

    budgets = await get_budgets_from_db(telegram_id)

    if not budgets:
        return await callback.message.answer("Нет доступных бюджетов.", reply_markup=actions_kb.back_menu)

    keyboard = await create_keyboard(budgets)

    await callback.message.edit_text("Выберите бюджет:", reply_markup=keyboard)

@view_income_category_router.callback_query(F.data == 'back_income_categories_button')
async def back_button_handler(callback: CallbackQuery):
    await menu_budgets(callback)

@view_income_category_router.callback_query(F.data == 'income_budget_button')
async def view_income_categories_handler(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    budget_id = user_data.get('budget_id')

    if budget_id is None:
        await callback.answer("Ошибка: идентификатор бюджета не найден.")
        return

    await callback.message.delete()
    await view_income_categories(callback.message, budget_id)

async def get_category_details_db(category_id: int):
    async with aiosqlite.connect('tgBotDb.db') as db:
        async with db.execute("SELECT name, description FROM categories WHERE id = ?", (category_id,)) as cursor:
            return await cursor.fetchone()

income_category_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back_from_all_income_categories_button')]
])

@view_income_category_router.callback_query(F.data == 'back_from_all_income_categories_button')
async def back_from_all_income_categories_handler(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    budget_id = user_data.get('budget_id')

    if budget_id is None:
        await callback.answer("Ошибка: идентификатор бюджета не найден.")
        return

    await callback.message.delete()
    await view_income_categories(callback.message, budget_id)