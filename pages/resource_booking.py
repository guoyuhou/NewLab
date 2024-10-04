# pages/resource_booking.py

"""
此文件包含资源预约系统的页面渲染逻辑。
它提供了一个用户界面，允许用户选择资源、日期和时间段进行预约，
并显示用户的预约历史。
"""

import streamlit as st
from datetime import datetime, timedelta
from modules import resource_management

def render():
    """渲染资源预约系统的主页面"""
    st.title("资源预约系统")

    # 获取所有可用资源
    resources = resource_management.get_all_resources()

    # 选择资源
    selected_resource = st.selectbox("选择资源", [r['name'] for r in resources])
    resource_id = next(r['id'] for r in resources if r['name'] == selected_resource)

    # 选择日期
    date = st.date_input("选择日期", min_value=datetime.now().date())

    # 显示可用时间段
    available_slots = resource_management.get_available_slots(resource_id, date)
    if available_slots:
        selected_slot = st.selectbox("选择时间段", available_slots)

        # 预约原因
        booking_reason = st.text_area("预约原因")

        if st.button("预约"):
            # 尝试预约资源
            if resource_management.book_resource(resource_id, st.session_state.user['id'], date, selected_slot, booking_reason):
                st.success("预约成功！")
            else:
                st.error("预约失败，请重试。")
    else:
        st.warning("该日期没有可用的时间段。")

    # 显示用户的预约历史
    st.subheader("我的预约")
    user_bookings = resource_management.get_user_bookings(st.session_state.user['id'])
    for booking in user_bookings:
        # 为每个预约创建三列布局
        col1, col2, col3 = st.columns(3)
        col1.write(f"资源: {booking['resource_name']}")
        col2.write(f"日期: {booking['date']}")
        col3.write(f"时间: {booking['time_slot']}")
        st.write(f"原因: {booking['reason']}")
        
        # 如果预约日期是今天或将来，显示取消按钮
        if booking['date'] >= datetime.now().date():
            if st.button("取消预约", key=f"cancel_{booking['id']}"):
                # 尝试取消预约
                if resource_management.cancel_booking(booking['id']):
                    st.success("预约已取消。")
                    st.experimental_rerun()
                else:
                    st.error("取消预约失败，请重试。")
        st.write("---")