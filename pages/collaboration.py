"""
这个文件实现了一个实时协作页面，包括实时聊天功能。
它使用Streamlit创建用户界面，并通过WebSocket与服务器进行实时通信。
"""

import streamlit as st
import websockets
import asyncio
import json

def render():
    """渲染实时协作页面"""
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
            # 发送消息并刷新页面
            asyncio.run(send_message(st.session_state.user["username"], message))
            st.experimental_rerun()

async def send_message(user, message):
    """
    发送消息到WebSocket服务器
    
    参数:
    user (str): 用户名
    message (str): 消息内容
    """
    uri = "ws://localhost:8765"
    async with websockets.connect(uri) as websocket:
        # 发送消息
        await websocket.send(json.dumps({"user": user, "message": message}))
        # 接收响应
        response = await websocket.recv()
        data = json.loads(response)
        # 添加消息到聊天记录
        st.session_state.chat_messages.append({"user": data["user"], "message": data["message"]})

# 在页面加载时连接到WebSocket服务器
if "ws_connection" not in st.session_state:
    st.session_state.ws_connection = asyncio.run(websockets.connect("ws://localhost:8765"))