from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
import app.handlers.budget.keyboards.budget_menu_keyboard as kb
from app.handlers.main.database.registration_db import registration
import app.handlers.main.keyboards.registration_keyboard as reg_kb


registration_router = Router()

async def start_message(message):

    await message.answer('Пожалуйста, пройдите регистрацию, чтобы открыть все его возможности!', reply_markup=reg_kb.registration_keyboard)

@registration_router.callback_query(F.data == 'reg')
async def create_budget(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text('Управление бюджетом', reply_markup=kb.budget_menu_keyboard)

# Обработчик команды /start
@registration_router.message(CommandStart())
async def cmd_start(message: Message):

        telegram_id = message.from_user.id
        result = registration(telegram_id)
        if result == 0:
            await start_message(message)
        else:
            await message.answer('Управление бюджетом', reply_markup=kb.budget_menu_keyboard)