import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.handlers.budget.create_budget_handlers import create_budget_router
from app.handlers.budget.edit_budget_directory.view_budget_handlers import view_budget_router
from app.handlers.finance.view_finance_handlers import finance_budget_router
from app.handlers.main.menu_handler import router_menu_handler
from config import TOKEN
from app.handlers.main.database.create_table_db import create_tables_db
from app.handlers.main.registration_handler import registration_router

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router_menu_handler)
    dp.include_router(create_budget_router)
    dp.include_router(view_budget_router)
    dp.include_router(finance_budget_router)
    dp.include_router(registration_router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    create_tables_db()
    logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped by user.')