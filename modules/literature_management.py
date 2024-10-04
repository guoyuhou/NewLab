# modules/literature_management.py

"""
这个模块提供了文献管理的功能，包括添加、搜索、获取和更新文献信息。
它与数据库交互，处理文献的各种属性，如标题、作者、期刊等。
"""

from utils import database

def add_literature(user_id, title, authors, journal, year, doi, notes):
    """
    添加新的文献到数据库。
    
    参数:
    user_id (int): 用户ID
    title (str): 文献标题
    authors (str): 作者
    journal (str): 期刊名
    year (int): 出版年份
    doi (str): DOI号
    notes (str): 笔记
    
    返回:
    bool: 添加成功返回True，失败返回False
    """
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO literature (user_id, title, authors, journal, year, doi, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (user_id, title, authors, journal, year, doi, notes))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

def search_literature(query):
    """
    搜索文献。
    
    参数:
    query (str): 搜索关键词
    
    返回:
    list: 包含匹配文献信息的字典列表
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT id, title, authors, journal, year, doi, notes
        FROM literature
        WHERE title LIKE ? OR authors LIKE ? OR notes LIKE ?
    """, (f"%{query}%", f"%{query}%", f"%{query}%"))
    results = c.fetchall()
    return [{'id': r[0], 'title': r[1], 'authors': r[2], 'journal': r[3], 'year': r[4], 'doi': r[5], 'notes': r[6]} for r in results]

def get_literature(literature_id):
    """
    获取特定文献的详细信息。
    
    参数:
    literature_id (int): 文献ID
    
    返回:
    dict: 包含文献详细信息的字典
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, title, authors, journal, year, doi, notes FROM literature WHERE id = ?", (literature_id,))
    result = c.fetchone()
    return {'id': result[0], 'title': result[1], 'authors': result[2], 'journal': result[3], 'year': result[4], 'doi': result[5], 'notes': result[6]}

def update_literature(literature_id, title, authors, journal, year, doi, notes):
    """
    更新现有文献的信息。
    
    参数:
    literature_id (int): 要更新的文献ID
    title (str): 新的标题
    authors (str): 新的作者
    journal (str): 新的期刊名
    year (int): 新的出版年份
    doi (str): 新的DOI号
    notes (str): 新的笔记
    
    返回:
    bool: 更新成功返回True，失败返回False
    """
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("""
            UPDATE literature
            SET title = ?, authors = ?, journal = ?, year = ?, doi = ?, notes = ?
            WHERE id = ?
        """, (title, authors, journal, year, doi, notes, literature_id))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False