import socket
import threading

cache = {}


def handle_client(conn):
    while True:
        data = conn.recv(1024).decode().strip()
        if not data:  # ← Должно быть 'data'
            break

        parts = data.split(' ', 2)
        cmd = parts[0].upper()

        if cmd == 'SET' and len(parts) >= 3:
            cache[parts[1]] = parts[2]
            conn.send('OK'.encode())
        elif cmd == 'GET' and len(parts) >= 2:
            value = cache.get(parts[1], 'NOT_FOUND')
            conn.send(value.encode())
        else:
            conn.send('ERROR'.encode())

    conn.close()


server = socket.socket()
server.bind(('127.0.0.1', 65432))
server.listen()
print("Сервер запущен")

while True:
    conn, _ = server.accept()
    threading.Thread(target=handle_client, args=(conn,)).start()