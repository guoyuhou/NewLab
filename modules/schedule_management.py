# modules/schedule_management.py

from utils import database
from datetime import datetime, timedelta

def add_event(user_id, title, start_time, end_time, description, participants):
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