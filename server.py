HOST = '0.0.0.0'
PORT = 12137
INCOMING_PACKET_LENGHT = 1024
OUTGOING_PACKET_LENGHT = 4096

import os
import signal
import sys
import socket
import threading
import json
from time import time_ns, sleep

from utils.user import User
from utils.users import Users
from utils.message import Message
from utils.chat import Chat


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(5)

users = Users()
chat = Chat()


def sig_handler(sig, frame):
    print("\nSocket closing...")
    s.close()
    print("Server shutdown!")
    sys.exit(0)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def handle_client(conn: socket.socket, addr: tuple[str, int]):
    print("Drop")
    try:
        user = None
        while True:
            # For debugging purposes
            #clear()
            #chat.print_chat()

            data = conn.recv(INCOMING_PACKET_LENGHT)
            
            msgs_to_send: list[Message] = []  
            if data:
                if data[0] == 0x07:
                    break

                data_str = data.decode()
                if not user and data[0] != 0x00:
                    user = User(data_str, addr[0])
                    users.add_user(user)
                elif data[0] == 0x00:
                    pass
                else:
                    msg = Message(data_str, user.username, time_ns())
                    chat.add_msg(msg)

            if user is None:
                conn.sendall(b'\x00')
                continue
            
            for msg in chat.state:
                if(msg.timestamp > user.last_update_timestamp):
                    msgs_to_send.append(msg)

            if not msgs_to_send:
                conn.sendall(b'\x00')
                continue
            
            conn.sendall(json.dumps([m.to_dict() for m in msgs_to_send]).encode())
            users.update_user_last_timestamp(user, msgs_to_send[-1].timestamp)

    except (BrokenPipeError, AttributeError) as e:
        pass
    finally:
        if user:
            users.update_user_last_timestamp(user, 0)
        conn.close()


signal.signal(signal.SIGINT, sig_handler)

# Main logic
while True:
    #clear()
    users.print_all_users()
    sleep(0.1)

    conn, addr = s.accept()
    threading.Thread(
        target=handle_client, 
        args=(conn, addr), 
        daemon=True
    ).start()

    
    
    

