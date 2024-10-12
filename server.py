import socket
import threading
#import pandas as pd
from Data import FcData

HEADER = 69
PORT = 4069
SERVER = "127.0.0.1"
ADDR = (SERVER, PORT)
DISCONNECT = "!disconnected"
TERMINATE = "STOP SPAM"


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(ADDR)

s.listen

# pd.read_excel('Data.xlsx')


def handel_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")

    connected = True

    while connected:
        msg_length = conn.recv(HEADER).decode('utf-8')
        msg_length = int(msg_length)
        msg = conn.recv(msg_length).decode('utf-8')
        if msg == DISCONNECT:
            print(f"[DISCONNECT] {(addr)} disconnected!")
            print(f"[ACTIVE CONNECTIONS] {threading.active_count() -2}")
            connected = False
        else:
            message = msg.split(", ")
            Registration = FcData(message)
            print(f"[{addr}] {message}")
            print(f"{Registration}")
            conn.send(Registration.encode("utf-8"))
    conn.close()


def start():
    s.listen()
    print(f"[LISTENING] server is listening on ip {SERVER}")
    while True:
        conn, addr = s.accept()
        thread = threading.Thread(target=handel_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() -1}")


print("[STARTED] Server has successfully setuped")
start()
