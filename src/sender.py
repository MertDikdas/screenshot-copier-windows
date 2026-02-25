import socket
import subprocess
from pathlib import Path
from PIL import ImageGrab
import hashlib
import time
import io

PORT = 5000
PORT_TCP = 6000
BROADCAST_IP = "192.168.1.255"

current_dir = Path().resolve()

TEMP_FILE = Path(current_dir / "screenshot.png")

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
        with open(file_path, "rb") as f:
            image_bytes = f.read()

        header = f"IMG {len(image_bytes)}\n".encode()
        s.sendall(header)
        s.sendall(image_bytes)
    print("🖼 sended!")
    
def clipboard_has_image() -> bool:
    img= ImageGrab.grabclipboard()
    if img:
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        image_bytes = buffer.getvalue()
        if img:
            img.save("screenshot.png", "PNG")
        return True
    return False

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

