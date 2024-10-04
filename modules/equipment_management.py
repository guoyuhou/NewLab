# modules/equipment_management.py

from utils import database
from datetime import datetime, timedelta

def get_all_equipment():
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, status FROM inventory_items WHERE category = 'equipment'")
    equipment = c.fetchall()
    return [{'id': e[0], 'name': e[1], 'status': e[2]} for e in equipment]

def book_equipment(user_id, equipment_id, start_time, end_time):
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