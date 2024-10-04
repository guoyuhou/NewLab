# modules/project_management.py

from utils import database
from datetime import datetime
import pandas as pd

def get_recent_projects(user_id):
    return database.get_recent_projects(user_id)

def get_user_todos(user_id):
    return database.get_user_todos(user_id)

def get_user_notifications(user_id):
    return database.get_user_notifications(user_id)

def create_project(user_id, name, description, start_date, end_date):
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
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO todos (description, completed, user_id) VALUES (?, ?, ?)",
              (description, False, user_id))
    conn.commit()
    return c.lastrowid

def complete_todo(todo_id):
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("UPDATE todos SET completed = ? WHERE id = ?", (True, todo_id))
    conn.commit()

def add_notification(user_id, message):
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO notifications (message, user_id) VALUES (?, ?)",
              (message, user_id))
    conn.commit()
    return c.lastrowid

def get_user_projects(user_id):
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
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, description, status FROM tasks WHERE project_id = ?", (project_id,))
    tasks = c.fetchall()
    return [{'id': t[0], 'description': t[1], 'status': t[2]} for t in tasks]

def update_task_status(task_id, status):
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
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT name, start_date, end_date, status
        FROM projects
    """)
    projects = c.fetchall()
    return [{'name': p[0], 'start_date': p[1], 'end_date': p[2], 'status': p[3]} for p in projects]

def get_project_report():
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