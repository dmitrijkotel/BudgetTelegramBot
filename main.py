import asyncio
import logging

from aiogram import Bot, Dispatcher

from app.handlers.budget.create_budget_handlers import create_budget_router
from app.handlers.budget.edit_budget_directory.action_budget_directory.actions_budget_keyboards import router_actions_budget_keyboard
from app.handlers.budget.edit_budget_directory.view_budget_handlers import view_budget_router
from app.handlers.finance.add_income_categories import create_income_category_router
from app.handlers.finance.view_finance_handlers import finance_budget_router
from app.handlers.main.menu_handler import router_menu_handler
from config import TOKEN
from app.handlers.main.database.create_table_db import create_tables_db
from app.handlers.main.registration_handler import registration_router
from app.handlers.finance.view_income_categories import view_income_category_router
from app.handlers.finance.view_income_transactions_handlers import view_income_transactions_router
from app.handlers.finance.view_expenses_category import view_expenses_category_router
from app.handlers.finance.add_expenses_categories import create_expenses_category_router

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def main():
    dp.include_router(router_menu_handler)
    dp.include_router(create_budget_router)
    dp.include_router(view_budget_router)
    dp.include_router(router_actions_budget_keyboard)
    dp.include_router(finance_budget_router)
    dp.include_router(registration_router)
    dp.include_router(create_income_category_router) 
    dp.include_router(view_income_category_router)
    dp.include_router(view_income_transactions_router)
    dp.include_router(view_expenses_category_router)
    dp.include_router(create_expenses_category_router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    create_tables_db()
    logging.basicConfig(level=logging.INFO)

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Bot stopped by user.')