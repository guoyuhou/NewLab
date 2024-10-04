# modules/real_time_collaboration.py

import asyncio
import json
import websockets

connected = set()

async def chat_server(websocket, path):
    connected.add(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            await broadcast(json.dumps({"type": "chat", "user": data["user"], "message": data["message"]}))
    finally:
        connected.remove(websocket)

async def broadcast(message):
    for conn in connected:
        await conn.send(message)

def start_chat_server():
    return websockets.serve(chat_server, "localhost", 8765)

# 在主应用中启动WebSocket服务器
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(start_chat_server())
    asyncio.get_event_loop().run_forever()