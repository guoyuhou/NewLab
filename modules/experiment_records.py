# modules/experiment_records.py

"""
此模块包含与实验记录相关的数据库操作函数。
它提供了创建、获取和删除实验记录的功能。
"""

from utils import database

def create_experiment(user_id, name, description, date):
    """
    创建新的实验记录。

    参数:
    user_id (int): 用户ID
    name (str): 实验名称
    description (str): 实验描述
    date (str): 实验日期

    返回:
    int: 新创建实验的ID
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO experiments (user_id, name, description, date) VALUES (?, ?, ?, ?)",
              (user_id, name, description, date))
    conn.commit()
    return c.lastrowid

def get_user_experiments(user_id):
    """
    获取指定用户的所有实验记录。

    参数:
    user_id (int): 用户ID

    返回:
    list: 包含实验信息的字典列表，按日期降序排序
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, description, date FROM experiments WHERE user_id = ? ORDER BY date DESC", (user_id,))
    experiments = c.fetchall()
    return [{'id': e[0], 'name': e[1], 'description': e[2], 'date': e[3]} for e in experiments]

def delete_experiment(exp_id, user_id):
    """
    删除指定的实验记录。

    参数:
    exp_id (int): 实验ID
    user_id (int): 用户ID

    返回:
    bool: 如果删除成功返回True，否则返回False
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM experiments WHERE id = ? AND user_id = ?", (exp_id, user_id))
    conn.commit()
    return c.rowcount > 0