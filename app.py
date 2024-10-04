"""
实验室管理系统主应用入口

本文件包含以下主要功能：
1. 设置Streamlit页面配置
2. 实现用户认证逻辑
3. 根据用户权限动态加载相应页面
4. 处理页面路由

作者: [您的名字]
创建日期: [创建日期]
最后修改日期: [最后修改日期]
版本: 1.0
"""

import streamlit as st
from utils import ui_components
from pages import home, inventory_management, financial_management, project_management, schedule_management, data_visualization, data_export, settings
import modules.user_management as user_management
import xlsxwriter


def main():
    """
    主函数，负责初始化应用并控制页面流程
    """
    ui_components.set_page_config()
    
    # 检查用户会话状态
    if 'user' not in st.session_state:
        st.session_state.user = None

    # 根据用户登录状态显示相应页面
    if not st.session_state.user:
        show_login_page()
    else:
        show_main_app()

def show_login_page():
    """
    显示登录页面并处理用户认证
    """
    st.title("欢迎使用实验室管理系统")
    username = st.text_input("用户名")
    password = st.text_input("密码", type="password")
    if st.button("登录"):
        # TODO: 实现真实的用户认证逻辑
        st.session_state.user = {"username": username, "role": "admin"}
        st.experimental_rerun()

def show_main_app():
    """
    显示主应用界面，包括侧边栏菜单和相应的页面内容
    """
    page = ui_components.sidebar_menu()

    # 定义可用页面
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
    
    # 创建侧边栏导航
    selection = st.sidebar.radio("导航", list(pages.keys()))

    # 检查用户权限
    if selection == "用户管理" and not user_management.has_permission(st.session_state.user['id'], 'manage_users'):
        st.error("您没有权限访问此页面。")
    else:
        # 渲染选中的页面
        page = pages[selection]
        page.render()

    # 添加页面底部信息
    st.sidebar.markdown("---")
    st.sidebar.info("© 2023 实验室管理系统 v1.0")

if __name__ == "__main__":
    main()