# pages/user_management.py

"""
此文件包含用户权限管理页面的渲染逻辑。
主要功能包括:
1. 显示用户列表及其角色
2. 允许管理员更新用户角色
3. 管理角色权限

作者: [您的名字]
创建日期: [创建日期]
最后修改日期: [最后修改日期]
"""

import streamlit as st
from modules import user_management

def render():
    # 检查当前用户是否有管理用户的权限
    if not user_management.has_permission(st.session_state.user['id'], 'manage_users'):
        st.error("您没有权限访问此页面。")
        return

    st.title("用户权限管理")

    # 用户列表
    st.subheader("用户列表")
    users = user_management.get_all_users()
    for user in users:
        col1, col2, col3 = st.columns([2, 2, 1])
        col1.write(f"**{user['username']}** ({user['email']})")
        current_role = user['role']
        # 为每个用户创建一个角色选择框
        new_role = col2.selectbox("角色", list(user_management.ROLES.keys()), 
                                  index=list(user_management.ROLES.keys()).index(current_role),
                                  key=f"role_{user['id']}")
        # 如果选择了新角色，显示更新按钮
        if new_role != current_role:
            if col3.button("更新", key=f"update_{user['id']}"):
                # 尝试更新用户角色
                if user_management.assign_role(user['id'], new_role):
                    st.success(f"已将 {user['username']} 的角色更新为 {user_management.ROLES[new_role]}")
                else:
                    st.error("更新角色失败，请重试。")

    # 角色权限管理
    st.subheader("角色权限管理")
    # 选择要管理的角色
    selected_role = st.selectbox("选择角色", list(user_management.ROLES.keys()))
    # 获取当前角色的权限
    role_permissions = user_management.get_role_permissions(selected_role)
    # 多选框用于选择新的权限
    new_permissions = st.multiselect("选择权限", list(user_management.PERMISSIONS.keys()), default=role_permissions)
    
    # 更新角色权限的按钮
    if st.button("更新角色权限"):
        # 尝试更新角色权限
        if user_management.update_role_permissions(selected_role, new_permissions):
            st.success(f"已更新 {user_management.ROLES[selected_role]} 的权限")
        else:
            st.error("更新权限失败，请重试。")