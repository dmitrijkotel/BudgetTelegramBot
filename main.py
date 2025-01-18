import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.handlers.handlerBudget import routerBudget
from app.handlers.handlerReg import routerReg
from config import TOKEN
from app.database.tables import createTables

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    # Регистрация роутеров
    dp.include_router(routerReg)
    dp.include_router(routerBudget)

    # Запуск бота с поллингом
    await dp.start_polling(bot)

if __name__ == '__main__':
    # Создаем таблицы в базе данных перед запуском
    createTables()
    logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped by user.')