import sqlite3
from datetime import datetime

DB_NAME = "finance.db"


def initialize_database():
    """
    Инициализация базы данных: создаём таблицы, если их ещё нет.
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        amount REAL NOT NULL,
        timestamp TEXT NOT NULL
    )
    ''')
    conn.commit()
    conn.close()


def add_income(user_id: int, amount: float):
    """
    Добавляет доход в базу данных.
    :param user_id: ID пользователя Telegram
    :param amount: Сумма дохода
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO income (user_id, amount, timestamp) VALUES (?, ?, ?)",
                   (user_id, amount, timestamp))
    conn.commit()
    conn.close()


def get_income(user_id: int):
    """
    Получает все записи доходов для указанного пользователя.
    :param user_id: ID пользователя Telegram
    :return: Список доходов
    """
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("SELECT amount, timestamp FROM income WHERE user_id = ?", (user_id,))
    rows = cursor.fetchall()

    conn.close()
    return rows
