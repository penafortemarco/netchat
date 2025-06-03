import signal
import sys
import socket
import json

from utils.user import User
from utils.users import Users
from utils.chat import Chat
from utils.message import Message

def sig_handler(sig, frame):
    print("\nSocket closing...")
    s.close()
    print("Server shutdown!")
    sys.exit(0)

signal.signal(signal.SIGINT, sig_handler)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind(('0.0.0.0', 12137))
s.listen(5)

users = Users()
chat = Chat()

while True:
    conn, addr = s.accept()
    data = conn.recv(1024)
    
    if not data:
        conn.close()
        continue

    user = users.get_user_by_ip(addr[0])

    if(not user):
        user = User(data.decode(), addr[0])
        users.add_user(user)
    else:
        msg = Message(data.decode(), user.username)
        chat.add_msg(msg)

    msgs_to_send: list[Message] = []
    for msg in chat.state:
        if(msg.timestamp > user.last_update_timestamp):
            msgs_to_send.append(msg)

    conn.sendall(json.dumps([msg.to_dict() for msg in msgs_to_send]).encode())

    conn.close()

