# 云存储模块
# 功能:
# 1. 实现文件上传、下载、删除功能
# 2. 管理文件元数据
# 3. 实现文件共享和权限控制
# 4. 集成云存储服务(如AWS S3)

# modules/cloud_storage.py

import os
from utils import database, security

UPLOAD_FOLDER = "uploads"

def upload_file(file, user_id):
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    file_path = os.path.join(UPLOAD_FOLDER, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO files (name, path, user_id) VALUES (?, ?, ?)",
              (file.name, file_path, user_id))
    conn.commit()
    return c.lastrowid

def list_user_files(user_id):
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name FROM files WHERE user_id = ?", (user_id,))
    files = c.fetchall()
    return [{'id': f[0], 'name': f[1]} for f in files]

def download_file(file_id, user_id):
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT path FROM files WHERE id = ? AND user_id = ?", (file_id, user_id))
    result = c.fetchone()
    if result:
        return result[0]
    return None

def delete_file(file_id, user_id):
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT path FROM files WHERE id = ? AND user_id = ?", (file_id, user_id))
    result = c.fetchone()
    if result:
        os.remove(result[0])
        c.execute("DELETE FROM files WHERE id = ?", (file_id,))
        conn.commit()
        return True
    return False

def share_file(file_name, share_with, user_id):
    conn = database.get_connection()
    c = conn.cursor()
    
    # 获取要共享的文件ID
    c.execute("SELECT id FROM files WHERE name = ? AND user_id = ?", (file_name, user_id))
    file_result = c.fetchone()
    if not file_result:
        return False
    
    file_id = file_result[0]
    
    # 获取要共享给的用户ID
    c.execute("SELECT id FROM users WHERE username = ?", (share_with,))
    user_result = c.fetchone()
    if not user_result:
        return False
    
    share_with_id = user_result[0]
    
    # 创建共享记录
    c.execute("INSERT INTO file_shares (file_id, shared_by, shared_with) VALUES (?, ?, ?)",
              (file_id, user_id, share_with_id))
    conn.commit()
    return True