import sqlite3


def delete_database():
    conn = sqlite3.connect('account.db')
    conn.execute('''DROP TABLE IF EXISTS ACCOUNT''')
    conn.execute('''DROP TABLE IF EXISTS AVATAR''')


def create_database():
    conn = sqlite3.connect('account.db')
    conn.execute('''CREATE TABLE ACCOUNT
        (NICKNAME           TEXT                NOT NULL,
        FIRSTNAME           TEXT                NOT NULL,
        SURNAME             TEXT                NOT NULL,
        DATEOFBIRTH         TEXT                NOT NULL,
        EMAIL               TEXT  PRIMARY KEY   NOT NULL,
        PHOTO               BLOB                NOT NULL);''')


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


def select_from_database(select_string):
    conn = sqlite3.connect('account.db')
    cursor = conn.execute(select_string)
    return cursor


def is_user_registred(email):
    conn = sqlite3.connect('account.db')
    cursor = conn.execute(
        "SELECT A.NICKNAME FROM ACCOUNT A WHERE A.EMAIL = '{}'".format(email))
    if(len(cursor.fetchall()) == 0):
        return False
    return True


def get_user_info(email):
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


def get_photo(email):
    conn = sqlite3.connect('account.db')
    cursor = conn.execute(
        "SELECT PHOTO FROM ACCOUNT A WHERE A.EMAIL = '{}'".format(email))
    binary_photo = cursor.fetchone()[0]

    return binary_photo

def change_photo(photo, email):
    conn = sqlite3.connect('account.db')
    conn.execute("UPDATE ACCOUNT SET PHOTO = ? WHERE EMAIL = ?", (photo, email))
    conn.commit()


def change_name(firstname, surname, email):
    conn = sqlite3.connect('account.db')
    conn.execute("UPDATE ACCOUNT SET FIRSTNAME = '{}', SURNAME = '{}' WHERE EMAIL = '{}'".format(
        firstname, surname, email))
    conn.commit()


def change_nickname(nickname, email):
    conn = sqlite3.connect('account.db')
    conn.execute(
        "UPDATE ACCOUNT SET NICKNAME = '{}' WHERE EMAIL = '{}'".format(nickname, email))
    conn.commit()


def change_date_of_birth(dateOfBirth, email):
    conn = sqlite3.connect('account.db')
    conn.execute("UPDATE ACCOUNT SET DATEOFBIRTH = '{}' WHERE EMAIL = '{}'".format(
        dateOfBirth, email))
    conn.commit()


def print_select_output(cursor, rows_name_arr):
    for row in cursor:
        for i in range(len(rows_name_arr)):
            print(rows_name_arr[i], "=", row[i])
    print("\n")
