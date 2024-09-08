import sqlite3

connection = sqlite3.connect("pupil.db")

command = """
INSERT INTO pupils('first_name','last_name','email','class','age')
VALUES('Nurbek','Uktamov','nurbekuktamov66@gmail.com','8-class','14'),('Asil','Shoyiqulov','asilbek55@gmail.com','8-class','13'),('Raxmatillayev','Boburjon','bobur33@gmail.com'9-class','15');


"""
cursor = connection.cursor()

cursor.execute(command)

connection.commit()
