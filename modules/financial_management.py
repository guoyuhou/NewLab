# modules/financial_management.py

"""
这个模块包含了财务管理系统的核心功能。
它提供了添加交易、获取交易记录、删除交易、获取财务摘要、
分析支出分布、查看月度趋势、管理预算以及生成财务报告等功能。
"""

from utils import database
from datetime import datetime
import pandas as pd

def add_transaction(user_id, transaction_type, amount, category, description, date):
    """
    添加新的交易记录到数据库。
    
    参数:
    user_id (int): 用户ID
    transaction_type (str): 交易类型 ('收入' 或 '支出')
    amount (float): 交易金额
    category (str): 交易类别
    description (str): 交易描述
    date (str): 交易日期
    
    返回:
    bool: 添加成功返回True，失败返回False
    """
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO financial_transactions (user_id, type, amount, category, description, date)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (user_id, 'income' if transaction_type == '收入' else 'expense', amount, category, description, date))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

def get_recent_transactions(limit=20):
    """
    获取最近的交易记录。
    
    参数:
    limit (int): 返回的记录数量，默认为20
    
    返回:
    list: 包含交易记录字典的列表
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT id, type, amount, category, description, date
        FROM financial_transactions
        ORDER BY date DESC, id DESC
        LIMIT ?
    """, (limit,))
    transactions = c.fetchall()
    return [{'id': t[0], 'type': t[1], 'amount': t[2], 'category': t[3], 'description': t[4], 'date': t[5]} for t in transactions]

def delete_transaction(transaction_id):
    """
    删除指定ID的交易记录。
    
    参数:
    transaction_id (int): 要删除的交易记录ID
    
    返回:
    bool: 删除成功返回True，失败返回False
    """
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("DELETE FROM financial_transactions WHERE id = ?", (transaction_id,))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

def get_financial_summary():
    """
    获取财务摘要，包括总收入、总支出和余额。
    
    返回:
    dict: 包含总收入、总支出和余额的字典
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT SUM(amount) FROM financial_transactions WHERE type = 'income'")
    total_income = c.fetchone()[0] or 0
    c.execute("SELECT SUM(amount) FROM financial_transactions WHERE type = 'expense'")
    total_expense = c.fetchone()[0] or 0
    balance = total_income - total_expense
    return {'total_income': total_income, 'total_expense': total_expense, 'balance': balance}

def get_expense_distribution():
    """
    获取支出分布情况。
    
    返回:
    pandas.Series: 按类别汇总的支出总额
    """
    conn = database.get_connection()
    df = pd.read_sql_query("""
        SELECT category, SUM(amount) as total
        FROM financial_transactions
        WHERE type = 'expense'
        GROUP BY category
    """, conn)
    return df.set_index('category')['total']

def get_monthly_trend():
    """
    获取月度收支趋势。
    
    返回:
    pandas.DataFrame: 包含每月收入和支出的数据框
    """
    conn = database.get_connection()
    df = pd.read_sql_query("""
        SELECT 
            strftime('%Y-%m', date) as month,
            SUM(CASE WHEN type = 'income' THEN amount ELSE 0 END) as income,
            SUM(CASE WHEN type = 'expense' THEN amount ELSE 0 END) as expense
        FROM financial_transactions
        GROUP BY strftime('%Y-%m', date)
        ORDER BY month
    """, conn)
    df['month'] = pd.to_datetime(df['month'])
    return df.set_index('month')

def get_budgets():
    """
    获取所有预算及其使用情况。
    
    返回:
    list: 包含预算信息字典的列表
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT category, amount FROM budgets")
    budgets = c.fetchall()
    
    result = []
    for budget in budgets:
        category, amount = budget
        c.execute("""
            SELECT SUM(amount) FROM financial_transactions
            WHERE type = 'expense' AND category = ?
        """, (category,))
        used = c.fetchone()[0] or 0
        result.append({'category': category, 'amount': amount, 'used': used})
    
    return result

def set_budget(category, amount):
    """
    设置或更新指定类别的预算。
    
    参数:
    category (str): 预算类别
    amount (float): 预算金额
    
    返回:
    bool: 设置成功返回True，失败返回False
    """
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT OR REPLACE INTO budgets (category, amount)
            VALUES (?, ?)
        """, (category, amount))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

def get_financial_report():
    """
    获取完整的财务报告。
    
    返回:
    pandas.DataFrame: 包含所有交易记录的数据框
    """
    conn = database.get_connection()
    df = pd.read_sql_query("""
        SELECT type, amount, category, description, date
        FROM financial_transactions
        ORDER BY date DESC
    """, conn)
    return df