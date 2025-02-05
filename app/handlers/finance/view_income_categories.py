from aiogram import Router, F  
from aiogram.types import CallbackQuery, Message  
from aiogram.fsm.context import FSMContext  
import aiosqlite  
from app.handlers.budget.database.viewBudget import get_budgets_from_db, create_keyboard  
import app.handlers.budget.edit_budget_directory.action_budget_directory.actions_budget_keyboards as actions_kb  
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup  
from aiogram.utils.keyboard import InlineKeyboardBuilder   

view_income_category_router = Router()  

async def get_income_categories_from_db(budget_id):  
    async with aiosqlite.connect('tgBotDb.db') as conn:  
        async with conn.execute(  
            "SELECT id, name FROM categories WHERE budget_id = ? AND type = ?",  
            (budget_id, 'income')  
        ) as cursor:  
            buttons = await cursor.fetchall()  # Получаем список с id и name категорий  
    return buttons  # Возвращаем полученные данные  

async def create_income_categories_keyboard(categories):  
    keyboard = InlineKeyboardBuilder()  

    # Создаем кнопки для каждой категории  
    for category_id, category_name in categories:  
        button = InlineKeyboardButton(text=category_name, callback_data=f"category_{category_id}")  
        keyboard.add(button)  

    # Добавляем кнопки "Добавить категорию" и "Назад"  
    keyboard.row(  
        InlineKeyboardButton(text="Добавить категорию", callback_data="add_income_category_button"),  
        InlineKeyboardButton(text="Назад", callback_data="back_income_categories_button")  
    )  

    # Возвращаем клавиатуру  
    return keyboard.as_markup()  

async def view_income_categories(message: Message, budget_id):  
    categories = await get_income_categories_from_db(budget_id)  # Получаем категории доходов из БД  

    # Создаем клавиатуру с категориями и кнопками "Добавить категорию" и "Назад"  
    keyboard = await create_income_categories_keyboard(categories)  

    # Если нет доступных категорий, выводим соответствующее сообщение  
    if not categories:  
        await message.answer("Нет доступных категорий доходов.", reply_markup=keyboard)  
    else:  
        await message.answer("Выберите категорию дохода:", reply_markup=keyboard)  # Отправляем сообщение с клавиатурой  

async def menu_budgets(callback: CallbackQuery):  
    telegram_id = callback.from_user.id  
    await callback.answer()  
    await callback.message.delete()  

    budgets = await get_budgets_from_db(telegram_id)  # Получаем бюджеты для пользователя  

    if not budgets:  
        return await callback.message.answer("Нет доступных бюджетов.", reply_markup=actions_kb.back_menu)  

    keyboard = await create_keyboard(budgets)  

    await callback.message.answer("Выберите бюджет:", reply_markup=keyboard)  

@view_income_category_router.callback_query(F.data == 'back_income_categories_button')  
async def back_button_handler(callback: CallbackQuery):  
    await menu_budgets(callback)  

@view_income_category_router.callback_query(F.data == 'income_budget_button')  
async def view_income_categories_handler(callback: CallbackQuery, state: FSMContext):  
    print("Проверка категорий бюджета")  # Отладочная информация  
    user_data = await state.get_data()  
    budget_id = user_data.get('budget_id')  # Получаем budget_id из состояния  

    if budget_id is None:  
        await callback.answer("Ошибка: идентификатор бюджета не найден.")  
        return  

    await callback.message.delete()  
    await view_income_categories(callback.message, budget_id)  

async def get_category_details_db(category_id):  
    async with aiosqlite.connect('tgBotDb.db') as db:  
        async with db.execute("SELECT name, description FROM categories WHERE id = ?",  
            (category_id,)) as cursor:  
            category = await cursor.fetchone()  # Получаем детали категории  
    return category  

income_category_keyboard = InlineKeyboardMarkup(inline_keyboard=[  
    [InlineKeyboardButton(text='Назад', callback_data='back_from_all_income_categories_button')]  
])  

@view_income_category_router.callback_query(F.data == 'back_from_all_income_categories_button')  
async def back_from_all_income_categories_handler(callback: CallbackQuery, state: FSMContext):  
    user_data = await state.get_data()  
    budget_id = user_data.get('budget_id')  # Получаем budget_id из состояния  

    if budget_id is None:  
        await callback.answer("Ошибка: идентификатор бюджета не найден.")  
        return  

    await callback.message.delete()  # Удаляем предыдущее сообщение  
    await view_income_categories(callback.message, budget_id)  # Переход к просмотру категорий доходов  

@view_income_category_router.callback_query(lambda call: call.data.startswith("category_"))  
async def handle_income_selection(callback: CallbackQuery, state: FSMContext):  
    try:  
        await callback.message.delete()  # Удаляем предыдущее сообщение  
        await callback.answer()  # Оповещение об успешном нажатии на кнопку  

        category_id = int(callback.data.split("_")[1])  # Извлекаем ID категории  
        await state.update_data(category_id=category_id)  # Сохраняем category_id в состоянии  
        
        # Получаем детали категории  
        category_details = await get_category_details_db(category_id)  
        if category_details:  
            name, description = category_details  
            response_message = f"Категория: {name}\nОписание: {description}" if description else f"{name}\n"  
        else:  
            response_message = "Категория не найдена."  

        # Отправляем сообщение с деталями категории  
        await callback.message.answer(response_message, reply_markup=income_category_keyboard)  
    except Exception as e:  
        await callback.answer("Произошла ошибка. Попробуйте позже.")  
        print(f"Ошибка при обработке запроса: {e}")