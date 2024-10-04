# modules/literature_management.py

from utils import database

def add_literature(user_id, title, authors, journal, year, doi, notes):
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
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, title, authors, journal, year, doi, notes FROM literature WHERE id = ?", (literature_id,))
    result = c.fetchone()
    return {'id': result[0], 'title': result[1], 'authors': result[2], 'journal': result[3], 'year': result[4], 'doi': result[5], 'notes': result[6]}

def update_literature(literature_id, title, authors, journal, year, doi, notes):
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