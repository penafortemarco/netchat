SERVER = '127.0.0.1'
PORT = 12137
INCOMMING_PACKET_LENGHT = 1024
OUTCOMMING_PACKET_LENGHT = 4096

import os
import signal
import sys
import socket
import threading
import json
import time

from utils.chat import Chat
from utils.message import Message

conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
conn.connect((SERVER, PORT))

cmd_lock = threading.Lock()
cmd = ''
chat = Chat()


def sig_handler(sig, frame):
    print("\nSocket closing...")
    conn.close()
    print("Client shutdown!")
    sys.exit(0)


def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def handle_server(conn: socket.socket):
    global cmd
    try:
        while True:
            cmd_lock.acquire()
            if cmd:
                conn.sendall(cmd.encode())
                cmd = ''
            else:
                conn.sendall(b'\x00')
            cmd_lock.release()

            data = conn.recv(OUTCOMMING_PACKET_LENGHT)

            if data and data[0] != 0x00:
                msgs_to_update = json.loads(data.decode())
                for msg in msgs_to_update:
                    chat.state.append(Message.from_dict(msg))
                clear()
                chat.print_chat()
                

            time.sleep(0.1)

    except BrokenPipeError:
        pass
    finally:
        conn.close()


signal.signal(signal.SIGINT, sig_handler)
threading.Thread(target=handle_server, args=(conn,), daemon=True).start()


# Main logic
while True:
    usr_input = input("> ")
    
    if not usr_input:
        continue

    cmd_lock.acquire()
    cmd = usr_input
    cmd_lock.release()



    


    