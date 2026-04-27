import socket

HOST = "127.0.0.1"
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen(5)

print(f"HTTP Server running on http://{HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    print(f"\n[NEW CONNECTION] {addr}")

    request = conn.recv(1024).decode()
    print("\n[REQUEST RECEIVED]")
    print(request)

    # Extract HTTP method
    if "GET" in request:
        body = "Hello from your custom HTTP server!"
        response = (
            "HTTP/1.1 200 OK\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(body)}\r\n"
            "\r\n"
            f"{body}"
        )
    else:
        body = "Not Found"
        response = (
            "HTTP/1.1 404 NOT FOUND\r\n"
            "Content-Type: text/plain\r\n"
            f"Content-Length: {len(body)}\r\n"
            "\r\n"
            f"{body}"
        )

    conn.sendall(response.encode())
    conn.close()

    print("[RESPONSE SENT]\n")