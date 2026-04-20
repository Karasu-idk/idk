
import asyncio
from SQL_part import init_db
import logging
logging.basicConfig(level=logging.INFO)
from actions import dp, bot
init_db()

#possible_choices = {
#    "1": actions.choice_1,
#    "2": actions.choice_2,
#    "3": actions.choice_3,
#    "4": exit,
#    "5": actions.choice_5,
#    "6": actions.choice_6,
#    "7": actions.choice_7,
#    "8": actions.choice_8,
#    "9": actions.choice_9,
#    "10": actions.choice_10
#}
#



async def main():
    init_db()
    print("bot running")
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())