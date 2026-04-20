import socket

HOST = "0.0.0.0"
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

print(f"Servidor escuchando en {HOST}:{PORT}")

conn, addr = server.accept()
print("Conexión aceptada desde:", addr)

data = conn.recv(1024)
print("Bytes recibidos:", data)

body = b"Hola cliente!"

response = (
    b"HTTP/1.1 200 OK\r\n"
    b"Content-Type: text/plain; charset=utf-8\r\n"
    b"Content-Length: " + str(len(body)).encode() + b"\r\n"
    b"Connection: close\r\n" + body
)

conn.sendall(response)

conn.close()
server.close()

print("Conexión cerrada.")
