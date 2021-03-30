import os, psycopg2, json, discord

DATABASE_URL = None
try:
    DATABASE_URL = os.environ["DATABASE_URL"]
except:
    from secret_keys import DATABASE_URL


#Connect to the database (private function)
def _connect_to_database():
    connection = None
    try:
        connection = psycopg2.connect(DATABASE_URL)
        cur = connection.cursor()
    except:
        print("Error connecting to data base!")
        raise
    return connection, cur

#Disconnect from the database (private function)
def _disconnect_from_database(conn, cur, commit = False):
    if commit:
        conn.commit()
    cur.close()
    conn.close()

def _check_if_exist(conn, cur, text):
    try:
        cur.execute("SELECT * FROM RANDOM_TEXT WHERE TEXT = %s;", (text,))
    except:
        print("Error getting text from data base!")
        raise
    querry_result = cur.fetchone()
    if(querry_result is None):
        return False
    else:
        return True


#Add a new row.
#text - String to be saved in the new row
def add_random_text(text):
    conn, cur = _connect_to_database()

    try:
        cur.execute("INSERT INTO RANDOM_TEXT(TEXT) VALUES (%s);", (text,))
    except:
        print("Error adding random text to data base!")
        _disconnect_from_database(conn, cur)
        raise
    _disconnect_from_database(conn, cur, commit=True)

#Returns text from a random row
def get_random_text():
    conn, cur = _connect_to_database()
    try:
        cur.execute("SELECT * FROM RANDOM_TEXT ORDER BY RANDOM() LIMIT 1;")
    except:
        print("Error getting random text from data base!")
        raise
    querry_result = cur.fetchone()[0]
    _disconnect_from_database(conn, cur)
    return querry_result

#Remove a row
#text - Row that has its text equal to this variable will be removed
def remove_random_text(text):
    conn,cur = _connect_to_database()

    try:
        if not _check_if_exist(conn,cur,text): 
            raise psycopg2.Error
    except:
        raise

    try:
        cur.execute("DELETE FROM RANDOM_TEXT WHERE TEXT = %s;", (text,))
    except:
        _disconnect_from_database(conn, cur)
        raise 
    _disconnect_from_database(conn, cur, commit=True)


#Returns all the text from the database
def get_all_text():
    conn, cur = _connect_to_database()
    try:
        cur.execute("SELECT * FROM RANDOM_TEXT;")
    except:
        print("Error getting random text from data base!")
        raise
    querry_result = cur.fetchall()
    _disconnect_from_database(conn, cur)
    return querry_result

# def check_if_exist(text):
#     conn, cur = _connect_to_database()
#     try:
#         cur.execute("SELECT * FROM RANDOM_TEXT WHERE TEXT = %s;", (text,))
#     except:
#         print("Error getting text from data base!")
#         raise
#     querry_result = cur.fetchone()
#     _disconnect_from_database(conn, cur)
#     if(querry_result is None):
#         return False
#     else:
#         return True