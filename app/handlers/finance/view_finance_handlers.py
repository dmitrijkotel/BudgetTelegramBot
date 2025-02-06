from unicodedata import category

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
import app.handlers.finance.keyboards.finance_budget_keyboard as kb
from app.handlers.budget.database.viewBudget import get_budgets_from_db, create_keyboard
import app.handlers.budget.edit_budget_directory.action_budget_directory.actions_budget_keyboards as actions_kb
from app.handlers.budget.edit_budget_directory.view_budget_handlers import budget_id
from app.handlers.finance.view_income_categories import view_income_categories

finance_budget_router = Router()

async def menu_budgets(callback):
    telegram_id = callback.from_user.id

    await callback.answer()
    

    budgets = await get_budgets_from_db(telegram_id)

    if not budgets:
        return await callback.message.answer("Нет доступных бюджетов.", reply_markup=actions_kb.back_menu)

    keyboard = await create_keyboard(budgets)

    await callback.message.edit_text("Выберите бюджет:", reply_markup=keyboard)

@finance_budget_router.callback_query(F.data == 'finance_button')
async def edit_budget_handler(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()

    print(
        f" budget_id: {budget_id}")

    await callback.message.answer('Выбор категории:', reply_markup=kb.finance_budget_keyboard)

@finance_budget_router.callback_query(F.data == 'back_finance_button')
async def edit_budget_handler(callback: CallbackQuery):
    await menu_budgets(callback)

# @finance_budget_router.callback_query(F.data == 'expenses_budget_button')
# async def view_budget_router(callback: CallbackQuery):
#     await view_incomes()
