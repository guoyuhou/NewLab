# modules/project_management.py

"""
这个模块包含了项目管理系统的核心功能。
它提供了创建和管理项目、任务、待办事项和通知的功能，
以及生成项目报告和统计信息的能力。
"""

from utils import database
from datetime import datetime
import pandas as pd

def get_recent_projects(user_id):
    """获取用户最近的项目"""
    return database.get_recent_projects(user_id)

def get_user_todos(user_id):
    """获取用户的待办事项"""
    return database.get_user_todos(user_id)

def get_user_notifications(user_id):
    """获取用户的通知"""
    return database.get_user_notifications(user_id)

def create_project(user_id, name, description, start_date, end_date):
    """
    创建新项目
    
    参数:
    user_id (int): 用户ID
    name (str): 项目名称
    description (str): 项目描述
    start_date (str): 开始日期
    end_date (str): 结束日期
    
    返回:
    bool: 创建成功返回True，失败返回False
    """
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO projects (user_id, name, description, start_date, end_date, status)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, name, description, start_date, end_date, '进行中'))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

def add_todo(user_id, description):
    """
    添加待办事项
    
    参数:
    user_id (int): 用户ID
    description (str): 待办事项描述
    
    返回:
    int: 新添加的待办事项ID
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO todos (description, completed, user_id) VALUES (?, ?, ?)",
              (description, False, user_id))
    conn.commit()
    return c.lastrowid

def complete_todo(todo_id):
    """将待办事项标记为已完成"""
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("UPDATE todos SET completed = ? WHERE id = ?", (True, todo_id))
    conn.commit()

def add_notification(user_id, message):
    """
    添加通知
    
    参数:
    user_id (int): 用户ID
    message (str): 通知消息
    
    返回:
    int: 新添加的通知ID
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO notifications (message, user_id) VALUES (?, ?)",
              (message, user_id))
    conn.commit()
    return c.lastrowid

def get_user_projects(user_id):
    """
    获取用户的所有项目及其统计信息
    
    参数:
    user_id (int): 用户ID
    
    返回:
    list: 包含项目信息和统计数据的字典列表
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT p.id, p.name, p.description, p.start_date, p.end_date, p.status,
               COUNT(t.id) as total_tasks,
               SUM(CASE WHEN t.status = '已完成' THEN 1 ELSE 0 END) as completed_tasks
        FROM projects p
        LEFT JOIN tasks t ON p.id = t.project_id
        WHERE p.user_id = ?
        GROUP BY p.id
    """, (user_id,))
    projects = c.fetchall()
    return [{'id': p[0], 'name': p[1], 'description': p[2], 'start_date': p[3], 'end_date': p[4], 
             'status': p[5], 'total_tasks': p[6], 'completed_tasks': p[7]} for p in projects]

def add_task(project_id, description):
    """
    向项目添加新任务
    
    参数:
    project_id (int): 项目ID
    description (str): 任务描述
    
    返回:
    bool: 添加成功返回True，失败返回False
    """
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO tasks (project_id, description, status)
            VALUES (?, ?, ?)
        """, (project_id, description, '进行中'))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

def get_project_tasks(project_id):
    """
    获取项目的所有任务
    
    参数:
    project_id (int): 项目ID
    
    返回:
    list: 包含任务信息的字典列表
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, description, status FROM tasks WHERE project_id = ?", (project_id,))
    tasks = c.fetchall()
    return [{'id': t[0], 'description': t[1], 'status': t[2]} for t in tasks]

def update_task_status(task_id, status):
    """
    更新任务状态
    
    参数:
    task_id (int): 任务ID
    status (str): 新状态
    
    返回:
    bool: 更新成功返回True，失败返回False
    """
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("UPDATE tasks SET status = ? WHERE id = ?", (status, task_id))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

def get_all_projects():
    """
    获取所有项目的基本信息
    
    返回:
    list: 包含所有项目基本信息的字典列表
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT name, start_date, end_date, status
        FROM projects
    """)
    projects = c.fetchall()
    return [{'name': p[0], 'start_date': p[1], 'end_date': p[2], 'status': p[3]} for p in projects]

def get_project_report():
    """
    生成项目报告
    
    返回:
    pandas.DataFrame: 包含所有项目详细信息和统计数据的数据框
    """
    conn = database.get_connection()
    df = pd.read_sql_query("""
        SELECT p.name, p.description, p.start_date, p.end_date, p.status,
               COUNT(t.id) as total_tasks,
               SUM(CASE WHEN t.status = '已完成' THEN 1 ELSE 0 END) as completed_tasks
        FROM projects p
        LEFT JOIN tasks t ON p.id = t.project_id
        GROUP BY p.id
    """, conn)
    return df