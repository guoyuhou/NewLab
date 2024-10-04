# modules/communication.py
"""
通信模块
设计思路:
1. 实现实时聊天功能
2. 支持一对一和群组通信
3. 集成消息通知系统
4. 实现文件和图片共享
5. 提供消息历史记录和搜索功能
"""

# modules/communication.py

from utils import database
from datetime import datetime

def get_chat_rooms():
    conn = database.get_connection()
    c = conn.cursor()
    c.execute("SELECT id, name FROM chat_rooms")
    rooms = c.fetchall()
    return [{'id': r[0], 'name': r[1]} for r in rooms]

def create_chat_room(name, creator_id):
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