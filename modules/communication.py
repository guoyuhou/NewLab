# modules/communication.py
"""
通信模块

该模块实现了一个基本的聊天系统，包括以下功能：
1. 获取聊天室列表
2. 创建新的聊天室
3. 获取特定聊天室的消息
4. 发送消息到聊天室

设计思路:
1. 实现实时聊天功能
2. 支持一对一和群组通信
3. 集成消息通知系统
4. 实现文件和图片共享
5. 提供消息历史记录和搜索功能

注意：当前实现仅包含基本功能，未来可能会扩展以支持更多高级特性。
"""

from utils import database
from datetime import datetime

def get_chat_rooms():
    """
    获取所有聊天室的列表

    返回:
    list: 包含聊天室信息的字典列表，每个字典包含'id'和'name'键
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name FROM chat_rooms")
    rooms = c.fetchall()
    return [{'id': r[0], 'name': r[1]} for r in rooms]

def create_chat_room(name, creator_id):
    """
    创建新的聊天室

    参数:
    name (str): 聊天室名称
    creator_id (int): 创建者的用户ID

    返回:
    bool: 创建成功返回True，失败返回False
    """
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO chat_rooms (name, creator_id) VALUES (?, ?)", (name, creator_id))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False

def get_chat_messages(room_id):
    """
    获取指定聊天室的所有消息

    参数:
    room_id (int): 聊天室ID

    返回:
    list: 包含消息信息的字典列表，每个字典包含'content'、'timestamp'和'username'键
    """
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("""
        SELECT m.content, m.timestamp, u.username 
        FROM chat_messages m 
        JOIN users u ON m.user_id = u.id 
        WHERE m.room_id = ? 
        ORDER BY m.timestamp
    """, (room_id,))
    messages = c.fetchall()
    return [{'content': m[0], 'timestamp': m[1], 'username': m[2]} for m in messages]

def send_message(room_id, user_id, content):
    """
    向指定聊天室发送消息

    参数:
    room_id (int): 聊天室ID
    user_id (int): 发送消息的用户ID
    content (str): 消息内容

    返回:
    bool: 发送成功返回True，失败返回False
    """
    conn = database.get_connection()
    c = conn.cursor()
    try:
        c.execute("INSERT INTO chat_messages (room_id, user_id, content, timestamp) VALUES (?, ?, ?, ?)",
                  (room_id, user_id, content, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        conn.commit()
        return True
    except:
        conn.rollback()
        return False