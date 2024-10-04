# utils/ui_components.py

import streamlit as st

def set_page_config():
    st.set_page_config(
        page_title="实验室管理系统",
        page_icon="🧪",
        layout="wide",
        initial_sidebar_state="expanded",
    )

def sidebar_menu():
    with st.sidebar:
        st.image("logo.png", width=200)
        st.title("实验室管理系统")
        menu_items = {
            "首页": "home",
            "库存管理": "inventory",
            "财务管理": "finance",
            "项目管理": "projects",
            "日程安排": "schedule",
            "数据可视化": "visualization",
            "数据导出": "export",
            "设置": "settings",
        }
        selection = st.radio("导航", list(menu_items.keys()))
        return menu_items[selection]

def create_metric_card(title, value, delta=None):
    st.metric(label=title, value=value, delta=delta)

def create_info_card(title, content):
    with st.expander(title):
        st.write(content)

def create_action_card(title, action_func):
    with st.expander(title):
        if st.button("执行"):
            result = action_func()
            st.success(f"操作成功: {result}")