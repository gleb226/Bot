import sqlite3
from datetime import datetime
from functools import wraps

def log_error_to_db(user_id: int, command: str, error_message: str):
    conn = sqlite3.connect("errors.db")
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS errors (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, command TEXT, error_message TEXT, timestamp TEXT)"
    )
    cursor.execute(
        "INSERT INTO errors (user_id, command, error_message, timestamp) VALUES (?, ?, ?, ?)",
        (user_id, command, error_message, datetime.now().strftime("%Y-%m-%d %H:%M:%S")),
    )
    conn.commit()
    conn.close()

def error_handler(command: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(message):
            try:
                return await func(message)
            except Exception as e:
                log_error_to_db(message.from_user.id, command, str(e))
                await message.answer("⛔ Function is currently unavailable. Please try again later.")
        return wrapper
    return decorator
