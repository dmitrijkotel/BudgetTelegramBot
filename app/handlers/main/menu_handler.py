from aiogram import Router, F
from aiogram.types import CallbackQuery
import app.handlers.budget.keyboards.budget_menu_keyboard as kbMain
from aiogram.fsm.state import State, StatesGroup

routerBudget = Router()


class BudgetStates(StatesGroup):
    waiting_for_new_name = State()
    waiting_for_budget_new_description = State()


@routerBudget.callback_query(F.data == 'cancel_button')
async def create_budget(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer("Выберите действие:", reply_markup=kbMain.mainKeyboard)

@routerBudget.callback_query(F.data == 'back_button')
async def create_budget(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer("Выберите действие:", reply_markup=kbMain.mainKeyboard)