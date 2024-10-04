# utils/database.py
"""
数据库操作工具
设计思路:
1. 管理数据库连接池
2. 提供通用的CRUD操作接口
3. 实现数据库迁移和版本控制
4. 处理复杂查询和事务管理
5. 实现数据缓存机制提高性能
"""

# utils/database.py

import sqlite3
import streamlit as st

def init_connection():
    return sqlite3.connect('lab_management.db', check_same_thread=False)

def init_db():
    conn = get_connection()
    c = conn.cursor()
    
    # 创建用户表
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY,
                  username TEXT UNIQUE,
                  email TEXT UNIQUE,
                  password_hash TEXT,
                  role TEXT DEFAULT "guest",
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # ... (其他表的创建代码)
    # 创建库存表
    c.execute('''CREATE TABLE IF NOT EXISTS inventory_items
                 (id INTEGER PRIMARY KEY,
                  name TEXT,
                  category TEXT,
                  quantity INTEGER,
                  unit TEXT)''')
    # 创建库存使用记录表
    c.execute('''CREATE TABLE IF NOT EXISTS inventory_usage
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER,
                  item_id INTEGER,
                  quantity INTEGER,
                  timestamp TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id),
                  FOREIGN KEY (item_id) REFERENCES inventory_items (id))''')
    # 创建财务交易记录表
    c.execute('''CREATE TABLE IF NOT EXISTS financial_transactions
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER,
                  type TEXT,
                  amount REAL,
                  category TEXT,
                  description TEXT,
                  date DATE,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    # 创建预算表
    c.execute('''CREATE TABLE IF NOT EXISTS budgets
                 (category TEXT PRIMARY KEY,
                  amount REAL)''')
    # 创建设备预约表
    c.execute('''CREATE TABLE IF NOT EXISTS equipment_bookings
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER,
                  equipment_id INTEGER,
                  start_time TIMESTAMP,
                  end_time TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id),
                  FOREIGN KEY (equipment_id) REFERENCES inventory_items (id))''')
    # 创建设备使用日志表
    c.execute('''CREATE TABLE IF NOT EXISTS equipment_usage_logs
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER,
                  equipment_id INTEGER,
                  start_time TIMESTAMP,
                  end_time TIMESTAMP,
                  notes TEXT,
                  FOREIGN KEY (user_id) REFERENCES users (id),
                  FOREIGN KEY (equipment_id) REFERENCES inventory_items (id))''')
    # 创建实验数据表
    c.execute('''CREATE TABLE IF NOT EXISTS experiments
                 (id INTEGER PRIMARY KEY,
                  user_id INTEGER,
                  name TEXT,
                  data TEXT,
                  timestamp TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users (id))''')
    conn.commit()

@st.cache(hash_funcs={sqlite3.Connection: id})
def get_connection():
    return init_connection()

def get_user(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    if user:
        return {'id': user[0], 'username': user[1], 'password_hash': user[2], 'email': user[3]}
    return None

def user_exists(username):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    return c.fetchone() is not None

def create_user(username, password_hash, email):
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
              (username, password_hash, email))
    conn.commit()
    return get_user(username)

def get_recent_projects(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM projects WHERE user_id = ? ORDER BY id DESC LIMIT 5", (user_id,))
    projects = c.fetchall()
    return [{'id': p[0], 'name': p[1], 'description': p[2]} for p in projects]

def get_user_todos(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM todos WHERE user_id = ? AND completed = 0", (user_id,))
    todos = c.fetchall()
    return [{'id': t[0], 'description': t[1], 'completed': t[2]} for t in todos]

def get_user_notifications(user_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM notifications WHERE user_id = ? ORDER BY id DESC LIMIT 5", (user_id,))
    notifications = c.fetchall()
    return [{'id': n[0], 'message': n[1]} for n in notifications]

def get_file(file_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM files WHERE id = ?", (file_id,))
    file = c.fetchone()
    if file:
        return {'id': file[0], 'name': file[1], 'path': file[2], 'user_id': file[3]}
    return None