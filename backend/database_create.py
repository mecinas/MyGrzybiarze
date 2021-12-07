import sqlite3
import manipulate_database as md
import io

photo = open("resources/noname.png", 'rb')

md.delete_database()
md.create_database()
md.insert_into_account('mecinas', 'Szymon', 'Męcina', '1999-10-20', 'test@gmail.com', photo.read())
md.insert_into_account('oktawius', 'Sonia', 'Olewska', '1999-10-20', 'kotek@gmail.com', photo.read())
md.insert_into_account('kamas', 'Kamil', 'Owies', '1999-10-20', 'smok@gmail.com', photo.read())
md.insert_into_account('sutras', 'Sylwek', 'Maciejewski', '1999-10-20', 'bazyliszek@gmail.com', photo.read())
md.insert_into_account('venom', 'Krzysztof', 'Orban', '1999-10-20', 'tygrys@gmail.com', photo.read())


md.add_friendship("smok@gmail.com", "test@gmail.com")
md.add_friendship("test@gmail.com", "bazyliszek@gmail.com")

md.add_notification("info", "Kamil Owies przyjął twoje zaproszenie do znajomych", "test@gmail.com")
md.add_notification("action", "Sonia Olewska wysłała Ci zaproszenie do znajomych", "test@gmail.com", "/friendship")





