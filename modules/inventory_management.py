# modules/inventory_management.py

from utils import database
from datetime import datetime
import pandas as pd

def add_item(name, category, quantity, unit):
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO inventory_items (name, category, quantity, unit)
            VALUES (?, ?, ?, ?)
        """, (name, category, quantity, unit))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

def get_all_items():
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, category, quantity, unit FROM inventory_items")
    items = c.fetchall()
    return [{'id': i[0], 'name': i[1], 'category': i[2], 'quantity': i[3], 'unit': i[4]} for i in items]

def update_item_quantity(item_id, new_quantity):
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("UPDATE inventory_items SET quantity = ? WHERE id = ?", (new_quantity, item_id))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

def get_low_stock_items(threshold=10):
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, category, quantity, unit FROM inventory_items WHERE quantity < ?", (threshold,))
    items = c.fetchall()
    return [{'id': i[0], 'name': i[1], 'category': i[2], 'quantity': i[3], 'unit': i[4]} for i in items]

def add_usage_record(user_id, item_id, quantity):
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO inventory_usage (user_id, item_id, quantity, timestamp)
            VALUES (?, ?, ?, ?)
        """, (user_id, item_id, quantity, datetime.now()))
        c.execute("UPDATE inventory_items SET quantity = quantity - ? WHERE id = ?", (quantity, item_id))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

def get_usage_records(limit=20):
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT u.username, i.name, i.unit, iu.quantity, iu.timestamp
        FROM inventory_usage iu
        JOIN users u ON iu.user_id = u.id
        JOIN inventory_items i ON iu.item_id = i.id
        ORDER BY iu.timestamp DESC
        LIMIT ?
    """, (limit,))
    records = c.fetchall()
    return [{'user': r[0], 'item_name': r[1], 'unit': r[2], 'quantity': r[3], 'timestamp': r[4]} for r in records]

def get_equipment_usage():
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT i.name, 
               COALESCE(COUNT(iu.id), 0) / 
               (JULIANDAY('now') - JULIANDAY(MIN(iu.timestamp))) as usage_rate
        FROM inventory_items i
        LEFT JOIN inventory_usage iu ON i.id = iu.item_id
        WHERE i.category = 'equipment'
        GROUP BY i.id
        ORDER BY usage_rate DESC
    """)
    usage = c.fetchall()
    return [{'name': u[0], 'usage_rate': u[1]} for u in usage]

def get_inventory_report():
    conn = database.get_connection()
    df = pd.read_sql_query("""
        SELECT name, category, quantity, unit
        FROM inventory_items
    """, conn)
    return df