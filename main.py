import sqlite3
import credentials


def connect_to_db(db_path):
    try:
        db_conn = sqlite3.connect(db_path)
        return db_conn
    except sqlite3.Error as e:
        print(e)
    return None


if __name__ == '__main__':
    conn = connect_to_db(credentials.get_db_path())
    if conn is not None:
        cur = conn.cursor()


