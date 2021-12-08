import sqlite3

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


#For debug
def select_from_database(select_string):
    conn = sqlite3.connect('account.db')
    cursor = conn.execute(select_string)
    return cursor


def print_select_output(cursor, rows_name_arr):
    for row in cursor:
        for i in range(len(rows_name_arr)):
            print(rows_name_arr[i], "=", row[i])
    print("\n")