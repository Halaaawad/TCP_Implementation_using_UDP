import utils
from reliable_udp import ReliableUDP

# ================= LOSS TEST =================
utils.config["LOSS_PROB"] = 0.7
utils.config["CORRUPT_PROB"] = 0.0


client = ReliableUDP("127.0.0.1", 0)
server_addr = ("127.0.0.1", 8080)

print("\n[TEST 2] Packet loss simulation\n")

client.handshake_client(server_addr)

request = """GET / HTTP/1.0
Host: localhost

"""

client.send(request, server_addr)

response, _ = client.receive()
print("\nRESPONSE:\n", response)

client.close(server_addr)