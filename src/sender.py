import socket

PORT = 5000
PORT_TCP = 6000
BROADCAST_IP = "192.168.1.255"

def sender_broadcast():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    while True:
        message = input("Message: ")
        sock.sendto(message.encode(), (BROADCAST_IP, PORT))
        data, addr = sock.recvfrom(1024)
        if addr != None:
            break
    sock.close()
    return addr

def sender_tcp_connection(addr):
    HOST = addr[0]   # Her yerden bağlantı kabul et
    PORT = addr[1]

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((HOST, PORT_TCP))

    while True:
        message = input("Mesaj yaz: ")
        client.send(message.encode())

        data = client.recv(1024)
        print("Sunucudan gelen:", data.decode())

def handleSender():
    addr = sender_broadcast()
    sender_tcp_connection(addr)
