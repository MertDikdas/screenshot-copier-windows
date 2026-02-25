import socket
import subprocess
from pathlib import Path
from PIL import ImageGrab
import hashlib
import time
import sys

PORT = 5000
PORT_TCP = 6000
BROADCAST_IP = "192.168.1.255"

TEMP_FILE = Path("/tmp/clipboard_image.png")

def get_image_hash(path: Path) -> str | None:
    if not path.exists():
        return None
    data = path.read_bytes()
    return hashlib.md5(data).hexdigest()

def sender_broadcast():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sock.settimeout(1)  # ⬅️ 1 saniye bekle, sonra devam et

    while True:
        sock.sendto(b"Discover", (BROADCAST_IP, PORT))

        try:
            data, addr = sock.recvfrom(1024)
            print("Peer found:", addr)
            sock.close()
            return addr
        except socket.timeout:
            print("No answer")
            continue

def sender_tcp_connection(addr, file_path:Path):
    HOST = addr[0]   # Her yerden bağlantı kabul et

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT_TCP))
        s.sendall(b"IMG\n")
        with open(file_path, "rb") as f:
            while chunk := f.read(4096):
                s.sendall(chunk)
    print("🖼 sended!")

def clipboard_has_image() -> bool:
    img= ImageGrab.grabclipboard()
    if img is None:
        return False
    img.save(TEMP_FILE,"PNG")
    return True

def handleSender():
    addr = sender_broadcast()

    last_hash=None

    while True:
        if clipboard_has_image():
            current_hash = get_image_hash(TEMP_FILE)
            if current_hash and current_hash != last_hash:
                sender_tcp_connection(addr,TEMP_FILE)
                last_hash = current_hash
        time.sleep(0.5)

