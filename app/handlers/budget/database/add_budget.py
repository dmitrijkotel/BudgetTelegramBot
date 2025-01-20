import sqlite3

def add_budget_db(user_id, budget_name, description):
    db = sqlite3.connect('tgBotDb.db')
    cursor = db.cursor()

    try:
        cursor.execute('INSERT INTO budgets (user_id, budget_name, description) VALUES (?, ?, ?)',
                   (user_id, budget_name, description,))
        db.commit()
        db.close()
        return 'Бюджет успешно создан!'
    except ConnectionError:
        return 'Произошла ошибка, попробуйте снова!'

