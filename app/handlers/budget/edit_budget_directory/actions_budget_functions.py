from aiogram.types import CallbackQuery
import app.handlers.budget.keyboards.edit_budget_keyboard as kb
from app.handlers.budget.database.actionsBudget import delete_budget_db

async def delete_budget_function(callback: CallbackQuery, budget_id):
    if budget_id is None:
        await callback.answer("Выберите бюджет для удаления.", show_alert=True)
        return

    await callback.message.delete()
    await callback.answer()

    # Удаляем бюджет по ID
    await delete_budget_db(budget_id, callback.message)  # Теперь передаем бюджет_id
    budget_id = None  # Сбрасываем budget_id после операции


async def edit_budget_function(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()
    await callback.message.answer('Что желаете изменить?', reply_markup=kb.edit_budget_keyboard)  # Отправляем сообщение с деталями бюджета