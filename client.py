from reliable_udp import ReliableUDP

if __name__ == "__main__":
    # 1. Create client (port 0 lets OS choose any free port automatically)
    client = ReliableUDP("127.0.0.1", 0)

    # 2. Server address
    server_addr = ("127.0.0.1", 8080)

    print("Connecting to server...\n")

    # 3. HANDSHAKE 
    client.handshake_client(server_addr)


    # ================= 4a. HTTP GET REQUEST =================
    get_request = """GET / HTTP/1.0
Host: localhost

"""
    # SEND GET REQUEST
    print("[CLIENT] Sending HTTP GET request...\n")
    client.send(get_request, server_addr)

    # WAIT FOR GET RESPONSE
    print("[CLIENT] Waiting for GET response...\n")
    get_response, _ = client.receive()

    print("Get Response:", get_response)

    # ================= 4b. HTTP POST REQUEST =================
    post_body = "Hello World from Nour and Halaa"

    post_request = f"""POST /save HTTP/1.0
Host: localhost
Content-Length: {len(post_body)}

{post_body}
"""
    # SEND POST REQUEST
    print("[CLIENT] Sending HTTP POST request...\n")
    client.send(post_request, server_addr)

    # WAIT FOR POST RESPONSE
    print("[CLIENT] Waiting for POST response...\n")
    post_response, _ = client.receive()

    print("Post Response:", post_response)

    # 5. CLOSE CONNECTION
    client.close(server_addr)