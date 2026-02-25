import socket
from PIL import Image
from io import BytesIO
import win32clipboard
import time
import sys

PORT = 5000
PORT_TCP = 6000

def copy_image_to_clipboard_from_bytes(img_bytes):
    image = Image.open(BytesIO(img_bytes))

    output = BytesIO()
    image.convert("RGB").save(output,"BMP")
    data = output.getvalue()[14:]
    output.close()
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardData(win32clipboard.CF_DIB, data)
    win32clipboard.CloseClipboard()

    

def receiver_broadcast():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", PORT))

    print("Listening...")

    while True:
        data, addr = sock.recvfrom(1024)
        print(f"{addr[0]} adress message's: ", data.decode())
        sock.sendto(b"Handshake",addr)
        if addr != None:
            break
    sock.close()
    return addr

def receiver_tcp_connection(addr)->bool:
    HOST = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT_TCP))
    server.listen()
    
    server.settimeout(1000) 
    print("Waiting for connection")
    try:
        conn, addr = server.accept()
        print("Connection:", addr)
    except socket.timeout:
        print("No connection for 1000 sec.")
        return False
    
    with conn:
        header = b""
        while not header.endswith(b"\n"):
            chunk = conn.recv(1)
            if not chunk:
                return True
            header += chunk

        header = header.decode().strip()
        parts = header.split()

        image_size = int(parts[1])

        data = b""
        while len(data) < image_size:
            chunk = conn.recv(min(4096, image_size - len(data)))
            if not chunk:
                return False
            data += chunk

        copy_image_to_clipboard_from_bytes(data)
        print("Screenshot received.")

def handleReceiver():
    addr = receiver_broadcast()
    while(True):
        connection = receiver_tcp_connection(addr)
        if connection ==False:
            handleReceiver()
        time.sleep(0.5)
    