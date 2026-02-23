import socket

PORT = 5000
PORT_TCP = 6000
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
    print(f"Connected to : {addr}")

    while True:
        data = conn.recv(1024)
        if not data:
            break
        print("Message : ", data.decode())

        message = input("Answer: ")
        conn.send(message.encode())

    conn.close()
    server.close()

def handleReceiver():
    addr = receiver_broadcast()
    receiver_tcp_connection(addr)
    