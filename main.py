

from SQL_part import init_db
import actions

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

while True:
    print(" ")
    print("1 - add, 2 - show users, 3 - del,\n4 - quit, 5 - change, 6 - forgot the password"
          "\n7 - logs, 8 - show user logs, 9 - file logs\n10 - show analitics")

    user_choice = input("enter your choice: ")

    if user_choice in possible_choices:
        action = possible_choices[user_choice]
        action()
    else:
        print("wrong choice")

