from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
import app.keyboards.keyboardBudget as kb
import app.keyboards.keyboardMain as kbMain
from aiogram.fsm.state import State, StatesGroup
from app.database.budget.addBudget import addBudget
from app.handlers.handlerBudget import BudgetStates

create_budget_router = Router()

class create_budget_states(StatesGroup):
    waiting_for_budget_title = State()
    waiting_for_budget_description = State()

@create_budget_router.callback_query(F.data == 'create_budget_button')
async def create_budget(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    # Отправляем сообщение с просьбой ввести название бюджета и сохраняем идентификатор
    bot_message = await callback.message.answer("Введите название для бюджета:", reply_markup=kb.cancelKeyboard)
    await state.update_data(bot_message_id=bot_message.message_id)
    await state.set_state(BudgetStates.waiting_for_budget_title)
    await callback.answer()

@create_budget_router.message(BudgetStates.waiting_for_budget_title)
async def process_budget_title(message: Message, state: FSMContext):
    budget_name = message.text
    await state.update_data(budget_name=budget_name)  # Сохраняем название бюджета в состоянии
    await message.delete()  # Удаляем сообщение пользователя

    # Получаем идентификатор сообщения бота и удаляем его
    user_data = await state.get_data()
    bot_message_id = user_data.get('bot_message_id')
    await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)

    bot_message = await message.answer("Введите описание бюджета :", reply_markup=kb.addBudgetDescriptionKeyboard)
    await state.update_data(bot_message_id=bot_message.message_id)
    await state.set_state(BudgetStates.waiting_for_budget_description)

@create_budget_router.message(BudgetStates.waiting_for_budget_description)
async def process_budget_description(message: Message, state: FSMContext):
    user_data = await state.get_data()  # Получаем данные состояния
    bot_message_id = user_data.get('bot_message_id')

    if user_data.get('description') == '':
        # Если описание уже пустое (т.е. Нажата кнопка "Skip")
        await message.answer("Описание бюджета пропущено.", reply_markup=kbMain.mainKeyboard)
    else:
        # Обработка введенного описания
        description = message.text
        await state.update_data(description=description)  # Сохраняем описание
        await message.delete()  # Удаляем сообщение пользователя

        # Удаляем сообщение бота, если есть
        if bot_message_id is not None:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)

        budget_name = user_data.get('budget_name')  # Получаем название бюджета
        telegram_id = message.from_user.id
        result = addBudget(telegram_id, budget_name, description)

        await message.answer(result, reply_markup=kbMain.mainKeyboard)
    await state.clear()  # Очистка состояния после успешного создания бюджета

@create_budget_router.callback_query(F.data == 'skip_budget_description_button')
async def skip(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # Подтверждаем нажатие кнопки
    await callback.message.delete()  # Удаляем сообщение с кнопкой

    # Получаем данные состояния
    user_data = await state.get_data()
    budget_name = user_data.get('budget_name')  # Получаем название бюджета

    # Сохраняем пустое описание в состоянии
    description = ''
    await state.update_data(description=description)

    # Здесь добавляем логику добавления бюджета в базу данных
    telegram_id = callback.from_user.id
    result = addBudget(telegram_id, budget_name, description)

    await callback.message.answer(result, reply_markup=kbMain.mainKeyboard)
    await state.clear()  # Очистка состояния после успешного создания бюджета