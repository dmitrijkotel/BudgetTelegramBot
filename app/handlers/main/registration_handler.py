from aiogram import Router, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
import app.handlers.budget.keyboards.budget_menu_keyboard as kb
from app.handlers.main.database.registration_db import registration
import app.handlers.main.keyboards.registration_keyboard as reg_kb


registration_router = Router()

async def start_message(message):
    await message.answer("""
    🌟 <b>Добро пожаловать в Бюджетный Помощник!</b> 🌟

    Мы рады видеть вас здесь! Этот бот создан специально для того, чтобы помочь вам эффективно управлять вашим бюджетом и контролировать свои финансовые потоки.

    💰 <b>Что вы можете делать с нашим ботом?</b>

    1. Записывать расходы: Легко фиксируйте все свои траты, чтобы всегда быть в курсе, куда уходят ваши деньги. Просто укажите сумму и категорию расхода, и бот сохранит эту информацию для вас.

    2. Учитывать доходы: Не забывайте о своих доходах! Записывайте все поступления, чтобы иметь полное представление о своих финансах.

    3. Формировать отчеты: Получайте наглядные отчеты о ваших расходах и доходах. Это поможет вам анализировать свои финансовые привычки и принимать более обоснованные решения.

    4. Управлять бюджетом: Устанавливайте бюджетные лимиты для различных категорий расходов и следите за их выполнением. Бот напомнит вам, если вы приблизитесь к установленным границам.

    ✨ <b>Как начать?</b>

    Нажмите кнопку <b>зарегистрироваться</b>, чтобы получить список доступных команд и узнать больше о функционале бота. Мы рекомендуем начать с создания вашего первого бюджета, чтобы сразу увидеть, как легко и удобно это делать!

    📊 <i>Давайте сделаем ваши финансы более прозрачными и управляемыми вместе!</i>""", parse_mode=ParseMode.HTML)

    await message.answer('Пожалуйста, пройдите регистрацию, чтобы открыть все его возможности!', reply_markup=reg_kb.registration_keyboard)

@registration_router.callback_query(F.data == 'reg')
async def create_budget(callback: CallbackQuery):
    await callback.answer()
    await callback.message.delete()
    await callback.message.answer('Управление бюджетом', reply_markup=kb.budget_menu_keyboard)

# Обработчик команды /start
@registration_router.message(CommandStart())
async def cmd_start(message: Message):

        telegram_id = message.from_user.id
        result = registration(telegram_id)
        if result == 0:
            await start_message(message)
        else:
            await message.answer('Управление бюджетом', reply_markup=kb.budget_menu_keyboard)
