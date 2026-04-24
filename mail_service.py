import secrets
import smtplib
import sqlite3
from email.message import EmailMessage
from pass_secret import EMAIL_ADDRESS, EMAIL_PASSWORD
from SQL_part import DB_NAME
sender_email = (EMAIL_ADDRESS)
email_sender_password = (EMAIL_PASSWORD)

def send_email(name):
    with sqlite3.connect(DB_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute('''SELECT gmail_id FROM idk WHERE user_name = ? ''', (name,))
        result = cursor.fetchone()
        if not result:
            return
        elif result:
            reciver_email = result[0]
            code = str(secrets.randbelow(900000) + 100000)
            msg = EmailMessage()
            msg.set_content(f"your verification code is {code}")
            msg['Subject'] = 'verification code'
            msg['From'] = sender_email
            msg['To'] = reciver_email
            try:
                with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
                    server.set_debuglevel(1)
                    server.login(sender_email, email_sender_password)
                    server.send_message(msg)
                    return code
            except Exception as e:
                print(f"error {e}")
                return None
