import asyncio
from aiogram import Bot, Dispatcher
from databases.user_database import user_database
from handlers.user_handlers import user_router
from common.token import TOKEN
from middlewares.throttling import ThrottlingMiddleware

bot = Bot(token=TOKEN)
dp = Dispatcher()
db = user_database()

dp.include_router(user_router)
dp.update.middleware(ThrottlingMiddleware())


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
