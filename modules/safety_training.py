# modules/safety_training.py

"""
这个模块包含了安全培训系统的核心功能。
它提供了获取课程信息、评估答案、记录培训完成情况等功能。
所有的数据操作都通过与数据库的交互来完成。
"""

from utils import database
from datetime import datetime

def get_available_courses():
    """
    获取所有可用的安全课程。
    
    返回:
        list: 包含课程信息的字典列表，每个字典包含id、标题和描述。
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, title, description FROM safety_courses")
    courses = c.fetchall()
    return [{'id': c[0], 'title': c[1], 'description': c[2]} for c in courses]

def get_course(course_id):
    """
    根据课程ID获取特定课程的详细信息。
    
    参数:
        course_id (int): 课程的唯一标识符
    
    返回:
        dict: 包含课程id、标题和内容的字典
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, title, content FROM safety_courses WHERE id = ?", (course_id,))
    course = c.fetchone()
    return {'id': course[0], 'title': course[1], 'content': course[2]}

def get_course_questions(course_id):
    """
    获取特定课程的所有问题。
    
    参数:
        course_id (int): 课程的唯一标识符
    
    返回:
        list: 包含问题信息的字典列表，每个字典包含id、问题内容和选项
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, question, options FROM safety_questions WHERE course_id = ?", (course_id,))
    questions = c.fetchall()
    return [{'id': q[0], 'question': q[1], 'options': q[2].split('|')} for q in questions]

def evaluate_answers(course_id, user_answers):
    """
    评估用户对特定课程问题的回答。
    
    参数:
        course_id (int): 课程的唯一标识符
        user_answers (dict): 用户的回答，键为问题ID，值为用户的答案
    
    返回:
        float: 用户的得分（百分比）
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, correct_answer FROM safety_questions WHERE course_id = ?", (course_id,))
    correct_answers = {q[0]: q[1] for q in c.fetchall()}
    
    score = sum(user_answers[q_id] == correct_answers[q_id] for q_id in user_answers) / len(user_answers) * 100
    return round(score, 2)

def mark_course_completed(user_id, course_id, score):
    """
    标记用户完成了特定课程，并记录其得分。
    
    参数:
        user_id (int): 用户的唯一标识符
        course_id (int): 课程的唯一标识符
        score (float): 用户在课程中的得分
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO user_training_records (user_id, course_id, completion_date, score)
        VALUES (?, ?, ?, ?)
    """, (user_id, course_id, datetime.now().strftime("%Y-%m-%d"), score))
    conn.commit()

def get_user_training_records(user_id):
    """
    获取特定用户的所有培训记录。
    
    参数:
        user_id (int): 用户的唯一标识符
    
    返回:
        list: 包含用户培训记录的字典列表，每个字典包含课程标题、完成日期和得分
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT sc.title, utr.completion_date, utr.score
        FROM user_training_records utr
        JOIN safety_courses sc ON utr.course_id = sc.id
        WHERE utr.user_id = ?
        ORDER BY utr.completion_date DESC
    """, (user_id,))
    records = c.fetchall()
    return [{'course_title': r[0], 'completion_date': r[1], 'score': r[2]} for r in records]