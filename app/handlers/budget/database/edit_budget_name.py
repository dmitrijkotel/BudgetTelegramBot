import sqlite3
import app.handlers.main.keyboards.menu_keyboard as kb

async def set_new_budget_name(message, new_name, budget_id):
    conn = sqlite3.connect('tgBotDb.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE budgets SET budget_name = ? WHERE id = ?", (new_name, budget_id))
    conn.commit()
    conn.close()
    await message.answer('Название бюджета успешно изменено!', reply_markup=kb.back_keyboard)