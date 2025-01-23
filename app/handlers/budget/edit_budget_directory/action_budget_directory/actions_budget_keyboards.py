from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from aiogram import Router, F, types
from aiogram.types import CallbackQuery
from aiogram.utils.callback_answer import CallbackAnswer

import app.handlers.budget.keyboards.budget_menu_keyboard as kb_budget
from app.handlers.budget.database.viewBudget import view_budget, get_budgets_from_db, create_keyboard

cancel_sure_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Да', callback_data='yes_button')],
    [InlineKeyboardButton(text='Назад', callback_data='back_button_sure')],
])

back_complete_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Вернуться назад', callback_data='back_button_complete_delete')],
])

back_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='Назад', callback_data='back_button')],
])

router_actions_budget_keyboard = Router()

@router_actions_budget_keyboard.callback_query(F.data == 'cancel_button')
async def create_budget(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer("Выберите действие:", reply_markup=kb_budget.budget_menu_keyboard)

@router_actions_budget_keyboard.callback_query(F.data == 'back_button_complete_delete')
async def create_budget(callback: CallbackQuery):
    telegram_id = callback.from_user.id

    await callback.answer()
    await callback.message.delete()

    budgets = await get_budgets_from_db(telegram_id)

    if not budgets:
        return await callback.message.answer("Нет доступных бюджетов.", reply_markup=back_menu)

    keyboard = await create_keyboard(budgets)

    await callback.message.answer("Выберите бюджет:", reply_markup=keyboard)
