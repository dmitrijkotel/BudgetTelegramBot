from aiogram import Router, F  
from aiogram.types import CallbackQuery, Message, InlineKeyboardButton  
from aiogram.fsm.context import FSMContext  
from aiogram.utils.keyboard import InlineKeyboardBuilder  
from aiogram.fsm.state import State, StatesGroup  
import aiosqlite  
from datetime import datetime  
from app.handlers.finance.view_finance_handlers import menu_budgets  

view_income_transactions_router = Router()  

class Form(StatesGroup):  
    waiting_for_amount = State()  
    waiting_for_description = State()  

async def get_income_transactions_from_db(category_id: int):  
    async with aiosqlite.connect('tgBotDb.db') as conn:  
        async with conn.execute(  
            """SELECT id, amount, date   
               FROM income   
               WHERE category_id = ?   
               ORDER BY date DESC""",  
            (category_id,)  
        ) as cursor:  
            return await cursor.fetchall()  

async def create_income_transactions_keyboard(transactions: list):  
    keyboard = InlineKeyboardBuilder()  

    # Добавляем каждую транзакцию в отдельную строку  
    for transaction in transactions:  
        trans_id, amount, date = transaction  
        button_text = f"{date} - {amount}₽"  
        keyboard.add(InlineKeyboardButton(text=button_text, callback_data=f"transaction_{trans_id}"))  # Каждую кнопка добавляется на новую строку  

    # Если количество категорий четное, мы можем добавить их по 2 в ряд, иначе по 1
    if len(transactions) % 2 == 0:
        keyboard.adjust(2)  # 2 кнопки в ряд
    else:
        keyboard.adjust(1)  # 1 кнопка в ряд
    # Добавляем кнопку "Назад" и "Добавить транзакцию" в одной строке внизу  
    keyboard.row(  
        InlineKeyboardButton(text="Назад", callback_data="back_income_transactions_button"),  
        InlineKeyboardButton(text="Добавить транзакцию", callback_data="add_income_transaction_button")  
    )  

    return keyboard.as_markup()

async def view_income_transactions(message: Message, category_id: int, state: FSMContext):  
    transactions = await get_income_transactions_from_db(category_id)  
    keyboard = await create_income_transactions_keyboard(transactions)  

    if not transactions:  
        await message.answer("Нет транзакций в этой категории.", reply_markup=keyboard)  
    else:  
        await message.answer("Список транзакций доходов:", reply_markup=keyboard)  

@view_income_transactions_router.callback_query(F.data == 'back_income_transactions_button')  
async def back_to_categories_handler(callback: CallbackQuery, state: FSMContext):  
    await menu_budgets(callback)   

@view_income_transactions_router.callback_query(F.data.startswith('category_'))  
async def handle_category_selection(callback: CallbackQuery, state: FSMContext):  
    try:  
        category_id = int(callback.data.split('_')[1])  
        await state.update_data(category_id=category_id)  
        await callback.message.delete()  
        await view_income_transactions(callback.message, category_id, state)  
    except (ValueError, IndexError) as e:  
        await callback.answer("Ошибка загрузки транзакций")  
        print(f"Error: {e}")  

async def get_transaction_details_db(transaction_id: int):  
    async with aiosqlite.connect('tgBotDb.db') as db:  
        async with db.execute("""  
            SELECT income.amount, income.date, income.description, categories.name  
            FROM income  
            JOIN categories ON income.category_id = categories.id  
            WHERE income.id = ?  
            """, (transaction_id,)) as cursor:  
            return await cursor.fetchone()   

transaction_detail_keyboard = InlineKeyboardBuilder()  
transaction_detail_keyboard.add(InlineKeyboardButton(text='Назад', callback_data='back_from_transaction_detail'))  

@view_income_transactions_router.callback_query(F.data.startswith('transaction_'))  
async def show_transaction_detail(callback: CallbackQuery):  
    transaction_id = int(callback.data.split('_')[1])  
    transaction = await get_transaction_details_db(transaction_id)  

    if transaction:  
        amount, date, description, category = transaction  
        response = (  
            f"Категория: {category}\n"  
            f"Сумма: {amount}₽\n"  
            f"Дата: {date}\n"  
            f"Описание: {description or 'нет описания'}"  
        )  
    else:  
        response = "Транзакция не найдена"  

    # Создаем клавиатуру с кнопками "Назад" и "Удалить транзакцию"
    transaction_detail_keyboard = InlineKeyboardBuilder()  
    transaction_detail_keyboard.add(InlineKeyboardButton(text='Назад', callback_data='back_from_transaction_detail'))  
    transaction_detail_keyboard.add(InlineKeyboardButton(text='Удалить', callback_data=f'delete_transaction_{transaction_id}'))  

    await callback.message.edit_text(response, reply_markup=transaction_detail_keyboard.as_markup())  
    await callback.answer()  

@view_income_transactions_router.callback_query(F.data.startswith('delete_transaction_'))  
async def delete_transaction_handler(callback: CallbackQuery):  
    try:  
        # Получаем ID транзакции из callback_data
        transaction_id = int(callback.data.split('_')[2])  

        async with aiosqlite.connect('tgBotDb.db') as conn:  
            await conn.execute("DELETE FROM income WHERE id = ?", (transaction_id,))  
            await conn.commit()

        await callback.message.edit_text("Транзакция успешно удалена.", reply_markup=create_return_keyboard())  
    except (ValueError, IndexError) as e:  
        await callback.answer("Ошибка: не удалось удалить транзакцию.")  
        print(f"Ошибка при удалении транзакции: {e}")  
    await callback.answer()

@view_income_transactions_router.callback_query(F.data == 'add_income_transaction_button')  
async def add_income_transaction_handler(callback: CallbackQuery, state: FSMContext):  
        await callback.message.delete()  

        user_data = await state.get_data()  
        category_id = user_data.get('category_id')  

        if category_id is None:  
            await callback.answer("Ошибка: идентификатор категории не найден.")  
            return  

        bot_message = await callback.message.answer("Введите сумму транзакции:")  
        await state.update_data(bot_message_id=bot_message.message_id, category_id=category_id)  
        await state.set_state(Form.waiting_for_amount)  
        await callback.answer()  

@view_income_transactions_router.message(Form.waiting_for_amount)  
async def process_amount(message: Message, state: FSMContext):  
    user_data = await state.get_data()  
    category_id = user_data.get('category_id')  

    try:  
        amount = float(message.text)  
        await state.update_data(amount=amount)  

        # Удаляем сообщение с запросом суммы  
        await message.delete()  
        bot_message_id = user_data.get('bot_message_id')  

        if bot_message_id is not None:  
            await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)  

        # Запрашиваем ввод описания транзакции  
        bot_message = await message.answer("Введите описание транзакции:")  
        await state.update_data(bot_message_id=bot_message.message_id)  
        await state.set_state(Form.waiting_for_description)  

    except ValueError:  
        await message.answer("Пожалуйста, введите корректную сумму.")  

@view_income_transactions_router.message(Form.waiting_for_description)  
async def create_income_transaction_description(message: Message, state: FSMContext):  
    user_data = await state.get_data()  
    amount = user_data.get('amount')  
    category_id = user_data.get('category_id')  
    description = message.text or ''  # Если описание пустое, заменяем на пустую строку  
    transaction_date = datetime.now().strftime("%d-%m-%Y %H:%M:%S")  

    bot_message_id = user_data.get('bot_message_id')  

    if bot_message_id is not None:  
        await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)  

    try:  
        async with aiosqlite.connect('tgBotDb.db') as conn:  
            await conn.execute(  
                """INSERT INTO income (amount, description, category_id, date)   
                VALUES (?, ?, ?, ?)""",  
                (amount, description, category_id, transaction_date)  
            )  
            await conn.commit()  
            await message.answer("Транзакция выполнена успешно!", reply_markup=create_return_keyboard())  
    except Exception as e:  
        print(f"Ошибка при добавлении транзакции в БД: {e}")  
        await message.answer("Произошла ошибка при добавлении транзакции. Пожалуйста, попробуйте еще раз.")  

    await state.clear()  # Очищаем состояние после добавления транзакции  

def create_return_keyboard():  
    keyboard = InlineKeyboardBuilder()  
    keyboard.add(InlineKeyboardButton(text="Вернуться", callback_data="return_to_budgets"))  
    return keyboard.as_markup()  

@view_income_transactions_router.callback_query(F.data == "return_to_budgets")  
async def return_to_budgets_handler(callback: CallbackQuery, state: FSMContext):  
    await menu_budgets(callback)  # Возвращаем в меню бюджетов  

@view_income_transactions_router.callback_query(F.data == 'back_from_transaction_detail')  
async def back_to_transactions_handler(callback: CallbackQuery, state: FSMContext):  
    user_data = await state.get_data()  
    category_id = user_data.get('category_id')  

    if category_id is not None:  
        await callback.message.delete()  
        await view_income_transactions(callback.message, category_id, state)  
    else:  
        await callback.answer("Ошибка: идентификатор категории не найден.")