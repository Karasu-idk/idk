import sqlite3
import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.dispatcher.middlewares import data
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from SQL_part import add_user, log_func, del_user, check_password_func, changing_name, changing_gmail, see_logs, \
    show_user_log, show_users, show_analitics, init_db
from mail_service import send_email
from pass_secret import ADMIN_PASSWORD
from sec import check_gmail, is_valid_password, hash_password
from pass_secret import TOKEN

Admin_password = (ADMIN_PASSWORD)
bot = Bot(token=TOKEN)
dp = Dispatcher()

class Change(StatesGroup):
    choosing_option = State()
    waiting_for_old_name = State()
    waiting_for_pass = State()
    name_to_change = State()
    gmail_to_change = State()

class Registration(StatesGroup):
    name = State()
    gmail = State()
    password = State()

class Delete(StatesGroup):
    waiting_for_pass = State()
    waiting_for_name = State()

@dp.message(CommandStart())
async def show_commands(message: Message):
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

@dp.message(Command('add'))
async def start_add_user(message: Message, state: FSMContext):
    await state.set_state(Registration.name)
    await message.answer("Enter your name")
@dp.message(Registration.name)
async def process_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer("Enter your gmail")
    await state.set_state(Registration.gmail)
@dp.message(Registration.gmail)
async def get_gmail(message: Message, state: FSMContext):
    if check_gmail(message.text):
        await state.update_data(gmail=message.text)
        await message.answer("Enter your password")
        await state.set_state(Registration.password)
    else:
        await message.answer("wrong gmail")
@dp.message(Registration.password)
async def get_password(message: Message, state: FSMContext):
    if len(message.text) > 7:
        checked_password = is_valid_password(message.text)
        if checked_password is None:
            await message.answer("Password is too easy! Use upper, lower letters and digits")
            return
        else:
            await state.update_data(password=message.text)
            user_data = await state.get_data()
            name = user_data.get("name")
            gmail = user_data.get("gmail")
            password = user_data.get("password")
            hashed = hash_password(password)
            try:
                if add_user(name,gmail, hashed):
                    await message.answer(f"Successfully added {name}")
                with sqlite3.connect('database.db') as conn:
                    conn.execute("PRAGMA foreign_keys = ON")
                    cursor = conn.cursor()
                    cursor.execute('''SELECT user_id FROM idk WHERE user_name = ?''', (name,))
                    result = cursor.fetchone()
                    if result:
                        fetched_id = result[0]
                        log_func(fetched_id, "Was added")
            except sqlite3.IntegrityError:
                await message.answer("user already exists")
            await state.clear()
    else:
        await message.answer("password too short")
        return


@dp.message(Command('show'))
async def show_user_command(message: Message):
    user_list = show_users()
    await message.answer(user_list)

@dp.message(Command('del'))
async def delete_user(message: Message, state: FSMContext):
    await state.update_data(attempts=0)
    await state.set_state(Delete.waiting_for_pass)
    await message.answer("Enter admin password")
@dp.message(Delete.waiting_for_pass)
async def check_adm_passw(message: Message, state: FSMContext):
    data = await state.get_data()
    attempts = data.get('attempts', 0)
    if message.text == Admin_password:
        await message.answer("Password is correct\nchoose name to del:")
        choose_user_list = show_users()
        await message.answer(choose_user_list)
        await state.set_state(Delete.waiting_for_name)
    else:
        attempts += 1
        await state.update_data(attempts=attempts)
        await message.answer(f"Wrong password, attempts: {3 - attempts} ")
    if attempts >= 3:
        await message.answer("to many attempts")
        await state.clear()
@dp.message(Delete.waiting_for_name)
async def check_name(message: Message, state: FSMContext):
    name_to_del = message.text
    result_message = del_user(name_to_del)
    await message.answer(result_message)
    await state.clear()

@dp.message(Command('change'))
async def what_to_change(message: Message, state: FSMContext):
    await message.answer("1 - change name, 2 - change gmail, 3 - exit")
    await state.set_state(Change.choosing_option)
@dp.message(Change.choosing_option)
async def choose_option(message: Message, state: FSMContext):
    if message.text == "1" or message.text.lower() == "change name":
        await message.answer("Enter your name")
        await state.set_state(Change.waiting_for_old_name)
        await state.update_data(mode="change name")
    elif message.text == "2" or message.text.lower() == "change gmail":
        await message.answer("Enter your name")
        await state.set_state(Change.waiting_for_old_name)
        await state.update_data(mode="change gmail")
    elif message.text == "3" or message.text.lower() == "exit":
        await state.clear()
@dp.message(Change.waiting_for_old_name)
async def check_old_name(message: Message, state: FSMContext):
    await state.update_data(old_name=message.text)
    await state.set_state(Change.waiting_for_pass)
    await message.answer("Enter your password")
@dp.message(Change.waiting_for_pass)
async def check_pass(message: Message, state: FSMContext):
    data = await state.get_data()
    old_name = data.get('old_name')
    attempts = data.get('attempts', 0)
    mode = data.get('mode')
    db_password = check_password_func(old_name)
    if hash_password(message.text) == db_password:
        await message.answer("Password is correct")
        if mode == "change name":
            await state.set_state(Change.name_to_change)
            await message.answer("Enter your new name")
        elif mode == "change gmail":
            await state.set_state(Change.gmail_to_change)
            await message.answer("Enter your new gmail")
    else:
        await message.answer("Wrong password")
        attempts += 1
        await state.update_data(attempts=attempts)
    if attempts >= 3:
        await message.answer("to many attempts")
        await state.clear()
@dp.message(Change.name_to_change)
async def change_name(message: Message, state: FSMContext):
    new_name = message.text
    data = await state.get_data()
    old_name = data.get('old_name')
    if changing_name(old_name, new_name):
        await message.answer(f"Successfully changed your name to {new_name}")
        await state.clear()
    else:
        await message.answer(f"User already exists")
        await state.clear()
@dp.message(Change.gmail_to_change)
async def change_gmail(message: Message, state: FSMContext):
    new_gmail = message.text
    data = await state.get_data()
    old_name = data.get('old_name')
    if check_gmail(message.text):
        if changing_gmail(old_name, new_gmail):
            await message.answer(f"Successfully changed your gmail to {new_gmail}")
            await state.clear()
        else:
            await message.answer(f"gmail already exists")
    else:
        await message.answer("Wrong gmail")
        await state.clear()
#def choice_5():
#    user_choice = input("1 - change name, 2 - change gmail, 3 - exit ")
#    if user_choice == "1":
#        name = input("enter your name: ")
#        if check_password_func(name):
#            new_name = input("enter new name: ")
#            if changing_name(name, new_name):
#                print(f"Success, new name: {new_name}")
#            else:
#                print("User already exists")
#        else:
#            print("wrong password")
#    elif user_choice == "2":
#        name = input("enter your name: ")
#        if check_password_func(name):
#            new_gmail = input("enter new gmail: ")
#            if check_gmail(new_gmail):
#                if changing_gmail(name, new_gmail):
#                    print(f"Success, new gmail: {new_gmail}")
#                else:
#                    print("gmail already exists")
#            else:
#                print("wrong gmail")
#        else:
#            print("wrong password")
#    elif user_choice == "3":
#        return
#    else:
#        print("wrong choice")

def choice_6():
    user_name = input("enter your name or exit: ")
    if user_name == "exit":
        return
    else:
        sent_code = send_email(user_name)
        if sent_code:
            check_code = input("enter your verification code: ")
            if check_code == sent_code:
                print("Success")
                clean_password = is_valid_password()
                hashed = hash_password(clean_password)
                with sqlite3.connect('database.db') as conn:
                    cursor = conn.cursor()
                    cursor.execute('''UPDATE idk SET password = ? WHERE user_name = ?  ''', (hashed, user_name))
                    conn.commit()
                    print(f"password changed please remember it")
                    cursor.execute('''SELECT user_id FROM idk WHERE user_name = ?''', (user_name, ))
                    result = cursor.fetchone()
                    if result:
                        fetched_id = result[0]
                        log_func(fetched_id, "Reseted passw")
            else:
                print("wrong code")
        else:
            print("Failed to send email or user not found")

def choice_7():
    attempts = 0
    while True:
        if attempts > 3:
            print("sorry, you are out of attempts")
            break
        user_admpassword = input("enter your password: ")
        if user_admpassword == Admin_password:
            see_logs()
            return
        else:
            print("wrong password")
            attempts += 1

def choice_8():
    attempts = 0
    while True:
        if attempts > 3:
            print("sorry, you are out of attempts")
            break
        user_admpassword = input("enter your password: ")
        if user_admpassword == Admin_password:
            user_name = input("enter name: ")
            show_user_log(user_name)
            return
        else:
            print("wrong password")
            attempts += 1

def choice_9():
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute(''' SELECT * FROM logs''')
        result = cursor.fetchall()
        with open("report.txt", "w") as file:
            for row in result:
                file.write(f"log: {row}\n")
    print("Success")
def choice_10():
    show_analitics()

async def main():
    init_db()
    print("bot running")
    await dp.start_polling(bot)
if __name__ == "__main__":
    asyncio.run(main())