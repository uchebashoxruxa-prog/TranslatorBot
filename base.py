import sqlite3
from configs import LANGUAGES as langs


def create_table_users():
    db = sqlite3.connect('translator.db')
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id BIGINT UNIQUE,
        username VARCHAR(100),
        phone VARCHAR(20),
        date DATE DEFAULT CURRENT_DATE
    )
    ''')
    db.commit()
    db.close()


def get_user(chat_id):
    db = sqlite3.connect('translator.db')
    cursor = db.cursor()
    cursor.execute(f'''
    SELECT chat_id FROM users WHERE chat_id = ?
    ''', (chat_id,))
    user = cursor.fetchone()
    db.close()

    return user


def save_user_data(*args):
    db = sqlite3.connect('translator.db')
    cursor = db.cursor()
    cursor.execute('''
    INSERT INTO users(chat_id, username, phone)
    VALUES (?, ?, ?)
    ''', args)
    db.commit()
    db.close()


def create_table_history():
    db = sqlite3.connect('translator.db')
    cursor = db.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS history(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        src VARCHAR(10),
        dest VARCHAR(10),
        text TEXT,
        result TEXT,
        chat_id BIGINT
    )
    ''')
    db.commit()
    db.close()


def get_history(chat_id):
    db = sqlite3.connect('translator.db')
    cursor = db.cursor()
    cursor.execute('''
    SELECT * FROM (
        SELECT * FROM history
        WHERE chat_id = ?
        ORDER BY id DESC
        LIMIT 10
    )
    ORDER BY id
    ''', (chat_id,))
    history = cursor.fetchall()
    db.close()

    result = []
    i = 1

    for data in history:
        result.append(f'{i}. From {langs[data[1]]} to {langs[data[2]]}. Text: {data[3]}. Translate: {data[4]}')
        i += 1

    return '\n'.join(result)


def save_history_data(*args):
    db = sqlite3.connect('translator.db')
    cursor = db.cursor()
    cursor.execute('''
    INSERT INTO history(src, dest, text, result, chat_id)
    VALUES (?, ?, ?, ?, ?)
    ''', args)
    db.commit()
    db.close()


# create_table_history()
# create_table_users()
