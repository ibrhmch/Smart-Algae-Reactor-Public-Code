import socket

HOST = "10.200.195.123"  # Listen on this interface
PORT = 12345  # Arbitrary port number
iterations = 0

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print("Connected by", addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            tempdatalist = data.decode().split("---")
            print(f"iteration: {iterations}")
            iterations += 1
            for eachtempdata in tempdatalist:
                print(eachtempdata)
