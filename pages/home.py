"""
pages/home.py

这个文件实现了实验室管理系统的首页功能。

主要功能:
1. 显示用户个性化仪表板
2. 提供快速导航到常用功能
3. 展示重要通知和提醒
4. 显示个人任务和项目概览
5. 集成数据可视化组件
6. 显示天气信息

设计思路:
- 使用Streamlit库构建用户界面
- 从其他模块导入必要的功能
- 分区域展示不同类型的信息
- 提供交互式的天气查询功能
"""

import streamlit as st
from modules import project_management, notification_system, external_services

def render():
    # 设置页面标题
    st.title("实验室管理系统")
    st.write("欢迎使用实验室管理系统！")

    # 显示通知
    notifications = notification_system.generate_notifications()
    if notifications:
        st.subheader("通知")
        for notification in notifications:
            st.warning(notification)

    # 显示最近项目
    st.header("最近项目")
    projects = project_management.get_recent_projects(st.session_state.user['id'])
    for project in projects:
        st.write(f"- {project['name']}")
    
    # 显示待办事项
    st.header("待办事项")
    todos = project_management.get_user_todos(st.session_state.user['id'])
    for todo in todos:
        st.checkbox(todo['description'], value=todo['completed'])
    
    # 显示最新通知
    st.header("最新通知")
    notifications = project_management.get_user_notifications(st.session_state.user['id'])
    for notification in notifications:
        st.info(notification['message'])

    # 显示天气信息
    st.subheader("当前天气")
    city = st.text_input("输入城市名称", "北京")
    if st.button("获取天气"):
        weather_data = external_services.get_weather(city)
        if weather_data:
            # 显示天气详情
            st.write(f"温度: {weather_data['temperature']}°C")
            st.write(f"湿度: {weather_data['humidity']}%")
            st.write(f"天气: {weather_data['description']}")

            # 获取并显示天气建议
            recommendation = external_services.get_weather_recommendation(weather_data)
            st.info(recommendation)
        else:
            st.error("无法获取天气信息，请检查城市名称是否正确。")
