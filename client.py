import os
import socket
import json

from utils.chat import Chat
from utils.message import Message

host = "127.0.0.1"

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_chat(chat: Chat):
    for msg in chat.state:
        print(f"{msg.user}> {msg.text}")

chat = Chat()

while True:
    cmd = input("local: ")
    
    if not cmd:
        break

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, 12137))

    s.sendall(cmd.encode())

    data = s.recv(4096)

    if(data):
        msgs_to_update = json.loads(data.decode())
        chat.state.extend([Message.from_dict] for m in msgs_to_update)
        if(len(chat.state) > 0):
            clear()
            print_chat(chat)

    s.close()

    