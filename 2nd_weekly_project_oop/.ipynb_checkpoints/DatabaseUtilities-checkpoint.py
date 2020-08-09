import sqlite3

def connection(db='tiki.db'):
    db = sqlite3.connect(db)
    return db

def close_connection(con, commit=True):
    if commit:
        con.commit()
    con.close()