
import asyncio
from SQL_part import init_db
import actions
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import Bot, Dispatcher, F

from pass_secret import TOKEN
bot = Bot(token=TOKEN)
init_db()

possible_choices = {
    "1": actions.choice_1,
    "2": actions.choice_2,
    "3": actions.choice_3,
    "4": exit,
    "5": actions.choice_5,
    "6": actions.choice_6,
    "7": actions.choice_7,
    "8": actions.choice_8,
    "9": actions.choice_9,
    "10": actions.choice_10
}

dp = Dispatcher()
@dp.message(CommandStart())
async def show_users(message: Message):
    text = ("/add - add user\n"
            "/show - show users\n"
            "/del - delete user\n"
            "/change - change pasw, gmail\n"
            "/forgot - forgot the password\n"
            "/logs - see logs\n"
            "/show_user_logs - show user logs\n"
            "/file_logs - file logs\n"
            "/analitics - show analitics\n")
    await message.answer(text)

async def main():
    init_db()
    print("bot running")
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())