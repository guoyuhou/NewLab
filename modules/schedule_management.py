# modules/schedule_management.py

"""
这个模块包含了日程管理系统的核心功能。
它提供了添加、获取、删除事件以及管理团队事件的功能。
所有的数据库操作都通过 utils.database 模块进行。
"""

from utils import database
from datetime import datetime, timedelta

def add_event(user_id, title, start_time, end_time, description, participants):
    """
    添加新事件到数据库。
    
    参数:
    user_id (int): 创建事件的用户ID
    title (str): 事件标题
    start_time (datetime): 事件开始时间
    end_time (datetime): 事件结束时间
    description (str): 事件描述
    participants (list): 参与者用户名列表
    
    返回:
    bool: 添加成功返回True，失败返回False
    """
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO events (user_id, title, start_time, end_time, description)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, title, start_time, end_time, description))
        event_id = c.lastrowid
        for participant in participants:
            c.execute("INSERT INTO event_participants (event_id, username) VALUES (?, ?)", (event_id, participant))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

def get_events_by_date(user_id, date):
    """
    获取指定日期的所有事件。
    
    参数:
    user_id (int): 用户ID
    date (str): 日期字符串，格式为'YYYY-MM-DD'
    
    返回:
    list: 事件字典列表
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT e.id, e.title, e.start_time, e.end_time, e.description, GROUP_CONCAT(ep.username, ', ') as participants
        FROM events e
        LEFT JOIN event_participants ep ON e.id = ep.event_id
        WHERE e.user_id = ? AND DATE(e.start_time) = ?
        GROUP BY e.id
        ORDER BY e.start_time
    """, (user_id, date))
    events = c.fetchall()
    return [{'id': e[0], 'title': e[1], 'start_time': e[2], 'end_time': e[3], 'description': e[4], 'participants': e[5].split(', ') if e[5] else []} for e in events]

def get_events_by_range(user_id, start_date, end_date):
    """
    获取指定日期范围内的所有事件。
    
    参数:
    user_id (int): 用户ID
    start_date (str): 开始日期，格式为'YYYY-MM-DD'
    end_date (str): 结束日期，格式为'YYYY-MM-DD'
    
    返回:
    list: 事件字典列表
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT e.id, e.title, e.start_time, e.end_time, e.description, GROUP_CONCAT(ep.username, ', ') as participants
        FROM events e
        LEFT JOIN event_participants ep ON e.id = ep.event_id
        WHERE e.user_id = ? AND DATE(e.start_time) BETWEEN ? AND ?
        GROUP BY e.id
        ORDER BY e.start_time
    """, (user_id, start_date, end_date))
    events = c.fetchall()
    return [{'id': e[0], 'title': e[1], 'start_time': e[2], 'end_time': e[3], 'description': e[4], 'participants': e[5].split(', ') if e[5] else []} for e in events]

def delete_event(event_id):
    """
    删除指定的事件。
    
    参数:
    event_id (int): 要删除的事件ID
    
    返回:
    bool: 删除成功返回True，失败返回False
    """
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("DELETE FROM event_participants WHERE event_id = ?", (event_id,))
        c.execute("DELETE FROM events WHERE id = ?", (event_id,))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

def get_team_events_by_date(date):
    """
    获取指定日期的所有团队事件。
    
    参数:
    date (str): 日期字符串，格式为'YYYY-MM-DD'
    
    返回:
    list: 事件字典列表，包含创建者信息
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT e.id, e.title, e.start_time, e.end_time, e.description, u.username as creator
        FROM events e
        JOIN users u ON e.user_id = u.id
        WHERE DATE(e.start_time) = ?
        ORDER BY e.start_time
    """, (date,))
    events = c.fetchall()
    return [{'id': e[0], 'title': e[1], 'start_time': e[2], 'end_time': e[3], 'description': e[4], 'creator': e[5]} for e in events]

def get_upcoming_events(user_id, days=7):
    """
    获取用户未来指定天数内的事件。
    
    参数:
    user_id (int): 用户ID
    days (int): 未来的天数，默认为7天
    
    返回:
    list: 事件字典列表，包含事件ID、标题和开始时间
    """
    conn = database.get_connection()
    c = conn.cursor()
    now = datetime.now()
    future = now + timedelta(days=days)
    c.execute("""
        SELECT id, title, start_time
        FROM events
        WHERE user_id = ? AND start_time BETWEEN ? AND ?
        ORDER BY start_time
    """, (user_id, now, future))
    events = c.fetchall()
    return [{'id': e[0], 'title': e[1], 'start_time': e[2]} for e in events]