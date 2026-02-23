import socket
from PIL import Image
from io import BytesIO
import time

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

def receiver_tcp_connection(addr):
    HOST = addr[0]   # Her yerden bağlantı kabul et

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT_TCP))
    server.listen()

    print("Waiting for connection")
    conn, addr = server.accept()
    while True:

        print(f"Connected to : {addr}")
        header=b""
        while not header.endswith(b"\n"):
            header+=conn.recv(1)
        header = header.strip()
        data = b""
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            data += chunk
        if header==b"IMG":
            copy_image_to_clipboard_from_bytes(data)
    conn.close()

def handleReceiver():
    addr = receiver_broadcast()
    receiver_tcp_connection(addr)
    