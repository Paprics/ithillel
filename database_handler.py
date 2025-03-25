import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'database', 'chinook.db')
def execute_query(query, args=None):
    try:
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(query, args)
            records = cursor.fetchall()
        return records
    except Exception as e:
        print(f"Ошибка базы данных: {e}")
        return None