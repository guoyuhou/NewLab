# modules/resource_management.py

"""
此模块负责资源管理系统的核心功能。
包括资源查询、预订、取消预订等操作。
"""

from utils import database
from datetime import datetime, timedelta

def get_all_resources():
    """
    获取所有可用资源的列表。
    
    返回:
        list: 包含所有资源信息的字典列表。
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name FROM resources")
    resources = c.fetchall()
    return [{'id': r[0], 'name': r[1]} for r in resources]

def get_available_slots(resource_id, date):
    """
    获取指定资源在特定日期的可用时间段。
    
    参数:
        resource_id (int): 资源ID
        date (str): 日期字符串
    
    返回:
        list: 可用时间段列表
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT time_slot FROM resource_bookings 
        WHERE resource_id = ? AND date = ?
    """, (resource_id, date))
    booked_slots = [row[0] for row in c.fetchall()]
    
    all_slots = [f"{h:02d}:00-{h+1:02d}:00" for h in range(9, 18)]  # 9:00 到 18:00
    available_slots = [slot for slot in all_slots if slot not in booked_slots]
    return available_slots

def book_resource(resource_id, user_id, date, time_slot, reason):
    """
    预订资源。
    
    参数:
        resource_id (int): 资源ID
        user_id (int): 用户ID
        date (str): 预订日期
        time_slot (str): 预订时间段
        reason (str): 预订原因
    
    返回:
        bool: 预订成功返回True，否则返回False
    """
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO resource_bookings (resource_id, user_id, date, time_slot, reason) 
            VALUES (?, ?, ?, ?, ?)
        """, (resource_id, user_id, date, time_slot, reason))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

def get_user_bookings(user_id):
    """
    获取用户的所有预订记录。
    
    参数:
        user_id (int): 用户ID
    
    返回:
        list: 包含用户所有预订信息的字典列表
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT rb.id, r.name, rb.date, rb.time_slot, rb.reason 
        FROM resource_bookings rb
        JOIN resources r ON rb.resource_id = r.id
        WHERE rb.user_id = ?
        ORDER BY rb.date DESC, rb.time_slot
    """, (user_id,))
    bookings = c.fetchall()
    return [{'id': b[0], 'resource_name': b[1], 'date': b[2], 'time_slot': b[3], 'reason': b[4]} for b in bookings]

def cancel_booking(booking_id):
    """
    取消预订。
    
    参数:
        booking_id (int): 预订ID
    
    返回:
        bool: 取消成功返回True，否则返回False
    """
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("DELETE FROM resource_bookings WHERE id = ?", (booking_id,))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False