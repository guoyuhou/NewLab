# pages/collaboration.py

import streamlit as st
import websockets
import asyncio
import json

def render():
    st.title("实时协作")

    st.subheader("实时聊天")

    # 显示聊天消息
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    for message in st.session_state.chat_messages:
        st.text(f"{message['user']}: {message['message']}")

    # 发送消息
    message = st.text_input("输入消息")
    if st.button("发送"):
        if message:
            asyncio.run(send_message(st.session_state.user["username"], message))
            st.experimental_rerun()

async def send_message(user, message):
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send(json.dumps({"user": user, "message": message}))
        response = await websocket.recv()
        data = json.loads(response)
        st.session_state.chat_messages.append({"user": data["user"], "message": data["message"]})

# 在页面加载时连接到WebSocket服务器
if "ws_connection" not in st.session_state:
    st.session_state.ws_connection = asyncio.run(websockets.connect("ws://localhost:8765"))