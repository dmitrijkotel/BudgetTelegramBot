from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from app.handlers.budget.keyboards.actions_budget_keyboard import actions_budget_keyboard as kb_act
from aiogram.fsm.state import State, StatesGroup

from app.handlers.budget.database.actionsBudget import get_budget_details_db
from app.handlers.budget.database.viewBudget import view_budget
from app.handlers.budget.edit_budget_directory.actions_budget_functions import delete_budget_function, edit_budget_function
from app.handlers.budget.edit_budget_directory.edit_budget_functions import edit_name_budget_function, \
    edit_description_budget_function, process_edit_budget_description_function, process_edit_budget_name_function
view_budget_router = Router()

class edit_budget_states(StatesGroup):
    waiting_for_new_name = State()
    waiting_for_budget_new_description = State()

@view_budget_router.callback_query(F.data == 'view_budget_button')
async def view_budget_handler(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    await callback.message.delete()
    await view_budget(callback.message, telegram_id)  # Предполагается, что эта функция получает все бюджеты для конкретного пользователя
    await callback.answer()

# Глобальная переменная budget_id
budget_id = None

@view_budget_router.callback_query(lambda call: call.data.isdigit())
async def handle_budget_selection(callback: CallbackQuery):
    global budget_id  # Используем глобальную переменную
    budget_id = int(callback.data)  # Присваиваем значение

    budget_details = await get_budget_details_db(budget_id)  # Функция, которую нужно реализовать
    if budget_details:
        budget_name, description = budget_details
        response_message = f"{budget_name}\nОписание: {description}" if description else f"{budget_name}\n"
    else:
        response_message = "Бюджет не найден."

    await callback.message.delete()
    await callback.answer()  # Оповещение об успешном нажатии на кнопку
    await callback.message.answer(response_message, reply_markup=kb_act)  # Отправляем сообщение с деталями бюджета

@view_budget_router.callback_query(F.data == 'delete_budget_button')
async def delete_budget_handler(callback: CallbackQuery):
    global budget_id
    await delete_budget_function(callback, budget_id)

@view_budget_router.callback_query(F.data == 'edit_budget_button')
async def edit_budget_handler(callback: CallbackQuery):
    await edit_budget_function(callback)

@view_budget_router.callback_query(F.data == 'edit_name_budget_button')
async def edit_name_budget_handler(callback: CallbackQuery, state: FSMContext):
    await edit_name_budget_function(callback, state, edit_budget_states)

@view_budget_router.message(edit_budget_states.waiting_for_new_name)
async def process_update_budget_name_handler(message: Message, state: FSMContext):
    await process_edit_budget_name_function(message, state, budget_id)

@view_budget_router.callback_query(F.data == 'edit_description_button')
async def edit_description_budget_handler(callback: CallbackQuery, state: FSMContext):
    await edit_description_budget_function(callback, state, budget_id, edit_budget_states)

@view_budget_router.message(edit_budget_states.waiting_for_budget_new_description)
async def process_edit_budget_description_handler(message: Message, state: FSMContext):
    await process_edit_budget_description_function(message, state, budget_id)