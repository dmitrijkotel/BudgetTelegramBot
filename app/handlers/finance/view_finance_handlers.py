from unicodedata import category

from aiogram import Router, F
from aiogram.types import CallbackQuery
import app.handlers.finance.keyboards.finance_budget_keyboard as kb

finance_budget_router = Router()

@finance_budget_router.callback_query(F.data == 'finance_button')
async def edit_budget_handler(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()
    await callback.message.answer('Выбор категории:', reply_markup=kb.finance_budget_keyboard)


@finance_budget_router.callback_query(F.data == 'expenses_budget_button')
async def view_budget_router(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    await callback.message.delete()
    await callback.message.answer('Выберите категорию расхода:', reply_markup=kb.view_expense_categories_keyboard)
    await callback.answer()


@finance_budget_router.callback_query(F.data == 'income_budget_button')
async def view_budget_router(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    await callback.message.delete()
    await callback.message.answer('Выберите категорию дохода:', reply_markup=kb.view_income_categories_keyboard)
    await callback.answer()