# modules/user_management.py

"""
这个模块包含了用户管理相关的功能，包括角色和权限管理、用户活动跟踪等。

主要功能:
- 定义用户角色和权限
- 获取和分配用户角色
- 管理用户权限
- 跟踪用户活动
- 生成用户活动报告
"""

from utils import database
import pandas as pd

# 定义用户角色
ROLES = {
    'admin': '管理员',
    'lab_manager': '实验室管理员',
    'researcher': '研究员',
    'student': '学生',
    'guest': '访客'
}

# 定义系统权限
PERMISSIONS = {
    'manage_inventory': '管理库存',
    'view_inventory': '查看库存',
    'manage_finances': '管理财务',
    'view_finances': '查看财务',
    'manage_projects': '管理项目',
    'view_projects': '查看项目',
    'manage_schedule': '管理日程',
    'view_schedule': '查看日程',
    'manage_users': '管理用户',
    'view_data_visualization': '查看数据可视化',
    'export_data': '导出数据',
    'manage_settings': '管理设置',
}

# 定义角色对应的权限
ROLE_PERMISSIONS = {
    'admin': list(PERMISSIONS.keys()),
    'lab_manager': ['manage_inventory', 'view_inventory', 'manage_finances', 'view_finances', 'manage_projects', 'view_projects', 'manage_schedule', 'view_schedule', 'view_data_visualization', 'export_data'],
    'researcher': ['view_inventory', 'view_finances', 'manage_projects', 'view_projects', 'manage_schedule', 'view_schedule', 'view_data_visualization'],
    'student': ['view_inventory', 'view_projects', 'view_schedule'],
    'guest': ['view_schedule']
}

def get_user_role(user_id):
    """获取指定用户的角色"""
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT role FROM users WHERE id = ?", (user_id,))
    result = c.fetchone()
    return result[0] if result else None

def get_role_permissions(role):
    """获取指定角色的权限列表"""
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT permission FROM role_permissions WHERE role = ?", (role,))
    permissions = c.fetchall()
    return [p[0] for p in permissions]

def get_user_permissions(user_id):
    """获取指定用户的权限列表"""
    user_role = get_user_role(user_id)
    return ROLE_PERMISSIONS.get(user_role, [])

def has_permission(user_id, permission):
    """检查用户是否拥有指定权限"""
    user_permissions = get_user_permissions(user_id)
    return permission in user_permissions

def assign_role(user_id, role):
    """为用户分配新角色"""
    if role not in ROLES:
        return False
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("UPDATE users SET role = ? WHERE id = ?", (role, user_id))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

def get_all_users():
    """获取所有用户信息"""
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, username, email, role FROM users")
    users = c.fetchall()
    return [{'id': u[0], 'username': u[1], 'email': u[2], 'role': u[3]} for u in users]

def update_role_permissions(role, permissions):
    """更新角色的权限"""
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("DELETE FROM role_permissions WHERE role = ?", (role,))
        for permission in permissions:
            c.execute("INSERT INTO role_permissions (role, permission) VALUES (?, ?)", (role, permission))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

def get_user_activity():
    """获取用户活动统计"""
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT u.username, 
               (COUNT(DISTINCT ft.id) + COUNT(DISTINCT e.id) + COUNT(DISTINCT iu.id)) as activity_score
        FROM users u
        LEFT JOIN financial_transactions ft ON u.id = ft.user_id
        LEFT JOIN events e ON u.id = e.user_id
        LEFT JOIN inventory_usage iu ON u.id = iu.user_id
        GROUP BY u.id
        ORDER BY activity_score DESC
    """)
    activity = c.fetchall()
    return [{'username': a[0], 'activity_score': a[1]} for a in activity]

def get_safety_training_completion():
    """获取安全培训完成情况统计"""
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT 
            CASE 
                WHEN utr.completion_date IS NOT NULL THEN '已完成'
                ELSE '未完成'
            END as status,
            COUNT(*) as count
        FROM users u
        LEFT JOIN user_training_records utr ON u.id = utr.user_id
        GROUP BY status
    """)
    completion = c.fetchall()
    return [{'status': c[0], 'count': c[1]} for c in completion]

def get_user_activity_report():
    """生成用户活动报告"""
    conn = database.get_connection()
    df = pd.read_sql_query("""
        SELECT u.username, 
               COUNT(DISTINCT ft.id) as financial_transactions,
               COUNT(DISTINCT e.id) as events_created,
               COUNT(DISTINCT iu.id) as inventory_usages,
               COUNT(DISTINCT utr.id) as completed_trainings
        FROM users u
        LEFT JOIN financial_transactions ft ON u.id = ft.user_id
        LEFT JOIN events e ON u.id = e.user_id
        LEFT JOIN inventory_usage iu ON u.id = iu.user_id
        LEFT JOIN user_training_records utr ON u.id = utr.user_id
        GROUP BY u.id
    """, conn)
    return df