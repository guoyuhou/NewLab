"""
云存储模块

本模块提供了云存储相关的功能，包括：
1. 文件上传：允许用户上传文件到服务器
2. 文件下载：允许用户下载其上传的文件
3. 文件删除：允许用户删除其上传的文件
4. 文件列表：获取用户上传的所有文件列表
5. 文件共享：允许用户与其他用户共享文件

未来计划：
- 集成第三方云存储服务（如AWS S3）
- 实现更细粒度的文件权限控制
- 添加文件版本控制功能

依赖：
- os：用于文件系统操作
- utils.database：处理数据库连接和操作
- utils.security：提供安全相关功能（未在当前代码中直接使用）

注意：
- 所有与数据库的交互都使用参数化查询以防止SQL注入攻击
- 文件操作应考虑异常处理，确保系统稳定性
"""

import os
from utils import database, security

UPLOAD_FOLDER = "uploads"

def upload_file(file, user_id):
    """
    上传文件到服务器并在数据库中记录文件信息
    
    参数:
    file: 上传的文件对象
    user_id: 上传文件的用户ID
    
    返回:
    上传文件的ID
    """
    # 确保上传文件夹存在
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    # 保存文件到服务器
    file_path = os.path.join(UPLOAD_FOLDER, file.name)
    with open(file_path, "wb") as f:
        f.write(file.getbuffer())
    
    # 在数据库中记录文件信息
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO files (name, path, user_id) VALUES (?, ?, ?)",
              (file.name, file_path, user_id))
    conn.commit()
    return c.lastrowid

def list_user_files(user_id):
    """
    获取指定用户上传的所有文件列表
    
    参数:
    user_id: 用户ID
    
    返回:
    包含文件ID和名称的字典列表
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name FROM files WHERE user_id = ?", (user_id,))
    files = c.fetchall()
    return [{'id': f[0], 'name': f[1]} for f in files]

def download_file(file_id, user_id):
    """
    获取指定文件的路径，用于下载
    
    参数:
    file_id: 文件ID
    user_id: 请求下载的用户ID
    
    返回:
    文件路径，如果文件不存在或用户无权限则返回None
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT path FROM files WHERE id = ? AND user_id = ?", (file_id, user_id))
    result = c.fetchone()
    if result:
        return result[0]
    return None

def delete_file(file_id, user_id):
    """
    删除指定的文件
    
    参数:
    file_id: 要删除的文件ID
    user_id: 请求删除的用户ID
    
    返回:
    删除成功返回True，否则返回False
    """
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
    """
    与其他用户共享文件
    
    参数:
    file_name: 要共享的文件名
    share_with: 要共享给的用户名
    user_id: 共享文件的用户ID
    
    返回:
    共享成功返回True，否则返回False
    """
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