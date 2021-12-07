import sqlite3
import json


def delete_database():
    conn = sqlite3.connect('account.db')
    conn.execute('''DROP TABLE IF EXISTS ACCOUNT''')
    conn.execute('''DROP TABLE IF EXISTS FRIENDSHIP''')
    conn.execute('''DROP TABLE IF EXISTS NOTIFICATION''')


def create_database():
    conn = sqlite3.connect('account.db')
    conn.execute('''CREATE TABLE ACCOUNT
        (NICKNAME           TEXT                NOT NULL,
        FIRSTNAME           TEXT                NOT NULL,
        SURNAME             TEXT                NOT NULL,
        DATEOFBIRTH         TEXT                NOT NULL,
        EMAIL               TEXT  PRIMARY KEY   NOT NULL,
        PHOTO               BLOB                NOT NULL);''')

    conn.execute('''CREATE TABLE FRIENDSHIP
        (ID                 INTEGER PRIMARY KEY AUTOINCREMENT,
        FIRST_PERSON_EMAIL  TEXT                NOT NULL,
        SEC_PERSON_EMAIL    TEXT                NOT NULL,
        FOREIGN KEY(FIRST_PERSON_EMAIL) REFERENCES ACCOUNT(EMAIL),
        FOREIGN KEY(SEC_PERSON_EMAIL) REFERENCES ACCOUNT(EMAIL));''')

    #Dwa rodzaje typów, jeden wymaga potwierdzenia lub odrzucenia drugi jest czysto informacyjny
    conn.execute('''CREATE TABLE NOTIFICATION
        (ID                 INTEGER PRIMARY KEY AUTOINCREMENT,
        NOTIFICATION_TYPE   TEXT                NOT NULL,
        MESSAGE             TEXT                NOT NULL,
        USER_EMAIL          TEXT                NOT NULL,
        REQUEST_URL         TEXT                NULL,
        FOREIGN KEY(USER_EMAIL) REFERENCES ACCOUNT(EMAIL));''')

###############
# NOTIFICATION
###############

def add_notification(notification_type, message, user_email, request_url=None):
    conn = sqlite3.connect('account.db')
    if request_url == None:
        conn.execute("INSERT INTO NOTIFICATION (NOTIFICATION_TYPE, MESSAGE, USER_EMAIL) \
            VALUES (?, ?, ?)", (notification_type, message, user_email))
    else:
        conn.execute("INSERT INTO NOTIFICATION (NOTIFICATION_TYPE, MESSAGE, USER_EMAIL, REQUEST_URL) \
            VALUES (?, ?, ?, ?)", (notification_type, message, user_email, request_url))

    conn.commit()

def delete_notification(notification_id):
    conn = sqlite3.connect('account.db')
    conn.execute("DELETE FROM NOTIFICATION WHERE NOTIFICATION.ID = {}".format(notification_id))
    conn.commit()

def get_user_notifications(user_email):
    conn = sqlite3.connect('account.db')
    cursor = conn.execute("SELECT N.ID, N.NOTIFICATION_TYPE, N.MESSAGE, N.REQUEST_URL FROM NOTIFICATION N \
        WHERE N.USER_EMAIL = '{}'".format(user_email))

    rows_name_arr = ["id", "notification_type", "message", "request_url"]
    result_list = []
    for row in cursor.fetchall():
        result_dict = {}
        for i in range(len(row)):
            result_dict[rows_name_arr[i]] = row[i]
        result_list.append(result_dict)

    return result_list

###############
# FRIEND
###############


def add_friendship(first_email, sec_email):
    conn = sqlite3.connect('account.db')
    conn.execute("INSERT INTO FRIENDSHIP (FIRST_PERSON_EMAIL, SEC_PERSON_EMAIL) \
        VALUES (?, ?)", (first_email, sec_email))
    conn.commit()


def delete_friendship(first_email, sec_email):
    conn = sqlite3.connect('account.db')
    conn.execute("DELETE FROM FRIENDSHIP WHERE ((FRIENDSHIP.FIRST_PERSON_EMAIL = ? AND FRIENDSHIP.SEC_PERSON_EMAIL = ?) OR \
        (FRIENDSHIP.FIRST_PERSON_EMAIL = ? AND FRIENDSHIP.SEC_PERSON_EMAIL = ?))" ,(first_email, sec_email, sec_email, first_email))
    conn.commit()


def get_list_of_friends(user_email):
    conn = sqlite3.connect('account.db')
    cursor = conn.execute("SELECT F.FIRST_PERSON_EMAIL FROM FRIENDSHIP F WHERE F.SEC_PERSON_EMAIL = ? UNION \
        SELECT F.SEC_PERSON_EMAIL FROM FRIENDSHIP F WHERE F.FIRST_PERSON_EMAIL = ?", (user_email, user_email))

    rows_name_arr = ["friend_email"]
    result_list = []
    for row in cursor.fetchall():
        result_dict = {}
        for i in range(len(row)):
            result_dict[rows_name_arr[i]] = row[i]
        result_list.append(result_dict)

    return result_list

def are_users_friends(first_email, sec_email):
    conn = sqlite3.connect('account.db')
    cursor = conn.execute(
        "SELECT F.ID FROM FRIENDSHIP F WHERE (F.FIRST_PERSON_EMAIL = ? AND F.SEC_PERSON_EMAIL = ?) OR\
            (F.FIRST_PERSON_EMAIL = ? AND F.SEC_PERSON_EMAIL = ?)", (first_email, sec_email, sec_email, first_email))
    if(len(cursor.fetchall()) == 0):
        return False
    return True

###############
# ACCOUNT
###############


def insert_into_account(nickname, firstname, surname, dateOfBirth, email, photo):
    conn = sqlite3.connect('account.db')
    conn.execute("INSERT INTO ACCOUNT (NICKNAME, FIRSTNAME, SURNAME, DATEOFBIRTH, EMAIL, PHOTO) \
        VALUES (?, ?, ?, ?, ?, ?)", (nickname, firstname, surname, dateOfBirth, email, photo))
    conn.commit()


def delete_user(email):
    conn = sqlite3.connect('account.db')
    conn.execute(
        "DELETE FROM ACCOUNT WHERE ACCOUNT.EMAIL = '{}'".format(email))
    conn.commit()


def is_user_registred(email):
    conn = sqlite3.connect('account.db')
    cursor = conn.execute(
        "SELECT A.NICKNAME FROM ACCOUNT A WHERE A.EMAIL = '{}'".format(email))
    if(len(cursor.fetchall()) == 0):
        return False
    return True


def get_user(email):
    conn = sqlite3.connect('account.db')
    cursor = conn.execute("SELECT A.NICKNAME, A.FIRSTNAME, A.SURNAME, A.DATEOFBIRTH,\
         A.EMAIL FROM ACCOUNT A WHERE A.EMAIL = '{}'".format(email))
    rows_name_arr = ["nickname", "firstname",
                     "surname", "dateOfBirth", "email"]
    result_dict = {}
    values = cursor.fetchall()[0]
    for i in range(len(values)):
        result_dict[rows_name_arr[i]] = values[i]
    return result_dict


def get_users():
    conn = sqlite3.connect('account.db')
    cursor = conn.execute(
        "SELECT A.FIRSTNAME, A.SURNAME, A.EMAIL FROM ACCOUNT A")
    rows_name_arr = ["firstname", "surname", "email"]

    result_list = []
    for row in cursor.fetchall():
        result_dict = {}
        for i in range(len(row)):
            result_dict[rows_name_arr[i]] = row[i]
        result_list.append(json.dumps(result_dict))
    return result_list


def get_photo(email):
    conn = sqlite3.connect('account.db')
    cursor = conn.execute(
        "SELECT PHOTO FROM ACCOUNT A WHERE A.EMAIL = '{}'".format(email))
    binary_photo = cursor.fetchone()[0]

    return binary_photo


def change_photo(photo, email):
    conn = sqlite3.connect('account.db')
    conn.execute("UPDATE ACCOUNT SET PHOTO = ? WHERE EMAIL = ?",
                 (photo, email))
    conn.commit()


def change_name(firstname, surname, email):
    conn = sqlite3.connect('account.db')
    conn.execute("UPDATE ACCOUNT SET FIRSTNAME = ?, SURNAME = ? WHERE EMAIL = ?", (firstname, surname, email))
    conn.commit()


def change_nickname(nickname, email):
    conn = sqlite3.connect('account.db')
    conn.execute(
        "UPDATE ACCOUNT SET NICKNAME = ? WHERE EMAIL = ?", (nickname, email))
    conn.commit()


def change_date_of_birth(date_of_birth, email):
    conn = sqlite3.connect('account.db')
    conn.execute(
        "UPDATE ACCOUNT SET DATEOFBIRTH = ? WHERE EMAIL = ?", (date_of_birth, email))
    conn.commit()


def select_from_database(select_string):
    conn = sqlite3.connect('account.db')
    cursor = conn.execute(select_string)
    return cursor


def print_select_output(cursor, rows_name_arr):
    for row in cursor:
        for i in range(len(rows_name_arr)):
            print(rows_name_arr[i], "=", row[i])
    print("\n")
