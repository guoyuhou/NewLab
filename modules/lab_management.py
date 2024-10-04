# modules/lab_management.py

"""
这个模块包含了实验室管理系统的核心功能。
它提供了获取实验室信息、成员、设备和最近发表论文的函数，
以及更新实验室信息和检查用户是否为管理员的功能。
"""

from utils import database

def get_lab_info():
    """
    获取实验室的基本信息。
    
    返回:
    dict: 包含实验室名称、所属机构、成立日期和研究重点的字典。
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM lab_info LIMIT 1")
    info = c.fetchone()
    return {
        'name': info[1],
        'institution': info[2],
        'established_date': info[3],
        'research_focus': info[4]
    }

def get_lab_members():
    """
    获取所有实验室成员的信息。
    
    返回:
    list: 包含每个成员信息（姓名、职位、邮箱、研究领域）的字典列表。
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT name, position, email, research_area FROM lab_members")
    members = c.fetchall()
    return [{'name': m[0], 'position': m[1], 'email': m[2], 'research_area': m[3]} for m in members]

def get_lab_equipment():
    """
    获取实验室所有设备的信息。
    
    返回:
    list: 包含每件设备信息（名称、型号、购买日期、状态）的字典列表。
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT name, model, purchase_date, status FROM lab_equipment")
    equipment = c.fetchall()
    return [{'name': e[0], 'model': e[1], 'purchase_date': e[2], 'status': e[3]} for e in equipment]

def get_recent_papers():
    """
    获取实验室最近发表的5篇论文信息。
    
    返回:
    list: 包含每篇论文信息（标题、作者、期刊、发表日期）的字典列表。
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT title, authors, journal, date FROM papers ORDER BY date DESC LIMIT 5")
    papers = c.fetchall()
    return [{'title': p[0], 'authors': p[1], 'journal': p[2], 'date': p[3]} for p in papers]

def is_admin(user_id):
    """
    检查指定用户是否为管理员。
    
    参数:
    user_id (int): 用户ID
    
    返回:
    bool: 如果用户是管理员返回True，否则返回False。
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT is_admin FROM users WHERE id = ?", (user_id,))
    result = c.fetchone()
    return result[0] if result else False

def update_lab_info(name, institution, established_date, research_focus):
    """
    更新实验室的基本信息。
    
    参数:
    name (str): 实验室名称
    institution (str): 所属机构
    established_date (str): 成立日期
    research_focus (str): 研究重点
    
    返回:
    bool: 更新成功返回True，失败返回False。
    """
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("UPDATE lab_info SET name = ?, institution = ?, established_date = ?, research_focus = ?",
                  (name, institution, established_date, research_focus))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False