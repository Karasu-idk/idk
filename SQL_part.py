import sqlite3
from sec import hash_password, check_gmail
DB_NAME = 'database.db'
def init_db():
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute(''' 
            CREATE TABLE IF NOT EXISTS idk (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_name TEXT NOT NULL UNIQUE,
                gmail_id TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
            ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS logs (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                action TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY(user_id) REFERENCES idk (user_id) ON DELETE CASCADE
            )
            ''')
        conn.commit()

def add_user(user_name, gmail, password):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''INSERT into idk (user_name, gmail_id, password) VALUES (?, ?, ?)''', ( user_name, gmail, password ))
        conn.commit()
        return True

def show_users():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(''' SELECT * FROM idk ''')
        users = cursor.fetchall()
        if not users:
            return "No users"
        response = "list of users\n"
        for user in users:
            response += (f"Id: {user[0]}\n")
            response += (f"Name: {user[1]}\n")
            response += (f"Gmail: {user[2]}\n")
            response += ("-------------------------\n")
        return response

def del_user(user_name):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute('PRAGMA foreign_keys = ON')
        cursor = conn.cursor()
        cursor.execute('''DELETE FROM idk WHERE user_name = ?''', (user_name,))
        conn.commit()
        if cursor.rowcount > 0:
            return f"user {user_name} has been deleted"
        else:
            return f"user {user_name} does not exist"

def check_password_func(name):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute(''' SELECT password FROM idk WHERE user_name = ? ''', (name,))
        db_result = cursor.fetchone()
        if not db_result:
            return None
        else:
            return db_result[0]

def changing_name(old_name, new_name):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''UPDATE idk SET user_name = ? WHERE user_name = ? ''', (new_name, old_name))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

def changing_gmail(name, new_gmail):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute('''UPDATE idk SET gmail_id = ? WHERE user_name = ? ''', (new_gmail, name))
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False



def log_func(user_id, action):
    with sqlite3.connect(DB_NAME) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cursor = conn.cursor()
        cursor.execute('''INSERT INTO logs (user_id, action) VALUES (?, ?)''', (user_id, action))
        conn.commit()
def reset_passw(hashed, user_name):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''UPDATE idk SET password = ? WHERE user_name = ?  ''', (hashed, user_name))
        conn.commit()
        cursor.execute('''SELECT user_id FROM idk WHERE user_name = ?''', (user_name, ))
        result = cursor.fetchone()
        if result:
            fetched_id = result[0]
            log_func(fetched_id, "Reseted passw")

def see_logs():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM logs''')
        result = cursor.fetchall()
        if not result:
            return "no logs"
        else:
            response = "list of logs\n"
            for row in result:
                response += (f"Num {row[0]}\n")
                response += (f"user ID: {row[1]}\n")
                response += (f"Action: {row[2]}\n")
                response += ("---------------------\n")
            return response

def show_user_log(name):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            SELECT idk.user_name, logs.action, logs.timestamp
            FROM idk
            JOIN logs ON idk.user_id = logs.user_id
            WHERE idk.user_name = ?
        ''', (name,))
        result = cursor.fetchall()
        if not result:
            return "no logs"
        else:
            response = "list of logs\n"
            for row in result:
                response += (f"Name {row[0]}\n")
                response += (f"Action: {row[1]}\n")
                response += (f"Timestamp: {row[2]}\n")
            return response

def show_analytics():
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT COUNT(user_id) FROM idk''')
        result_users = cursor.fetchone()
        cursor.execute('''SELECT COUNT(*) FROM logs WHERE action = "Reseted passw"''')
        result_actions = cursor.fetchone()
        cursor.execute('''SELECT COUNT(*) FROM logs WHERE date(timestamp) = date("now")''')
        result_dates = cursor.fetchone()
        response = "analytics\n"
        response += f"Total users: {result_users[0]}\n"
        response += f"Total password resets: {result_actions[0]}\n"
        response += f"Actions today: {result_dates[0]}\n"
        return response
