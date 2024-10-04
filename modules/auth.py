# 用户认证模块
# 功能:
# 1. 实现用户注册、登录、注销功能
# 2. 管理用户会话
# 3. 实现权限控制
# 4. 集成双因素认证(2FA)

# modules/auth.py

import streamlit as st
from utils import database, security
from datetime import datetime

def login_user(username, password):
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, username, email, password_hash, role FROM users WHERE username = ?", (username,))
    user = c.fetchone()
    if user and security.verify_password(password, user[3]):
        return {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'role': user[4]
        }
    return None

def logout_user():
    st.session_state.user = None
    st.success("已成功注销")

def register_user(username, email, password):
    conn = database.get_connection()
    c = conn.cursor()
    try:
        password_hash = security.hash_password(password)
        c.execute("""
            INSERT INTO users (username, email, password_hash, role, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (username, email, password_hash, "guest", datetime.now()))
        conn.commit()
        return c.lastrowid
    except:
        conn.rollback()
        return None

def get_user(user_id):
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, username, email, role FROM users WHERE id = ?", (user_id,))
    user = c.fetchone()
    if user:
        return {
            'id': user[0],
            'username': user[1],
            'email': user[2],
            'role': user[3]
        }
    return None