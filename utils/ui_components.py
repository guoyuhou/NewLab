# utils/ui_components.py
"""
此模块包含实验室管理系统的用户界面组件。
它提供了设置页面配置、创建侧边栏菜单以及各种卡片组件的功能。
"""

import streamlit as st

def set_page_config():
    """
    设置Streamlit页面的配置。
    """
    st.set_page_config(
        page_title="实验室管理系统",
        page_icon="🧪",
        layout="wide",
        initial_sidebar_state="expanded",
    )

def sidebar_menu():
    """
    创建侧边栏菜单并返回用户选择的菜单项。
    
    返回:
    str: 选中的菜单项对应的值
    """
    with st.sidebar:
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
    """
    创建一个指标卡片。
    
    参数:
    title (str): 卡片标题
    value (Any): 显示的值
    delta (Any, 可选): 变化量
    """
    st.metric(label=title, value=value, delta=delta)

def create_info_card(title, content):
    """
    创建一个信息卡片。
    
    参数:
    title (str): 卡片标题
    content (str): 卡片内容
    """
    with st.expander(title):
        st.write(content)

def create_action_card(title, action_func):
    """
    创建一个动作卡片，包含可执行的操作。
    
    参数:
    title (str): 卡片标题
    action_func (callable): 执行按钮点击时调用的函数
    """
    with st.expander(title):
        if st.button("执行"):
            result = action_func()
            st.success(f"操作成功: {result}")