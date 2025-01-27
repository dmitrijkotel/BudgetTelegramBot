import sqlite3

def create_tables_db():
    # Подключаемся к базе данных (или создаем ее, если она не существует)
    db = sqlite3.connect('tgBotDb.db')
    cursor = db.cursor()

    # Создание таблицы пользователей
    cursor.execute('''  
    CREATE TABLE IF NOT EXISTS users (  
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        telegram_id INTEGER UNIQUE NOT NULL  
    )''')

    # Создание таблицы бюджетов
    cursor.execute("""  
    CREATE TABLE IF NOT EXISTS budgets (  
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        user_id INTEGER NOT NULL,  
        budget_name TEXT NOT NULL,  
        description TEXT,  
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
        FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE  
    );  
    """)

    cursor.execute("""  
        CREATE TABLE IF NOT EXISTS categories (  
            id INTEGER PRIMARY KEY AUTOINCREMENT,  
            budget_id INTEGER NOT NULL,  
            name TEXT NOT NULL,  
            description TEXT,
            type TEXT NOT NULL CHECK (type IN ('income', 'expense')),  
            limit_amount CHECK (limit_amount >= 0),  -- Ограничение по деньгам, неотрицательное значение  
            FOREIGN KEY (budget_id) REFERENCES budgets(id) ON DELETE CASCADE  
        );  
    """)

    # Создание таблицы расходов
    cursor.execute("""  
    CREATE TABLE IF NOT EXISTS expenses (  
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        budget_id INTEGER NOT NULL,  
        category_id INTEGER NOT NULL,  
        amount REAL NOT NULL,  
        date TEXT NOT NULL,  
        description TEXT,  
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE  
    );  
    """)

    # Создание таблицы доходов
    cursor.execute("""  
    CREATE TABLE IF NOT EXISTS income (  
        id INTEGER PRIMARY KEY AUTOINCREMENT,  
        budget_id INTEGER NOT NULL,  
        category_id INTEGER NOT NULL,  
        amount REAL NOT NULL,  
        date TEXT NOT NULL,  
        description TEXT,  
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,  
        FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE  
    );  
    """)

    # Сохраняем изменения и закрываем соединение
    db.commit()
    db.close()