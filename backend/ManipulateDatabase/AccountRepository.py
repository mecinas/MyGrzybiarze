import sqlite3

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
        result_list.append(result_dict)
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