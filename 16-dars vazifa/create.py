import sqlite3

connection = sqlite3.connect("sqlite.dp")

cursor = connection.cursor()

command = """
CREATE TABLE IF NOT EXISTS USERS(
first_name TEXT,
last_name TEXT,
phone_number TEXT,
telegram_id NUMBER unique,
my_photo TEXT,
me_email TEXT,
address TEXT,
yosh_1 NUMBER
);

"""

cursor.execute(command)

connection.commit()