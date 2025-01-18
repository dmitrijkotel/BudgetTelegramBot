import sqlite3
import aiosqlite
import app.keyboards.keyboardBudget as kb


async def get_budget_details(budget_id):
    async with aiosqlite.connect('tgBotDb.db') as db:
        async with db.execute("SELECT budget_name, description FROM budgets WHERE id = ?", (budget_id,)) as cursor:
            budget = await cursor.fetchone()  # Получаем детали бюджета
    return budget


async def delete_budget(budget_id, message):
    async with aiosqlite.connect('tgBotDb.db') as db:
        try:
            # Проверка существования бюджета с данным budget_id
            async with db.execute("SELECT id FROM budgets WHERE id = ?", (budget_id,)) as cursor:
                budget_exists = await cursor.fetchone()
                if not budget_exists:
                    await message.answer("Бюджет не найден!", reply_markup=kb.backKeyboard)
                    return

                    # Удаление бюджета
            async with db.execute("DELETE FROM budgets WHERE id = ?", (budget_id,)) as cursor:
                await db.commit()
                await message.answer('Бюджет успешно удалён!',
                                     reply_markup=kb.backKeyboard)  # Сообщение об успешном удалении

        except (sqlite3.Error, aiosqlite.Error) as e:  # Ловим ошибки базы данных
            print(f"Ошибка базы данных: {e}")  # Выводим ошибку в консоль
            await message.answer('Произошла ошибка, попробуйте снова!', reply_markup=kb.backKeyboard)