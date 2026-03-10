import socket

def send(cmd):
    with socket.socket() as s:
        s.connect(('127.0.0.1', 65432))
        s.send(cmd.encode())
        return s.recv(1024).decode()

if __name__ == "__main__":
    print(send("SET username Timofei"))
    print(send("GET username"))