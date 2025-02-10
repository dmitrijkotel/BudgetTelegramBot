from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
import app.handlers.main.keyboards.menu_keyboard as kb_menu
import app.handlers.budget.keyboards.budget_menu_keyboard as kb_main
import app.handlers.budget.keyboards.add_budget_description_keyboard as kb_desc
from aiogram.fsm.state import State, StatesGroup

create_report_router = Router()

class set_report_date(StatesGroup):
    waiting_for_report_date_start = State()
    waiting_for_report_date_end = State()

@create_report_router.callback_query(F.data == '')
async def create_budget_handler(callback: CallbackQuery, state: FSMContext):
    # Отправляем сообщение с просьбой ввести название бюджета и сохраняем идентификатор
    bot_message = await callback.message.edit_text("Введите дату начала отчёта для бюджета:", reply_markup=kb_menu.back_keyboard)
    await state.update_data(bot_message_id=bot_message.message_id)
    await state.set_state(set_report_date.waiting_for_report_date_start)
    await callback.answer()

@create_report_router.message(set_report_date.waiting_for_report_date_start)
async def create_budget_name(message: Message, state: FSMContext):
    budget_name = message.text
    await state.update_data(budget_name=budget_name)  # Сохраняем название бюджета в состоянии

    # Удаляем сообщение пользователя
    await message.delete()

    # Получаем идентификатор сообщения бота и редактируем его
    user_data = await state.get_data()
    bot_message_id = user_data.get('bot_message_id')
    
    await message.bot.edit_message_text(
        chat_id=message.chat.id,
        message_id=bot_message_id,
        text="Введите дату окончания отчёта для бюджета:",
        reply_markup=kb_desc.add_budget_description_keyboard
    )
    await state.set_state(set_report_date.waiting_for_report_date_end)

@create_report_router.message(set_report_date.waiting_for_report_date_end)
async def create_budget_description(message: Message, state: FSMContext):
    user_data = await state.get_data()  # Получаем данные состояния
    bot_message_id = user_data.get('bot_message_id')

    
    # Обработка введенного описания
    description = message.text
    await state.update_data(description=description)  # Сохраняем описание

    # Удаляем сообщение пользователя
    await message.delete()

    await state.clear()  # Очистка состояния после успешного создания бюджета