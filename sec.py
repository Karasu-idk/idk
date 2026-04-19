import hashlib
import re

from pass_secret import Salt

def hash_password(password):
    salted_password = password + Salt
    return hashlib.sha256(salted_password.encode()).hexdigest()

def is_valid_password():
    while True:
        count = 0
        has_upper = False
        has_digit = False
        has_lower = False
        user_password = input("enter your password: ")
        if len(user_password) < 8:
            print("password is too short")
            continue
        for char in user_password:
            if char.isupper():
                has_upper = True
            if char.isdigit():
                has_digit = True
            if char.islower():
                has_lower = True
        if has_upper == True:
            count += 1
        if has_digit == True:
            count += 1
        if has_lower == True:
            count += 1
        if count == 1:
            print("sorry, password is easy, try again")
            continue
        if count == 2:
            print("sorry, password is middle, try again")
            continue
        if count == 3:
            print("your password is good")
            password = user_password
            return password

def check_gmail(gmail):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.fullmatch(pattern, gmail):
        return True
    else:
        return False
