from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from app.handlers.budget.keyboards.actions_budget_keyboard import actions_budget_keyboard as kb_act
from aiogram.fsm.state import State, StatesGroup

from app.handlers.budget.database.actionsBudget import get_budget_details_db
from app.handlers.budget.database.viewBudget import create_keyboard, get_budgets_from_db
from app.handlers.budget.edit_budget_directory.action_budget_directory.actions_budget_functions import delete_budget_function, edit_budget_function
from app.handlers.budget.edit_budget_directory.edit_budet_directory.edit_budget_functions import edit_name_budget_function, \
    edit_description_budget_function, process_edit_budget_description_function, process_edit_budget_name_function
import app.handlers.budget.edit_budget_directory.action_budget_directory.actions_budget_keyboards as actions_kb

view_budget_router = Router()

async def menu_budgets(callback):
    telegram_id = callback.from_user.id

    await callback.answer()

    budgets = await get_budgets_from_db(telegram_id)

    if not budgets:
        return await callback.message.edit_text("Нет доступных бюджетов.", reply_markup=actions_kb.back_menu)

    keyboard = await create_keyboard(budgets)

    await callback.message.edit_text("Выберите бюджет:", reply_markup=keyboard)


class edit_budget_states(StatesGroup):
    waiting_for_new_name = State()
    waiting_for_budget_new_description = State()

@view_budget_router.callback_query(F.data == 'view_budget_button')
async def view_budget_handler(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    await menu_budgets(callback)  # Предполагается, что эта функция получает все бюджеты для конкретного пользователя
    await callback.answer()

# Глобальная переменная budget_id
budget_id = None

@view_budget_router.callback_query(lambda call: call.data.isdigit())
async def handle_budget_selection(callback: CallbackQuery, state: FSMContext):
    try:
        await callback.answer()  # Оповещение об успешном нажатии на кнопку

        global budget_id  # Используем глобальную переменную
        budget_id = int(callback.data)
        await state.update_data(budget_id=budget_id)

        # Получаем детали бюджета
        budget_details = await get_budget_details_db(budget_id)
        if budget_details:
            budget_name, description = budget_details
            response_message = f"{budget_name}\nОписание: {description}" if description else f"{budget_name}\n"
        else:
            response_message = "Бюджет не найден."

        # Отправляем сообщение с деталями бюджета
        await callback.message.edit_text(response_message, reply_markup=kb_act)
    except Exception as e:
        # Обработка ошибок, если выходит за рамки общего
        await callback.answer("Произошла ошибка. Попробуйте позже.")
        print(f"Ошибка при обработке запроса: {e}")
    print(
        f" budget_id: {budget_id}")


@view_budget_router.callback_query(F.data == 'delete_budget_button')
async def delete_budget_handler(callback: CallbackQuery):
    
    await callback.answer()
    await callback.message.edit_text('Вы уверены, что хотите удалить этот бюджет?', reply_markup=actions_kb.cancel_sure_keyboard)

@view_budget_router.callback_query(F.data == 'yes_button')
async def delete_budget_handler(callback: CallbackQuery):
    global budget_id
    await delete_budget_function(callback, budget_id)

@view_budget_router.callback_query(F.data == 'back_button_sure')
async def delete_budget_handler(callback: CallbackQuery):
    await menu_budgets(callback)

@view_budget_router.callback_query(F.data == 'back_menu_budget_button')
async def delete_budget_handler(callback: CallbackQuery):
    await menu_budgets(callback)

@view_budget_router.callback_query(F.data == 'edit_budget_button')
async def edit_budget_handler(callback: CallbackQuery):
    await edit_budget_function(callback)

@view_budget_router.callback_query(F.data == 'back_edit_budget_button')
async def edit_budget_handler(callback: CallbackQuery):
    await menu_budgets(callback)

@view_budget_router.callback_query(F.data == 'edit_name_budget_button')
async def edit_name_budget_handler(callback: CallbackQuery, state: FSMContext):
    await edit_name_budget_function(callback, state, edit_budget_states)

@view_budget_router.callback_query(F.data == 'back_edit_name_budget_button')
async def edit_name_budget_handler(callback: CallbackQuery, state: FSMContext):
    await menu_budgets(callback)

@view_budget_router.message(edit_budget_states.waiting_for_new_name)
async def process_update_budget_name_handler(message: Message, state: FSMContext):
    await process_edit_budget_name_function(message, state, budget_id)

@view_budget_router.callback_query(F.data == 'back_menu_budget_button')
async def edit_name_budget_handler(callback: CallbackQuery, state: FSMContext):
    await menu_budgets(callback)

@view_budget_router.callback_query(F.data == 'edit_description_button')
async def edit_description_budget_handler(callback: CallbackQuery, state: FSMContext):
    await edit_description_budget_function(callback, state, budget_id, edit_budget_states)

@view_budget_router.callback_query(F.data == 'back_edit_description_budget_button')
async def edit_name_budget_handler(callback: CallbackQuery, state: FSMContext):
    await menu_budgets(callback)

@view_budget_router.message(edit_budget_states.waiting_for_budget_new_description)
async def process_edit_budget_description_handler(message: Message, state: FSMContext):
    await process_edit_budget_description_function(message, state, budget_id)

@view_budget_router.callback_query(F.data == 'back_menu_budget_button')
async def edit_name_budget_handler(callback: CallbackQuery, state: FSMContext):
    await menu_budgets(callback)