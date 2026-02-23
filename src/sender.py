import socket

PORT = 5000
BROADCAST_IP = "255.255.255.255"

def sender_broadcast():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        message = input("Message: ")
        sock.sendto(message.encode(), (BROADCAST_IP, PORT))

def handleSender():
    sender_broadcast()