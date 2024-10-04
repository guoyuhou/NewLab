# modules/financial_management.py

from utils import database
from datetime import datetime
import pandas as pd

def add_transaction(user_id, transaction_type, amount, category, description, date):
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
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT SUM(amount) FROM financial_transactions WHERE type = 'income'")
    total_income = c.fetchone()[0] or 0
    c.execute("SELECT SUM(amount) FROM financial_transactions WHERE type = 'expense'")
    total_expense = c.fetchone()[0] or 0
    balance = total_income - total_expense
    return {'total_income': total_income, 'total_expense': total_expense, 'balance': balance}

def get_expense_distribution():
    conn = database.get_connection()
    df = pd.read_sql_query("""
        SELECT category, SUM(amount) as total
        FROM financial_transactions
        WHERE type = 'expense'
        GROUP BY category
    """, conn)
    return df.set_index('category')['total']

def get_monthly_trend():
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