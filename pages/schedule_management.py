# pages/schedule_management.py

import streamlit as st
from modules import schedule_management, user_management
from datetime import datetime, timedelta

def render():
    st.title("日程安排")

    # 添加新事件
    st.subheader("添加新事件")
    col1, col2 = st.columns(2)
    with col1:
        event_title = st.text_input("事件标题")
        event_date = st.date_input("日期")
    with col2:
        event_start_time = st.time_input("开始时间")
        event_end_time = st.time_input("结束时间")
    event_description = st.text_area("事件描述")
    event_participants = st.multiselect("参与者", user_management.get_all_usernames())

    if st.button("添加事件"):
        start_datetime = datetime.combine(event_date, event_start_time)
        end_datetime = datetime.combine(event_date, event_end_time)
        if schedule_management.add_event(st.session_state.user['id'], event_title, start_datetime, end_datetime, event_description, event_participants):
            st.success("事件已添加到日程")
        else:
            st.error("添加事件失败，请重试")

    # 显示日程
    st.subheader("我的日程")
    view_option = st.radio("查看选项", ["日", "周", "月"])
    if view_option == "日":
        selected_date = st.date_input("选择日期", datetime.now())
        events = schedule_management.get_events_by_date(st.session_state.user['id'], selected_date)
    elif view_option == "周":
        selected_week = st.date_input("选择周", datetime.now())
        start_of_week = selected_week - timedelta(days=selected_week.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        events = schedule_management.get_events_by_range(st.session_state.user['id'], start_of_week, end_of_week)
    else:  # 月视图
        selected_month = st.date_input("选择月", datetime.now())
        start_of_month = selected_month.replace(day=1)
        end_of_month = (start_of_month + timedelta(days=32)).replace(day=1) - timedelta(days=1)
        events = schedule_management.get_events_by_range(st.session_state.user['id'], start_of_month, end_of_month)

    for event in events:
        with st.expander(f"{event['start_time'].strftime('%H:%M')} - {event['end_time'].strftime('%H:%M')}: {event['title']}"):
            st.write(f"描述: {event['description']}")
            st.write(f"参与者: {', '.join(event['participants'])}")
            if st.button("删除事件", key=f"delete_{event['id']}"):
                if schedule_management.delete_event(event['id']):
                    st.success("事件已删除")
                    st.experimental_rerun()
                else:
                    st.error("删除事件失败，请重试")

    # 团队日程
    if user_management.has_permission(st.session_state.user['id'], 'view_team_schedule'):
        st.subheader("团队日程")
        team_date = st.date_input("选择日期", datetime.now(), key="team_date")
        team_events = schedule_management.get_team_events_by_date(team_date)
        for event in team_events:
            st.write(f"{event['start_time'].strftime('%H:%M')} - {event['end_time'].strftime('%H:%M')}: {event['title']} (由 {event['creator']} 创建)")

    # 日程提醒
    st.subheader("即将到来的事件")
    upcoming_events = schedule_management.get_upcoming_events(st.session_state.user['id'])
    for event in upcoming_events:
        st.info(f"提醒: {event['title']} 将在 {event['start_time'].strftime('%Y-%m-%d %H:%M')} 开始")