import sqlite3


def db_verify_user(username, password):
    # define query
    sql = """
            SELECT password
            FROM user
            WHERE username=?
            """

    # connect to db
    conn = sqlite3.connect('users.db')
    # to remove u from sqlite3 cursor.fetchall() results
    conn.text_factory = sqlite3.OptimizedUnicode

    # 1. create a cursor
    cursor = conn.cursor()
    # 2. execute query
    try:
        cursor.execute(sql, (username,))
    except sqlite3.Error:
        print "Username not found."
        # close connection
        conn.close()
        return False

    # analyze result
    result = cursor.fetchone()
    if result[0] == password:
        print "User correctly found."
        # close connection
        conn.close()
        return True
    else:
        print "Password not correct."
        # close connection
        conn.close()
        return False


def db_add_user(username, password, name, surname, born_date):
    # define query
    sql = """
        INSERT INTO user(username, password, name, surname, bornDate)
        VALUES (?, ?, ?, ?, ?)
        """

    # connect to db
    conn = sqlite3.connect('users.db')

    # 1. create a cursor
    cursor = conn.cursor()
    # 2. execute query
    cursor.execute(sql, (username, password, name, surname, born_date))

    # commit changes
    conn.commit()

    # close connection
    conn.close()


def db_add_session(username, start_datetime, pre_status, joy, sadness, anger, fear):
    # define query
    sql = """
        INSERT INTO userSession(username, startDatetime, preStatus, joy, sadness, anger, fear)
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """

    # connect to db
    conn = sqlite3.connect('users.db')

    # 1. create a cursor
    cursor = conn.cursor()
    # 2. execute query
    cursor.execute(sql, (username, start_datetime, pre_status, joy, sadness, anger, fear))

    # commit changes
    conn.commit()

    # close connection
    conn.close()


def db_close_session(username, start_datetime, post_status, end_datetime):
    # define query
    sql = """
            UPDATE userSession
            SET  postStatus=?, endDatetime=?
            WHERE username=? AND startDatetime=?
            """

    # connect to db
    conn = sqlite3.connect('users.db')

    # 1. create a cursor
    cursor = conn.cursor()
    # 2. execute query
    cursor.execute(sql, (post_status, end_datetime, username, start_datetime))

    # commit changes
    conn.commit()

    # close connection
    conn.close()


def db_get_user(username):
    # define query
    sql = """
        SELECT username, password, name, surname, bornDate
        FROM user
        WHERE username=?
        """

    # connect to db
    conn = sqlite3.connect('users.db')
    # to remove u from sqlite3 cursor.fetchall() results
    conn.text_factory = sqlite3.OptimizedUnicode

    # 1. create a cursor
    cursor = conn.cursor()
    # 2. execute query
    cursor.execute(sql, (username, ))

    # analyze result
    user = cursor.fetchone()
    # user is a list
    # user[0]->username, user[1]->password, etc.

    # close connection
    conn.close()

    return user


def db_get_emotion(emotion_name):
    # define query
    sql = """
        SELECT light, playlist
        FROM emotion
        WHERE emotionName=?
        """

    # connect to db
    conn = sqlite3.connect('users.db')
    # to remove u from sqlite3 cursor.fetchall() results
    conn.text_factory = sqlite3.OptimizedUnicode

    # 1. create a cursor
    cursor = conn.cursor()
    # 2. execute query
    cursor.execute(sql, (emotion_name, ))

    # analyze result
    emotion = cursor.fetchone()
    # emotion is a list
    # emotion[0]->light, emotion[1]->playlist

    # close connection
    conn.close()

    return emotion


def db_get_sessions(username):
    # define query
    sql = """
        SELECT startDatetime, joy, sadness, anger, fear, preStatus, postStatus
        FROM userSession
        WHERE username=?
        ORDER BY startDatetime DESC LIMIT 4;
        """

    # connect to db
    conn = sqlite3.connect('users.db')
    # to remove u from sqlite3 cursor.fetchall() results
    conn.text_factory = sqlite3.OptimizedUnicode

    # 1. create a cursor
    cursor = conn.cursor()
    # 2. execute query
    cursor.execute(sql, (username, ))

    # analyze result
    sessions_info = cursor.fetchall()

    # close connection
    conn.close()

    return sessions_info
