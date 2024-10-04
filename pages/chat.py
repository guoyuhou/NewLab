# pages/chat.py

import streamlit as st
from modules import communication

def render():
    st.title("实验室聊天室")

    # 获取所有聊天室
    chat_rooms = communication.get_chat_rooms()

    # 选择或创建聊天室
    selected_room = st.selectbox("选择聊天室", [room['name'] for room in chat_rooms] + ["创建新聊天室"])

    if selected_room == "创建新聊天室":
        new_room_name = st.text_input("新聊天室名称")
        if st.button("创建") and new_room_name:
            if communication.create_chat_room(new_room_name, st.session_state.user['id']):
                st.success(f"聊天室 '{new_room_name}' 创建成功！")
                st.experimental_rerun()
            else:
                st.error("创建聊天室失败，请重试。")
    else:
        # 显示选定聊天室的消息
        room_id = next(room['id'] for room in chat_rooms if room['name'] == selected_room)
        messages = communication.get_chat_messages(room_id)

        for msg in messages:
            st.text(f"{msg['username']} ({msg['timestamp']}): {msg['content']}")

        # 发送新消息
        new_message = st.text_input("输入消息")
        if st.button("发送") and new_message:
            if communication.send_message(room_id, st.session_state.user['id'], new_message):
                st.success("消息发送成功！")
                st.experimental_rerun()
            else:
                st.error("发送消息失败，请重试。")