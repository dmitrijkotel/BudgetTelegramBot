import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.handlers.main.menu_handler import router_menu_handler
from config import TOKEN
from app.handlers.main.database.create_table_db import create_tables_db


bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    # Регистрация роутеров
    dp.include_router()
    dp.include_router(router_menu_handler)

    # Запуск бота с поллингом
    await dp.start_polling(bot)

if __name__ == '__main__':
    # Создаем таблицы в базе данных перед запуском
    create_tables_db()
    logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped by user.')