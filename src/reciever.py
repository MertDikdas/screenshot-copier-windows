import socket

HOST = "0.0.0.0"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST,PORT))
server.listen()

print("Server started waiting for connection")

conn, addr= server.accept()

print(f"Connection with = {addr}")

while True:
    data = conn.recv(1024)
    if not data:
        break
    print(data.decode())

conn.close()
server.close()