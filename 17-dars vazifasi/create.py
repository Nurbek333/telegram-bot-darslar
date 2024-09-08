import sqlite3
connection  = sqlite3.connect("aqulite.db")

cursor = connection.cursor()

command = """
CREATE TABLE IF NOT EXISTS USERS(
first_name TEXT,
last_name TEXT,
phone_number TEXT,
telegram_id NUMBER unique,
address TEXT,
home_number NUMBER,
age NUMBER,
sinf NUMBER,
hobby TEXT,
fruit TEXT

);
"""
cursor.execute(command)

connection.commit()
