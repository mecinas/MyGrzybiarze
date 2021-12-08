import sqlite3

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