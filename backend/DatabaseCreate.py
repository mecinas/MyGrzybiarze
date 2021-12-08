import sqlite3
from ManipulateDatabase import CoreDatabase as manipulate_core
from ManipulateDatabase import Account as manipulate_account
from ManipulateDatabase import Friendship as manipulate_friendship
from ManipulateDatabase import Notification as manipulate_notification

import io


photo = open("Resources/noname.png", 'rb')

manipulate_core.delete_database()
manipulate_core.create_database()

manipulate_account.insert_into_account('mecinas', 'Szymon', 'Męcina', '1999-10-20', 'test@gmail.com', open("resources/noname.png", 'rb').read())
manipulate_account.insert_into_account('oktawius', 'Sonia', 'Olewska', '1999-10-20', 'kotek@gmail.com', open("resources/noname.png", 'rb').read())
manipulate_account.insert_into_account('kamas', 'Kamil', 'Owies', '1999-10-20', 'smok@gmail.com', open("resources/noname.png", 'rb').read())
manipulate_account.insert_into_account('sutras', 'Sylwek', 'Maciejewski', '1999-10-20', 'bazyliszek@gmail.com', open("resources/noname.png", 'rb').read())
manipulate_account.insert_into_account('venom', 'Krzysztof', 'Orban', '1999-10-20', 'tygrys@gmail.com', open("resources/noname.png", 'rb').read())


manipulate_friendship.add_friendship("smok@gmail.com", "test@gmail.com")
manipulate_friendship.add_friendship("test@gmail.com", "bazyliszek@gmail.com")

manipulate_notification.add_notification("info", "Kamil Owies przyjął twoje zaproszenie do znajomych", "test@gmail.com")
manipulate_notification.add_notification("action", "Sonia Olewska wysłała Ci zaproszenie do znajomych", "test@gmail.com", "/friendship")





