import sqlite3

def create_usertable():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS users(username TEXT PRIMARY KEY, password TEXT)')
    c.execute('CREATE TABLE IF NOT EXISTS results(username TEXT, filename TEXT, result TEXT)')
    conn.commit()
    conn.close()

def add_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('INSERT INTO users(username, password) VALUES (?,?)', (username, password))
    conn.commit()
    conn.close()

def login_user(username, password):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    data = c.fetchone()
    conn.close()
    return data

def save_prediction(username, filename, result):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("INSERT INTO results(username, filename, result) VALUES (?, ?, ?)", (username, filename, result))
    conn.commit()
    conn.close()

def get_prediction_history(username):
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    c.execute("SELECT filename, result FROM results WHERE username=?", (username,))
    results = c.fetchall()
    conn.close()
    return results
