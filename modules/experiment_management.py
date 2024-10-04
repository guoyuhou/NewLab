# modules/experiment_management.py

from utils import database
import pandas as pd
import numpy as np
from scipy import stats

def save_experiment_data(user_id, experiment_name, data):
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO experiments (user_id, name, data, timestamp)
            VALUES (?, ?, ?, CURRENT_TIMESTAMP)
        """, (user_id, experiment_name, data))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

def get_experiment_data(experiment_id):
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT data FROM experiments WHERE id = ?", (experiment_id,))
    result = c.fetchone()
    return result[0] if result else None

def analyze_experiment_data(data):
    df = pd.read_json(data)
    
    results = {
        'summary_statistics': df.describe().to_dict(),
        'correlation_matrix': df.corr().to_dict(),
    }
    
    # Perform t-test if there are two groups
    if 'group' in df.columns and df['group'].nunique() == 2:
        group_names = df['group'].unique()
        group1 = df[df['group'] == group_names[0]]['value']
        group2 = df[df['group'] == group_names[1]]['value']
        t_stat, p_value = stats.ttest_ind(group1, group2)
        results['t_test'] = {
            't_statistic': t_stat,
            'p_value': p_value
        }
    
    return results

def get_user_experiments(user_id):
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name, timestamp FROM experiments WHERE user_id = ? ORDER BY timestamp DESC", (user_id,))
    experiments = c.fetchall()
    return [{'id': e[0], 'name': e[1], 'timestamp': e[2]} for e in experiments]