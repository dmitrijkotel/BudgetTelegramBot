import sqlite3
import aiosqlite
import app.handlers.budget.edit_budget_directory.edit_budet_directory.edit_budget_keyboards as kb

async def set_new_budget_description(message, new_description, budget_id, bot_message_id):
    async with aiosqlite.connect('tgBotDb.db') as db:
        try:
            async with db.execute("UPDATE budgets SET description = ? WHERE id = ?", (new_description, budget_id)) as cursor:
                await db.commit()  # Формат commit в асинхронном режиме

            # Редактируем сообщение бота
            await message.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=bot_message_id,
                text='Описание бюджета успешно изменено!',
                reply_markup=kb.back_complete_edit_description_keyboard
            )
        except (sqlite3.Error, aiosqlite.Error) as e:  # Обработка ошибок базы данных
            print(f"Ошибка базы данных: {e}")  # Логирование ошибки

            # Редактируем сообщение бота в случае ошибки
            await message.bot.edit_message_text(
                chat_id=message.chat.id,
                message_id=bot_message_id,
                text='Произошла ошибка при обновлении описания бюджета. Попробуйте снова.',
                reply_markup=kb.back_complete_edit_description_keyboard
            )