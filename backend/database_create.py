import sqlite3
import manipulate_database as md
import io

photo = open("resources/noname.png", 'rb')

md.delete_database()
md.create_database()
md.insert_into_account('mecinas', 'Szymon', 'Męcina', '1999-10-20', 'test@gmail.com', photo.read())