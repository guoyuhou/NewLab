"""
实时协作模块

这个模块实现了一个简单的WebSocket聊天服务器，允许多个客户端之间进行实时通信。
它使用asyncio和websockets库来处理异步WebSocket连接。

主要功能:
1. 建立WebSocket服务器
2. 处理客户端连接
3. 广播消息给所有连接的客户端
"""

import asyncio
import json
import websockets

# 存储所有连接的WebSocket客户端
connected = set()

async def chat_server(websocket, path):
    """
    处理单个WebSocket连接的协程函数

    参数:
    websocket -- WebSocket连接对象
    path -- 请求路径（在此示例中未使用）
    """
    connected.add(websocket)
    try:
        async for message in websocket:
            # 解析接收到的JSON消息
            data = json.loads(message)
            # 广播消息给所有连接的客户端
            await broadcast(json.dumps({"type": "chat", "user": data["user"], "message": data["message"]}))
    finally:
        # 确保在连接关闭时从集合中移除
        connected.remove(websocket)

async def broadcast(message):
    """
    向所有连接的客户端广播消息

    参数:
    message -- 要广播的消息字符串
    """
    for conn in connected:
        await conn.send(message)

def start_chat_server():
    """
    启动WebSocket聊天服务器

    返回:
    websockets.serve对象，可用于启动服务器
    """
    return websockets.serve(chat_server, "localhost", 8765)

# 在主应用中启动WebSocket服务器
if __name__ == "__main__":
    # 运行聊天服务器
    asyncio.get_event_loop().run_until_complete(start_chat_server())
    # 保持事件循环运行
    asyncio.get_event_loop().run_forever()