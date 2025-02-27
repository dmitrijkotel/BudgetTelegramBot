import sqlite3
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import State, StatesGroup
from app.handlers.finance.keyboards.finance_budget_keyboard import back_expenses_categories_keyboard as kb_back
from app.handlers.finance.keyboards.finance_budget_keyboard import skip_description_expenses_keyboard as skip_keyboard

create_expenses_category_router = Router()


class CreateExpenseCategoryStates(StatesGroup):
    waiting_for_expenses_category_title = State()
    waiting_for_expenses_category_description = State()


budget_id_g = 0


def add_expenses_category_db(budget_id, category_name, description):
    conn = sqlite3.connect('tgBotDb.db')
    cursor = conn.cursor()
    try:
        cursor.execute("""  
            INSERT INTO categories (budget_id, name, type, description)   
            VALUES (?, ?, 'expense', ?)""",
                       (budget_id, category_name, description))
        conn.commit()
        return "Категория расхода успешно добавлена!"
    except Exception as e:
        conn.rollback()
        return f"Произошла ошибка: {str(e)}"
    finally:
        cursor.close()
        conn.close()


@create_expenses_category_router.callback_query(F.data == 'add_expenses_category_button')
async def create_expeses_category_handler(callback: CallbackQuery, state: FSMContext):

    user_data = await state.get_data()
    budget_id = user_data.get('budget_id')
    print(f"Создание категории: budget_id = {budget_id}")  # Отладка

    if not budget_id:
        await callback.answer("Ошибка: идентификатор бюджета не найден.")
        return

    bot_message = await callback.message.edit_text("Введите название для категории расхода:", reply_markup=kb_back)
    await state.update_data(bot_message_id=bot_message.message_id, budget_id=budget_id)
    global budget_id_g
    budget_id_g = budget_id
    await state.set_state(CreateExpenseCategoryStates.waiting_for_expenses_category_title)
    await callback.answer()


@create_expenses_category_router.message(CreateExpenseCategoryStates.waiting_for_expenses_category_title)
async def create_expenses_category_name(message: Message, state: FSMContext):
    user_data = await state.get_data()
    budget_id = user_data.get('budget_id')

    category_name = message.text
    await state.update_data(category_name=category_name)

    print(f"Название категории: {category_name}")  # Отладка

    await message.delete()  # Удаляем сообщение пользователя

    user_data = await state.get_data()
    bot_message_id = user_data.get('bot_message_id')

    # Редактируем сообщение бота
    if bot_message_id is not None:
        await message.bot.edit_message_text(
            chat_id=message.chat.id,
            message_id=bot_message_id,
            text="Введите описание категории (или нажмите 'Пропустить'):",
            reply_markup=skip_keyboard
        )
    else:
        # Если идентификатор сообщения бота не найден, отправляем новое сообщение
        bot_message = await message.answer(
            "Введите описание категории (или нажмите 'Пропустить'):",
            reply_markup=skip_keyboard
        )
        await state.update_data(bot_message_id=bot_message.message_id)

    await state.set_state(CreateExpenseCategoryStates.waiting_for_expenses_category_description)


@create_expenses_category_router.callback_query(F.data == "skip_expenses_categories_button")
async def skip_expensees_description_handler(callback: CallbackQuery, state: FSMContext):
    print("Пропуск описания категории")  # Отладка
    user_data = await state.get_data()
    category_name = user_data.get('category_name')
    budget_id = user_data.get('budget_id')
    bot_message_id = user_data.get('bot_message_id')

    description = None

    # Редактируем сообщение бота
    if bot_message_id is not None:
        await callback.bot.edit_message_text(
            chat_id=callback.from_user.id,
            message_id=bot_message_id,
            text="Описание категории пропущено.",
            reply_markup=kb_back
        )

    result = add_expenses_category_db(budget_id, category_name, description)

    await callback.answer(result)  # Отправляем результат пользователю
    await state.clear()  # Очистка состояния после успешного создания категории


@create_expenses_category_router.message(CreateExpenseCategoryStates.waiting_for_expenses_category_description)
async def create_expense_category_description(message: Message, state: FSMContext):
    print("Получение описания категории")  # Отладка
    await message.delete()  # Удаляем сообщение пользователя

    user_data = await state.get_data()
    category_name = user_data.get('category_name')
    budget_id = user_data.get('budget_id')
    bot_message_id = user_data.get('bot_message_id')

    description = message.text
    print(f"Добавление категории: budget_id={budget_id}, name={category_name}, type=expense, description={description}")  # Отладка

    # Редактируем сообщение бота
    if bot_message_id is not None:
        try:
            result = add_expenses_category_db(budget_id, category_name, description)
            await message.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=bot_message_id,
                text=result,
                reply_markup=kb_back
            )
        except Exception as e:
            print(f"Ошибка при добавлении категории: {e}")  # Логирование ошибки
            await message.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=bot_message_id,
                text="Произошла ошибка при добавлении категории. Попробуйте снова.",
                reply_markup=kb_back
            )
    else:
        # Если идентификатор сообщения бота не найден, отправляем новое сообщение
        result = add_expenses_category_db(budget_id, category_name, description)
        await message.answer(result, reply_markup=kb_back)

    await state.clear()  # Очистка состояния после успешного создания категории