# modules/notification_system.py

from utils import database
from datetime import datetime, timedelta

def generate_notifications():
    notifications = []
    
    # 检查库存不足
    low_stock_items = check_low_stock()
    for item in low_stock_items:
        notifications.append(f"警告：{item['name']} 库存不足，当前数量：{item['quantity']} {item['unit']}")
    
    # 检查预算超支
    over_budget_categories = check_over_budget()
    for category in over_budget_categories:
        notifications.append(f"警告：{category['name']} 类别预算超支，当前支出：¥{category['spent']:.2f}，预算：¥{category['budget']:.2f}")
    
    # 检查即将到期的项目
    expiring_projects = check_expiring_projects()
    for project in expiring_projects:
        notifications.append(f"提醒：项目 '{project['name']}' 将在 {project['days_left']} 天后到期")
    
    return notifications

def check_low_stock(threshold=10):
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT name, quantity, unit
        FROM inventory_items
        WHERE quantity < ?
    """, (threshold,))
    return [{'name': item[0], 'quantity': item[1], 'unit': item[2]} for item in c.fetchall()]

def check_over_budget():
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT b.category, SUM(ft.amount) as spent, b.amount as budget
        FROM budgets b
        JOIN financial_transactions ft ON b.category = ft.category
        WHERE ft.type = 'expense'
        GROUP BY b.category
        HAVING spent > budget
    """)
    return [{'name': item[0], 'spent': item[1], 'budget': item[2]} for item in c.fetchall()]

def check_expiring_projects(days_threshold=7):
    conn = database.get_connection()
    c = conn.cursor()
    today = datetime.now().date()
    threshold_date = today + timedelta(days=days_threshold)
    c.execute("""
        SELECT name, end_date
        FROM projects
        WHERE end_date BETWEEN ? AND ?
        AND status != '已完成'
    """, (today, threshold_date))
    return [{'name': item[0], 'days_left': (datetime.strptime(item[1], '%Y-%m-%d').date() - today).days} for item in c.fetchall()]