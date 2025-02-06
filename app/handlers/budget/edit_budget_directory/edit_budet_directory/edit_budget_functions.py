from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
import app.handlers.budget.edit_budget_directory.edit_budet_directory.edit_budget_keyboards as kb
from app.handlers.budget.database.edit_budget_description import set_new_budget_description
from app.handlers.budget.database.edit_budget_name import set_new_budget_name

async def edit_name_budget_function(callback: CallbackQuery, state: FSMContext, edit_budget_states):
        # Отправляем сообщение с просьбой ввести название бюджета и сохраняем идентификатор
        bot_message = await callback.message.edit_text("Введите название для бюджета:", reply_markup=kb.back_edit_name_budget_keyboard)
        await state.update_data(bot_message_id=bot_message.message_id)
        await state.set_state(edit_budget_states.waiting_for_new_name)
        await callback.answer()

async def process_edit_budget_name_function(message: Message, state: FSMContext, budget_id):
    budget_name = message.text
    await state.update_data(budget_name=budget_name)  # Сохраняем название бюджета в состоянии
    await message.delete()  # Удаляем сообщение пользователя

    # Получаем идентификатор сообщения бота и удаляем его
    user_data = await state.get_data()
    bot_message_id = user_data.get('bot_message_id')
    await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    await set_new_budget_name(message, budget_name, budget_id)
    await state.clear()  # Очистка состояния


async def edit_description_budget_function(callback: CallbackQuery, state: FSMContext, budget_id, edit_budget_states):
    await callback.message.delete()

    # Отправляем сообщение и сохраняем идентификатор сообщения
    bot_message = await callback.message.answer("Введите описание для бюджета:", reply_markup=kb.back_complete_edit_name_keyboard)
    await state.update_data(bot_message_id=bot_message.message_id)

    # Проверяем, что budget_id был установлен ранее
    if budget_id is None:
        await callback.answer("Id бюджета не найден. Пожалуйста, выберите бюджет для редактирования.", show_alert=True)
        return

    await state.set_state(edit_budget_states.waiting_for_budget_new_description)
    await callback.answer()

async def process_edit_budget_description_function(message: Message, state: FSMContext, budget_id):
    budget_description = message.text
    await state.update_data(budget_name=budget_description)  # Сохраняем новое описание бюджета
    await message.delete()  # Удаляем сообщение пользователя

    # Получаем идентификатор сообщения бота и удаляем его
    user_data = await state.get_data()
    bot_message_id = user_data.get('bot_message_id')
    await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)

    # Убедимся, что budget_id установлен перед вызовом функции обновления
    if budget_id is not None:
        await set_new_budget_description(message, budget_description, budget_id)
    else:
        await message.answer("Не удалось получить идентификатор бюджета. Обновление невозможно.",
                             reply_markup=kb.back_complete_edit_description_keyboard)
    await state.clear()  # Очистка состояния