import sqlite3

connection = sqlite3.connect("pupil.db")

command = """
SELECT * from pupils ORDER BY age;
"""

cursor = connection.cursor()

cursor.execute(command)

pupils = cursor.fetchall()

# print(pupils)



command = """
SELECT MIN(age)
FROM pupils

"""
cursor.execute(command)

eng_yosh_uquvchi = cursor.fetchone()

print(f"Bizda o'yiyotkan o'quvchilar sinflari:{eng_yosh_uquvchi}")