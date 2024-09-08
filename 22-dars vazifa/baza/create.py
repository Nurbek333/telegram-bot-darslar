import sqlite3


def users_db():
    connection = sqlite3.connect("sqlite.db")

    cursor = connection.cursor()

    #photo,address,username
    command = """
    CREATE TABLE IF NOT EXISTS USERS(
    full_name TEXT,
    telegram_id NUMBER unique
    );
    """

    cursor.execute(command)

    connection.commit()