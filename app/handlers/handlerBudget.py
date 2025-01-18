from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup
import app.keyboards.keyboardBudget as kb
import app.keyboards.keyboardMain as kbMain
from aiogram.fsm.state import State, StatesGroup

from app.database.budget.actionsBudget import get_budget_details, delete_budget
from app.database.budget.addBudget import addBudget
from app.database.budget.edit_budget_description import set_new_budget_description
from app.database.budget.edit_budget_name import set_new_budget_name
from app.database.budget.viewBudget import view_budget

routerBudget = Router()


class BudgetStates(StatesGroup):
    waiting_for_budget_title = State()
    waiting_for_budget_description = State()

    waiting_for_new_name = State()
    waiting_for_budget_new_description = State()




@routerBudget.callback_query(F.data == 'create_budget')
async def create_budget(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    # Отправляем сообщение с просьбой ввести название бюджета и сохраняем идентификатор
    bot_message = await callback.message.answer("Введите название для бюджета:", reply_markup=kb.cancelKeyboard)
    await state.update_data(bot_message_id=bot_message.message_id)
    await state.set_state(BudgetStates.waiting_for_budget_title)
    await callback.answer()


@routerBudget.message(BudgetStates.waiting_for_budget_title)
async def process_budget_title(message: Message, state: FSMContext):
    budget_name = message.text
    await state.update_data(budget_name=budget_name)  # Сохраняем название бюджета в состоянии
    await message.delete()  # Удаляем сообщение пользователя

    # Получаем идентификатор сообщения бота и удаляем его
    user_data = await state.get_data()
    bot_message_id = user_data.get('bot_message_id')
    await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)

    bot_message = await message.answer("Введите описание бюджета :", reply_markup=kb.addBudgetDescriptionKeyboard)
    await state.update_data(bot_message_id=bot_message.message_id)
    await state.set_state(BudgetStates.waiting_for_budget_description)





@routerBudget.callback_query(F.data == 'skip_button')
async def skip(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # Подтверждаем нажатие кнопки
    await callback.message.delete()  # Удаляем сообщение с кнопкой

    # Получаем данные состояния
    user_data = await state.get_data()
    budget_name = user_data.get('budget_name')  # Получаем название бюджета

    # Сохраняем пустое описание в состоянии
    description = ''
    await state.update_data(description=description)

    # Здесь добавляем логику добавления бюджета в базу данных
    telegram_id = callback.from_user.id
    result = addBudget(telegram_id, budget_name, description)

    await callback.message.answer(result, reply_markup=kbMain.mainKeyboard)
    await state.clear()  # Очистка состояния после успешного создания бюджета


@routerBudget.message(BudgetStates.waiting_for_budget_description)
async def process_budget_description(message: Message, state: FSMContext):
    user_data = await state.get_data()  # Получаем данные состояния
    bot_message_id = user_data.get('bot_message_id')

    if user_data.get('description') == '':
        # Если описание уже пустое (т.е. нажата кнопка "Skip")
        await message.answer("Описание бюджета пропущено.", reply_markup=kbMain.mainKeyboard)
    else:
        # Обработка введенного описания
        description = message.text
        await state.update_data(description=description)  # Сохраняем описание
        await message.delete()  # Удаляем сообщение пользователя

        # Удаляем сообщение бота, если есть
        if bot_message_id is not None:
            await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)

        budget_name = user_data.get('budget_name')  # Получаем название бюджета
        telegram_id = message.from_user.id
        result = addBudget(telegram_id, budget_name, description)

        await message.answer(result, reply_markup=kbMain.mainKeyboard)
    await state.clear()  # Очистка состояния после успешного создания бюджета







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





@routerBudget.callback_query(F.data == 'view_budget')
async def view_budget_router(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    await callback.message.delete()
    await view_budget(callback.message, telegram_id)  # Предполагается, что эта функция получает все бюджеты для конкретного пользователя
    await callback.answer()

# Глобальная переменная budget_id
budget_id = None

@routerBudget.callback_query(lambda call: call.data.isdigit())
async def handle_budget_selection(callback: CallbackQuery):
    global budget_id  # Используем глобальную переменную
    budget_id = int(callback.data)  # Присваиваем значение

    budget_details = await get_budget_details(budget_id)  # Функция, которую нужно реализовать
    if budget_details:
        budget_name, description = budget_details
        response_message = f"{budget_name}\nОписание: {description}" if description else f"{budget_name}\n"
    else:
        response_message = "Бюджет не найден."

    await callback.message.delete()
    await callback.answer()  # Оповещение об успешном нажатии на кнопку
    await callback.message.answer(response_message, reply_markup=kb.actionsBudget)  # Отправляем сообщение с деталями бюджета

@routerBudget.callback_query(F.data == 'delete_budget_button')
async def delete_budget_handler(callback: CallbackQuery):
    global budget_id  # Указываем, что будем использовать глобальную переменную

    if budget_id is None:
        await callback.answer("Выберите бюджет для удаления.", show_alert=True)
        return

    await callback.message.delete()
    await callback.answer()

    # Удаляем бюджет по ID
    await delete_budget(budget_id, callback.message)  # Теперь передаем бюджет_id
    budget_id = None  # Сбрасываем budget_id после операции




@routerBudget.callback_query(F.data == 'edit_budget_button')
async def edit_budget_handler(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()
    await callback.message.answer('Что желаете изменить?', reply_markup=kb.edit_budget_keyboard)  # Отправляем сообщение с деталями бюджета


@routerBudget.callback_query(F.data == 'edit_title_budget_button')
async def red_name_budget(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    # Отправляем сообщение с просьбой ввести название бюджета и сохраняем идентификатор
    bot_message = await callback.message.answer("Введите название для бюджета:", reply_markup=kb.cancelKeyboard)
    await state.update_data(bot_message_id=bot_message.message_id)
    await state.set_state(BudgetStates.waiting_for_new_name)
    await callback.answer()


@routerBudget.message(BudgetStates.waiting_for_new_name)
async def process_budget_title(message: Message, state: FSMContext):
    budget_name = message.text
    await state.update_data(budget_name=budget_name)  # Сохраняем название бюджета в состоянии
    await message.delete()  # Удаляем сообщение пользователя

    # Получаем идентификатор сообщения бота и удаляем его
    user_data = await state.get_data()
    bot_message_id = user_data.get('bot_message_id')
    await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    await set_new_budget_name(message, budget_name, budget_id)


@routerBudget.callback_query(F.data == 'edit_description_button')
async def red_name_budget(callback: CallbackQuery, state: FSMContext):
    global budget_id  # Указываем, что будем использовать глобальную переменную

    await callback.message.delete()

    # Отправляем сообщение и сохраняем идентификатор сообщения
    bot_message = await callback.message.answer("Введите описание для бюджета:", reply_markup=kb.cancelKeyboard)
    await state.update_data(bot_message_id=bot_message.message_id)

    # Проверяем, что budget_id был установлен ранее
    if budget_id is None:
        await callback.answer("Id бюджета не найден. Пожалуйста, выберите бюджет для редактирования.", show_alert=True)
        return

    await state.set_state(BudgetStates.waiting_for_budget_new_description)
    await callback.answer()


@routerBudget.message(BudgetStates.waiting_for_budget_new_description)
async def process_budget_description(message: Message, state: FSMContext):
    global budget_id  # Указываем использование глобальной переменной budget_id

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
                             reply_markup=kb.backKeyboard)





@routerBudget.callback_query(F.data == 'finance_button')
async def edit_budget_handler(callback: CallbackQuery):
    await callback.message.delete()
    await callback.answer()
    await callback.message.answer('Выбор категории:', reply_markup=kb.finance_budget_keyboard)


@routerBudget.callback_query(F.data == 'expenses_budget_button')
async def view_budget_router(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    await callback.message.delete()
    await callback.message.answer('Выберите категорию расхода:', reply_markup=kb.cancelKeyboard)
    await callback.answer()


@routerBudget.callback_query(F.data == 'income_budget_button')
async def view_budget_router(callback: CallbackQuery):
    telegram_id = callback.from_user.id
    await callback.message.delete()
    await callback.message.answer('Выберите категорию дохода:', reply_markup=kb.cancelKeyboard)
    await callback.answer()