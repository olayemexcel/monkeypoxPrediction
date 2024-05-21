import sqlite3
import threading

# Thread local storage for database connections
thread_local = threading.local()

def get_db_connection():
    if not hasattr(thread_local, "connection"):
        thread_local.connection = sqlite3.connect("usersinfo.db", check_same_thread=False)
        thread_local.connection.execute("PRAGMA foreign_keys = ON")
    return thread_local.connection

def get_db_cursor():
    conn = get_db_connection()
    return conn.cursor()

def create_usertable():
    c = get_db_cursor()
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT UNIQUE, password TEXT)')
    c.connection.commit()
    
def add_userdata(username, password):
    c = get_db_cursor()
    c.execute('INSERT INTO userstable(username, password) VALUES (?, ?)', (username, password))
    c.connection.commit()

def login_user(username, password):
    c = get_db_cursor()
    c.execute('SELECT * FROM userstable WHERE username = ? AND password = ?', (username, password))
    data = c.fetchall()
    return data

def get_user_by_username(username):
    c = get_db_cursor()
    c.execute('SELECT * FROM userstable WHERE username = ?', (username,))
    data = c.fetchone()
    return data

def view_all_users():
    c = get_db_cursor()
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data
