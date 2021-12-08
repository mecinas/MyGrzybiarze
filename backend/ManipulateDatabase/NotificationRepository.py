import sqlite3

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