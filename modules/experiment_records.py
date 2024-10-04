# modules/experiment_records.py

from utils import database

def create_experiment(user_id, name, description, date):
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("INSERT INTO experiments (user_id, name, description, date) VALUES (?, ?, ?, ?)",
              (user_id, name, description, date))
    conn.commit()
    return c.lastrowid

def get_user_experiments(user_id):
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, description, date FROM experiments WHERE user_id = ? ORDER BY date DESC", (user_id,))
    experiments = c.fetchall()
    return [{'id': e[0], 'name': e[1], 'description': e[2], 'date': e[3]} for e in experiments]

def delete_experiment(exp_id, user_id):
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM experiments WHERE id = ? AND user_id = ?", (exp_id, user_id))
    conn.commit()
    return c.rowcount > 0