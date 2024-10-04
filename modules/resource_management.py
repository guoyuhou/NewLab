# modules/resource_management.py

from utils import database
from datetime import datetime, timedelta

def get_all_resources():
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name FROM resources")
    resources = c.fetchall()
    return [{'id': r[0], 'name': r[1]} for r in resources]

def get_available_slots(resource_id, date):
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT time_slot FROM resource_bookings 
        WHERE resource_id = ? AND date = ?
    """, (resource_id, date))
    booked_slots = [row[0] for row in c.fetchall()]
    
    all_slots = [f"{h:02d}:00-{h+1:02d}:00" for h in range(9, 18)]  # 9:00 to 18:00
    available_slots = [slot for slot in all_slots if slot not in booked_slots]
    return available_slots

def book_resource(resource_id, user_id, date, time_slot, reason):
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
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("DELETE FROM resource_bookings WHERE id = ?", (booking_id,))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False