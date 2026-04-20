import sqlite3
import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
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

class Registration(StatesGroup):
    name = State()
    gmail = State()
    password = State()

def choice_1():
    set_name_input = input("enter your name: ")
    set_gmail_input = input("enter your gmail: ")
    if check_gmail(set_gmail_input):
        clean_password = is_valid_password()
        hashed = hash_password(clean_password)
        try:
            add_user(set_name_input, set_gmail_input, hashed)
            with sqlite3.connect('database.db') as conn:
                conn.execute("PRAGMA foreign_keys = ON")
                cursor = conn.cursor()
                cursor.execute('''SELECT user_id FROM idk WHERE user_name = ?''', (set_name_input,))
                result = cursor.fetchone()
                if result:
                    fetched_id = result[0]
                    log_func(fetched_id, "Was added")
        except sqlite3.IntegrityError:
            print("user already exists")
    else:
        print("wrong email")

def choice_2():
    show_users()

def choice_3():
    attempts = 0
    while True:
        if attempts > 3:
            print("sorry, you are out of attempts")
            break
        user_admpassword = input("enter your password: ")
        if user_admpassword == Admin_password:
            with sqlite3.connect('database.db') as conn:
                cursor = conn.cursor()
                cursor.execute(''' SELECT * FROM idk ''')
                users = cursor.fetchall()
                if not users:
                    print("no users")
                    return
                for user in users:
                    print("-" * 20)
                    print(f"Id: {user[0]}")
                    print(f"user name: {user[1]}")
            name_to_del = input("enter user name: ")
            del_user(name_to_del)
            break
        else:
            print("wrong password")
            attempts += 1

def choice_5():
    user_choice = input("1 - change name, 2 - change gmail, 3 - exit ")
    if user_choice == "1":
        name = input("enter your name: ")
        if check_password_func(name):
            new_name = input("enter new name: ")
            if changing_name(name, new_name):
                print(f"Success, new name: {new_name}")
            else:
                print("User already exists")
        else:
            print("wrong password")
    elif user_choice == "2":
        name = input("enter your name: ")
        if check_password_func(name):
            new_gmail = input("enter new gmail: ")
            if check_gmail(new_gmail):
                if changing_gmail(name, new_gmail):
                    print(f"Success, new gmail: {new_gmail}")
                else:
                    print("gmail already exists")
            else:
                print("wrong gmail")
        else:
            print("wrong password")
    elif user_choice == "3":
        return
    else:
        print("wrong choice")

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

