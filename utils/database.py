# utils/database.py
"""
数据库操作工具模块

该模块提供了一系列用于管理实验室管理系统数据库的函数和工具。

主要功能：
1. 管理数据库连接池
2. 提供通用的CRUD（创建、读取、更新、删除）操作接口
3. 实现数据库初始化和表结构创建
4. 处理用户认证和授权相关的数据库操作
5. 提供项目、待办事项和通知等功能的数据访问方法

设计思路:
1. 使用SQLite作为轻量级数据库解决方案
2. 利用连接池管理数据库连接，提高性能
3. 使用参数化查询，防止SQL注入攻击
4. 实现基本的数据模型，包括用户、库存、财务、设备预约等
5. 提供缓存机制（通过Streamlit的缓存装饰器）以提高查询效率
"""

import sqlite3
import streamlit as st

def init_connection():
    """
    初始化并返回一个新的数据库连接
    
    返回:
        sqlite3.Connection: 数据库连接对象
    """
    return sqlite3.connect('lab_management.db', check_same_thread=False)

def init_db():
    """
    初始化数据库，创建必要的表结构
    
    该函数会创建以下表：
    - users: 用户信息表
    - inventory_items: 库存物品表
    - inventory_usage: 库存使用记录表
    - financial_transactions: 财务交易记录表
    - budgets: 预算表
    - equipment_bookings: 设备预约表
    - equipment_usage_logs: 设备使用日志表
    - experiments: 实验数据表
    """
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
    """
    获取数据库连接（使用Streamlit缓存以提高性能）
    
    返回:
        sqlite3.Connection: 缓存的数据库连接对象
    """
    return init_connection()

def get_user(username):
    """
    根据用户名获取用户信息
    
    参数:
        username (str): 用户名
    
    返回:
        dict: 包含用户信息的字典，如果用户不存在则返回None
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    if user:
        return {'id': user[0], 'username': user[1], 'password_hash': user[2], 'email': user[3]}
    return None

def user_exists(username):
    """
    检查用户名是否已存在
    
    参数:
        username (str): 要检查的用户名
    
    返回:
        bool: 如果用户名已存在返回True，否则返回False
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    return c.fetchone() is not None

def create_user(username, password_hash, email):
    """
    创建新用户
    
    参数:
        username (str): 用户名
        password_hash (str): 密码哈希值
        email (str): 电子邮件地址
    
    返回:
        dict: 包含新创建用户信息的字典
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password_hash, email) VALUES (?, ?, ?)",
              (username, password_hash, email))
    conn.commit()
    return get_user(username)

def get_recent_projects(user_id):
    """
    获取用户最近的项目
    
    参数:
        user_id (int): 用户ID
    
    返回:
        list: 包含最近5个项目信息的列表
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM projects WHERE user_id = ? ORDER BY id DESC LIMIT 5", (user_id,))
    projects = c.fetchall()
    return [{'id': p[0], 'name': p[1], 'description': p[2]} for p in projects]

def get_user_todos(user_id):
    """
    获取用户未完成的待办事项
    
    参数:
        user_id (int): 用户ID
    
    返回:
        list: 包含未完成待办事项信息的列表
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM todos WHERE user_id = ? AND completed = 0", (user_id,))
    todos = c.fetchall()
    return [{'id': t[0], 'description': t[1], 'completed': t[2]} for t in todos]

def get_user_notifications(user_id):
    """
    获取用户最近的通知
    
    参数:
        user_id (int): 用户ID
    
    返回:
        list: 包含最近5条通知信息的列表
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM notifications WHERE user_id = ? ORDER BY id DESC LIMIT 5", (user_id,))
    notifications = c.fetchall()
    return [{'id': n[0], 'message': n[1]} for n in notifications]

def get_file(file_id):
    """
    根据文件ID获取文件信息
    
    参数:
        file_id (int): 文件ID
    
    返回:
        dict: 包含文件信息的字典，如果文件不存在则返回None
    """
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM files WHERE id = ?", (file_id,))
    file = c.fetchone()
    if file:
        return {'id': file[0], 'name': file[1], 'path': file[2], 'user_id': file[3]}
    return None