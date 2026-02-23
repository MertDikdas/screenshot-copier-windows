import socket

PORT = 5000

def reciever_broadcast():
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(("", PORT))

    print("Listening...")

    while True:
        data, addr = sock.recvfrom(1024)
        print(f"{addr[0]} adress message's: ", data.decode())
        if addr != None:
            break
    return addr

def handleReciever():
    addr = reciever_broadcast()
    print(addr)