"""
用户认证模块

本模块提供了用户认证和管理的核心功能，包括：
1. 用户注册：允许新用户创建账户
2. 用户登录：验证用户身份并创建会话
3. 用户注销：结束用户会话
4. 用户信息获取：根据用户ID检索用户信息
5. 权限控制：通过用户角色实现基本的权限管理

未来计划：
- 实现更复杂的权限控制系统
- 集成双因素认证(2FA)以提高安全性

依赖：
- streamlit：用于Web界面交互
- utils.database：处理数据库连接和操作
- utils.security：提供密码哈希和验证功能

注意：
- 所有与数据库的交互都应该使用参数化查询以防止SQL注入攻击
- 密码在存储前应该进行哈希处理，确保用户数据安全
"""

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