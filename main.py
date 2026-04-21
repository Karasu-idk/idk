
import asyncio
from SQL_part import init_db
import logging
logging.basicConfig(level=logging.INFO)
from actions import dp, bot
init_db()



async def main():
    init_db()
    print("bot running")
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())