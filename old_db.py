#import sqlite3
#conn = sqlite3.connect("usersinfo.db")
#c = conn.cursor()

import sqlite3
import threading

# Thread local storage for database connections
thread_local = threading.local()

def get_db_connection():
    # Check if the connection already exists for the current thread
    if not hasattr(thread_local, "connection"):
        # Create a new connection for this thread
        thread_local.connection = sqlite3.connect("usersinfo.db")
        # Ensure foreign key constraints are enforced, if any
        thread_local.connection.execute("PRAGMA foreign_keys = ON")
    return thread_local.connection

def get_db_cursor():
    # Get the current thread's connection
    conn = get_db_connection()
    return conn.cursor()

# Functions
def create_usertable():
    c = get_db_cursor()
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT, password TEXT)')
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

def view_all_users():
    c = get_db_cursor()
    c.execute('SELECT * FROM userstable')
    data = c.fetchall()
    return data