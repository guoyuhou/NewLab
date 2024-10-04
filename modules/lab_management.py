# modules/lab_management.py

from utils import database

def get_lab_info():
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
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT name, position, email, research_area FROM lab_members")
    members = c.fetchall()
    return [{'name': m[0], 'position': m[1], 'email': m[2], 'research_area': m[3]} for m in members]

def get_lab_equipment():
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT name, model, purchase_date, status FROM lab_equipment")
    equipment = c.fetchall()
    return [{'name': e[0], 'model': e[1], 'purchase_date': e[2], 'status': e[3]} for e in equipment]

def get_recent_papers():
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT title, authors, journal, date FROM papers ORDER BY date DESC LIMIT 5")
    papers = c.fetchall()
    return [{'title': p[0], 'authors': p[1], 'journal': p[2], 'date': p[3]} for p in papers]

def is_admin(user_id):
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT is_admin FROM users WHERE id = ?", (user_id,))
    result = c.fetchone()
    return result[0] if result else False

def update_lab_info(name, institution, established_date, research_focus):
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