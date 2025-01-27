import sqlite3
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from app.handlers.finance.keyboards.finance_budget_keyboard import back_income_categories_keyboard as kb_back
from app.handlers.finance.keyboards.finance_budget_keyboard import skip_description_income_keyboard as skip_keyboard
from app.handlers.finance.view_income_categories import view_income_categories

create_income_category_router = Router()


class CreateIncomeCategoryStates(StatesGroup):
    waiting_for_category_title = State()
    waiting_for_category_description = State()


budget_id_g = 0


def add_income_category_db(budget_id, category_name, description):
    conn = sqlite3.connect('tgBotDb.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""  
            INSERT INTO categories (budget_id, name, type, description)   
            VALUES (?, ?, 'income', ?)""",
                       (budget_id, category_name, description))
        conn.commit()
        return "Категория дохода успешно добавлена!"
    except Exception as e:
        conn.rollback()
        return f"Произошла ошибка: {str(e)}"
    finally:
        cursor.close()
        conn.close()


@create_income_category_router.callback_query(F.data == 'add_income_category_button')
async def create_income_category_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()

    user_data = await state.get_data()
    budget_id = user_data.get('budget_id')
    print(f"Создание категории: budget_id = {budget_id}")  # Отладка

    if not budget_id:
        await callback.answer("Ошибка: идентификатор бюджета не найден.")
        return

    bot_message = await callback.message.answer("Введите название для категории дохода:", reply_markup=kb_back)
    await state.update_data(bot_message_id=bot_message.message_id, budget_id=budget_id)
    global budget_id_g
    budget_id_g = budget_id
    await state.set_state(CreateIncomeCategoryStates.waiting_for_category_title)
    await callback.answer()


@create_income_category_router.message(CreateIncomeCategoryStates.waiting_for_category_title)
async def create_income_category_name(message: Message, state: FSMContext):
    user_data = await state.get_data()
    budget_id = user_data.get('budget_id')

    category_name = message.text
    await state.update_data(category_name=category_name)

    print(f"Название категории: {category_name}")  # Отладка

    await message.delete()
    user_data = await state.get_data()
    bot_message_id = user_data.get('bot_message_id')

    if bot_message_id is not None:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)

    bot_message = await message.answer("Введите описание категории (или нажмите 'Пропустить'):",
                                       reply_markup=skip_keyboard)
    await state.update_data(bot_message_id=bot_message.message_id)
    await state.set_state(CreateIncomeCategoryStates.waiting_for_category_description)


@create_income_category_router.callback_query(F.data == "skip_income_categories_button")
async def skip_description_handler(callback: CallbackQuery, state: FSMContext):
    print("Пропуск описания категории")  # Отладка
    user_data = await state.get_data()
    category_name = user_data.get('category_name')
    budget_id = user_data.get('budget_id')

    description = None

    bot_message_id = user_data.get('bot_message_id')

    if bot_message_id is not None:
        await callback.bot.delete_message(chat_id=callback.from_user.id, message_id=bot_message_id)

    result = add_income_category_db(budget_id, category_name, description)

    await callback.message.answer(result, reply_markup=kb_back)
    await state.clear()  # Очистка состояния после успешного создания категории


@create_income_category_router.message(CreateIncomeCategoryStates.waiting_for_category_description)
async def create_income_category_description(message: Message, state: FSMContext):
    print("Получение описания категории")  # Отладка
    await message.delete()
    user_data = await state.get_data()
    category_name = user_data.get('category_name')
    budget_id = user_data.get('budget_id')

    description = message.text
    print(f"Описание категории: {description}")  # Отладка

    bot_message_id = user_data.get('bot_message_id')

    if bot_message_id is not None:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)

    result = add_income_category_db(budget_id, category_name, description)
    await message.answer(result, reply_markup=kb_back)
    await state.clear()  # Очистка состояния после успешного создания категории


@create_income_category_router.callback_query(F.data == 'income_budget_button')
async def view_income_categories_handler(callback: CallbackQuery, state: FSMContext):
    print("Проверка категорий бюджета")  # Отладка
    global budget_id_g

    user_data = await state.get_data()
    budget_id = user_data.get('budget_id')

    if budget_id is None:
        budget_id = budget_id_g
        if budget_id is None:
            await callback.answer("Ошибка: идентификатор бюджета не найден.")
            return

    await callback.message.delete()
    await view_income_categories(callback.message, budget_id)