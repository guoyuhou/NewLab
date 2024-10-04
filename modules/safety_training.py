# modules/safety_training.py

from utils import database
from datetime import datetime

def get_available_courses():
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, title, description FROM safety_courses")
    courses = c.fetchall()
    return [{'id': c[0], 'title': c[1], 'description': c[2]} for c in courses]

def get_course(course_id):
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, title, content FROM safety_courses WHERE id = ?", (course_id,))
    course = c.fetchone()
    return {'id': course[0], 'title': course[1], 'content': course[2]}

def get_course_questions(course_id):
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, question, options FROM safety_questions WHERE course_id = ?", (course_id,))
    questions = c.fetchall()
    return [{'id': q[0], 'question': q[1], 'options': q[2].split('|')} for q in questions]

def evaluate_answers(course_id, user_answers):
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, correct_answer FROM safety_questions WHERE course_id = ?", (course_id,))
    correct_answers = {q[0]: q[1] for q in c.fetchall()}
    
    score = sum(user_answers[q_id] == correct_answers[q_id] for q_id in user_answers) / len(user_answers) * 100
    return round(score, 2)

def mark_course_completed(user_id, course_id, score):
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        INSERT INTO user_training_records (user_id, course_id, completion_date, score)
        VALUES (?, ?, ?, ?)
    """, (user_id, course_id, datetime.now().strftime("%Y-%m-%d"), score))
    conn.commit()

def get_user_training_records(user_id):
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