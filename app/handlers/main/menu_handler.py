from aiogram import Router, F
from aiogram.types import CallbackQuery
import app.handlers.budget.keyboards.budget_menu_keyboard as kb_budget
from aiogram.fsm.state import State, StatesGroup

router_menu_handler = Router()

@router_menu_handler.callback_query(F.data == 'cancel_button')
async def create_budget(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer("Выберите действие:", reply_markup=kb_budget.budget_menu_keyboard)

@router_menu_handler.callback_query(F.data == 'back_button')
async def create_budget(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer("Выберите действие:", reply_markup=kb_budget.budget_menu_keyboard)