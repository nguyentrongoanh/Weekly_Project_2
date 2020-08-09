import sqlite3
from DatabaseUtilities import connection

db = connection()

def create_categories_table(conn=db):
    query = """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            url TEXT, 
            parent_id INTEGER, 
            create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """
    try:
        conn.cursor().execute(query)
        conn.commit()
    except Exception as err:
        print('ERROR BY CREATE TABLE', err)
        
def create_products_table(conn=db):
    query = """
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category VARCHAR(255),
            name VARCHAR(255),
            final_price INTEGER,
            regular_price INTEGER,
            discount_percentage INTEGER,
            installment VARCHAR(255),
            cross_border VARCHAR(255),
            sponsor VARCHAR(255),
            reviews INTEGER,
            rating INTEGER,
            rating_by_stars INTEGER,
            url TEXT,
            image_url TEXT
        )"""
    try:
        conn.cursor().execute(query)
        conn.commit()
    except Exception as err:
        print('ERROR BY CREATE TABLE', err)

def get_urls(conn=db):
    urls = conn.cursor().execute("""SELECT DISTINCT url
        FROM categories
        WHERE id
        NOT IN (
            SELECT DISTINCT parent_id 
            FROM categories
            WHERE parent_id NOTNULL)
        AND parent_id NOTNULL""").fetchall()
    return urls

