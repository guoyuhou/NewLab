# 主应用入口
# 功能:
# 1. 设置Streamlit页面配置
# 2. 实现用户认证逻辑
# 3. 根据用户权限动态加载相应页面
# 4. 处理页面路由

# app.py

import streamlit as st
from utils import ui_components
from pages import home, inventory_management, financial_management, project_management, schedule_management, data_visualization, data_export, settings
import modules.user_management as user_management

def main():
    ui_components.set_page_config()
    
    if 'user' not in st.session_state:
        st.session_state.user = None

    if not st.session_state.user:
        show_login_page()
    else:
        show_main_app()

def show_login_page():
    st.title("欢迎使用实验室管理系统")
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")
    if st.button("登录"):
        # 这里应该有真实的用户认证逻辑
        st.session_state.user = {"username": username, "role": "admin"}
        st.experimental_rerun()

def show_main_app():
    page = ui_components.sidebar_menu()

    pages = {
        "home": home,
        "inventory": inventory_management,
        "finance": financial_management,
        "projects": project_management,
        "schedule": schedule_management,
        "visualization": data_visualization,
        "export": data_export,
        "settings": settings,
    }
    
    selection = st.sidebar.radio("导航", list(pages.keys()))

    # 检查用户权限
    if selection == "用户管理" and not user_management.has_permission(st.session_state.user['id'], 'manage_users'):
        st.error("您没有权限访问此页面。")
    else:
        # 渲染选中的页面
        page = pages[selection]
        page.render()

    # 页面底部
    st.sidebar.markdown("---")
    st.sidebar.info("© 2023 实验室管理系统 v1.0")

if __name__ == "__main__":
    main()