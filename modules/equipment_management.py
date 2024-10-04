# modules/equipment_management.py

"""
这个模块负责管理实验室设备的相关功能。
包括获取设备列表、预订设备、查看预订记录、记录设备使用情况和查看使用日志等。
"""

from utils import database
from datetime import datetime, timedelta

def get_all_equipment():
    """
    获取所有设备的列表。
    
    返回:
        list: 包含所有设备信息的列表，每个设备是一个字典，包含id、name和status。
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, status FROM inventory_items WHERE category = 'equipment'")
    equipment = c.fetchall()
    return [{'id': e[0], 'name': e[1], 'status': e[2]} for e in equipment]

def book_equipment(user_id, equipment_id, start_time, end_time):
    """
    预订设备。
    
    参数:
        user_id (int): 用户ID
        equipment_id (int): 设备ID
        start_time (datetime): 预订开始时间
        end_time (datetime): 预订结束时间
    
    返回:
        bool: 预订成功返回True，失败返回False
    """
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO equipment_bookings (user_id, equipment_id, start_time, end_time)
            VALUES (?, ?, ?, ?)
        """, (user_id, equipment_id, start_time, end_time))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

def get_equipment_bookings(equipment_id, start_date, end_date):
    """
    获取指定设备在给定时间范围内的预订记录。
    
    参数:
        equipment_id (int): 设备ID
        start_date (datetime): 开始日期
        end_date (datetime): 结束日期
    
    返回:
        list: 包含预订记录的列表，每条记录是一个字典，包含id、user、start_time和end_time。
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT eb.id, u.username, eb.start_time, eb.end_time
        FROM equipment_bookings eb
        JOIN users u ON eb.user_id = u.id
        WHERE eb.equipment_id = ? AND eb.start_time >= ? AND eb.end_time <= ?
    """, (equipment_id, start_date, end_date))
    bookings = c.fetchall()
    return [{'id': b[0], 'user': b[1], 'start_time': b[2], 'end_time': b[3]} for b in bookings]

def log_equipment_usage(user_id, equipment_id, start_time, end_time, notes):
    """
    记录设备使用情况。
    
    参数:
        user_id (int): 用户ID
        equipment_id (int): 设备ID
        start_time (datetime): 使用开始时间
        end_time (datetime): 使用结束时间
        notes (str): 使用备注
    
    返回:
        bool: 记录成功返回True，失败返回False
    """
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO equipment_usage_logs (user_id, equipment_id, start_time, end_time, notes)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, equipment_id, start_time, end_time, notes))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

def get_equipment_usage_logs(equipment_id, start_date, end_date):
    """
    获取指定设备在给定时间范围内的使用日志。
    
    参数:
        equipment_id (int): 设备ID
        start_date (datetime): 开始日期
        end_date (datetime): 结束日期
    
    返回:
        list: 包含使用日志的列表，每条日志是一个字典，包含id、user、start_time、end_time和notes。
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT eul.id, u.username, eul.start_time, eul.end_time, eul.notes
        FROM equipment_usage_logs eul
        JOIN users u ON eul.user_id = u.id
        WHERE eul.equipment_id = ? AND eul.start_time >= ? AND eul.end_time <= ?
    """, (equipment_id, start_date, end_date))
    logs = c.fetchall()
    return [{'id': l[0], 'user': l[1], 'start_time': l[2], 'end_time': l[3], 'notes': l[4]} for l in logs]