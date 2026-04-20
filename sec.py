import hashlib
import re

from pass_secret import Salt

def hash_password(password):
    salted_password = password + Salt
    return hashlib.sha256(salted_password.encode()).hexdigest()

def is_valid_password(user_password):
    count = 0
    has_upper = False
    has_digit = False
    has_lower = False
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
    if count == 1 or count == 2:
        return None
    if count == 3:
        password = user_password
        return password
def check_gmail(gmail):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if re.fullmatch(pattern, gmail):
        return True
    else:
        return False
