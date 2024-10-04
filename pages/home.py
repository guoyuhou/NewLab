# pages/home.py
"""
首页
设计思路:
1. 显示用户个性化仪表板
2. 提供快速导航到常用功能
3. 展示重要通知和提醒
4. 显示个人任务和项目概览
5. 集成数据可视化组件
"""
# pages/home.py

import streamlit as st
from modules import project_management, notification_system, external_services

def render():
    st.title("实验室管理系统")
    st.write("欢迎使用实验室管理系统！")

    # 显示通知
    notifications = notification_system.generate_notifications()
    if notifications:
        st.subheader("通知")
        for notification in notifications:
            st.warning(notification)

    st.header("最近项目")
    projects = project_management.get_recent_projects(st.session_state.user['id'])
    for project in projects:
        st.write(f"- {project['name']}")
    
    st.header("待办事项")
    todos = project_management.get_user_todos(st.session_state.user['id'])
    for todo in todos:
        st.checkbox(todo['description'], value=todo['completed'])
    
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
            st.write(f"温度: {weather_data['temperature']}°C")
            st.write(f"湿度: {weather_data['humidity']}%")
            st.write(f"天气: {weather_data['description']}")

            recommendation = external_services.get_weather_recommendation(weather_data)
            st.info(recommendation)
        else:
            st.error("无法获取天气信息，请检查城市名称是否正确。")
