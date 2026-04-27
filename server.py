from reliable_udp import ReliableUDP
from packet import Packet


server = ReliableUDP("127.0.0.1", 8080, is_server=True)

print("Server running...\n")

# ================= HANDSHAKE =================
client_addr = server.handshake_server()

# ================= MAIN LOOP =================
while True:
    result, addr = server.receive()

    # CHECK IF IT IS A CONTROL PACKET
    if isinstance(result, Packet):

        if result.flags == "FIN":
            print("[SERVER] FIN received")
            seq_num = result.seq
            ack = Packet(ack=seq_num, flags="ACK")
            server.sock.sendto(ack.to_json().encode(), addr)
            print("[SERVER] Connection closed")
            break

        continue  # ignore other control packets

    # ================= DATA PACKET =================
    data = result  # now ALWAYS string

    print("Request Received:", data)

    # ================= HTTP GET =================
    if data.startswith("GET"):
        response = """HTTP/1.0 200 OK

Hello Halaa and Nour! This is a response from the server.
"""

    # ================= HTTP POST =================
    elif data.startswith("POST"):
        # Extract body (everything after blank line)
        parts = data.split("\n\n", 1)

        if len(parts) > 1:
            post_body = parts[1]
        else:
            post_body = ""

        print(f"[SERVER] POST Body Received: {post_body}")

        response = f"""HTTP/1.0 200 OK

POST received successfully:
{post_body}
"""

    # ================= NOT FOUND =================
    else:
        response = """HTTP/1.0 404 NOT FOUND

Requested method not supported
"""

    # ================= SEND RESPONSE ================
    server.send(response, addr)