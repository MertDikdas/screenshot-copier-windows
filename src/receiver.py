import socket
from PIL import Image
from io import BytesIO
import win32clipboard
import time
import sys

PORT = 5000
PORT_TCP = 6000

#Copies recieved file to clipboard
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

    
#Waits for connection with another screenshot-copier application
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
#After broadcast it make a tcp connection between each other
def receiver_tcp_connection(addr)->bool:
    HOST = "0.0.0.0"
    #Socket creation
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT_TCP))
    server.listen()
    #Timeout for long waits
    server.settimeout(1000) 
    print("Waiting for screenshot from sender")
    try:
        conn, conn_addr = server.accept()
        if(conn_addr[0] != addr[0]):
            return False
        print("Connection:", conn_addr)
    except socket.timeout:
        print("No connection for 1000 sec.")
        return False
    
    with conn:
        #Reads header
        header = b""
        while not header.endswith(b"\n"):
            chunk = conn.recv(1)
            if not chunk:
                return True
            header += chunk

        header = header.decode().strip()
        parts = header.split()
        #image size
        image_size = int(parts[1])
        #Reads the data
        data = b""
        while len(data) < image_size:
            chunk = conn.recv(min(4096, image_size - len(data)))
            if not chunk:
                return False
            data += chunk
        #copy to clipboard
        copy_image_to_clipboard_from_bytes(data)
        print("Screenshot received.")
#handles receiver functions
def handleReceiver():
    addr = receiver_broadcast()
    while(True):
        connection = receiver_tcp_connection(addr)
        if connection ==False:
            handleReceiver()
        time.sleep(0.2)
    