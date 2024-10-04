# modules/inventory_management.py

"""
这个模块负责管理库存系统的核心功能。
它包含了添加、更新、查询库存项目以及记录使用情况的函数。
同时还提供了生成库存报告和设备使用率分析的功能。
"""

from utils import database
from datetime import datetime
import pandas as pd

def add_item(name, category, quantity, unit):
    """
    向库存中添加新项目。
    
    参数:
    name (str): 项目名称
    category (str): 项目类别
    quantity (int): 数量
    unit (str): 单位
    
    返回:
    bool: 添加成功返回True，失败返回False
    """
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
    """
    获取所有库存项目。
    
    返回:
    list: 包含所有库存项目信息的字典列表
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, category, quantity, unit FROM inventory_items")
    items = c.fetchall()
    return [{'id': i[0], 'name': i[1], 'category': i[2], 'quantity': i[3], 'unit': i[4]} for i in items]

def update_item_quantity(item_id, new_quantity):
    """
    更新指定项目的数量。
    
    参数:
    item_id (int): 项目ID
    new_quantity (int): 新数量
    
    返回:
    bool: 更新成功返回True，失败返回False
    """
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
    """
    获取库存低于指定阈值的项目。
    
    参数:
    threshold (int): 库存阈值，默认为10
    
    返回:
    list: 包含低库存项目信息的字典列表
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, category, quantity, unit FROM inventory_items WHERE quantity < ?", (threshold,))
    items = c.fetchall()
    return [{'id': i[0], 'name': i[1], 'category': i[2], 'quantity': i[3], 'unit': i[4]} for i in items]

def add_usage_record(user_id, item_id, quantity):
    """
    添加项目使用记录并更新库存。
    
    参数:
    user_id (int): 用户ID
    item_id (int): 项目ID
    quantity (int): 使用数量
    
    返回:
    bool: 添加成功返回True，失败返回False
    """
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
    """
    获取最近的使用记录。
    
    参数:
    limit (int): 返回记录的最大数量，默认为20
    
    返回:
    list: 包含使用记录信息的字典列表
    """
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
    """
    获取设备的使用率。
    
    返回:
    list: 包含设备名称和使用率的字典列表
    """
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
    """
    生成库存报告。
    
    返回:
    pandas.DataFrame: 包含库存项目信息的数据框
    """
    conn = database.get_connection()
    df = pd.read_sql_query("""
        SELECT name, category, quantity, unit
        FROM inventory_items
    """, conn)
    return df