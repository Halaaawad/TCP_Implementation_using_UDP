import utils
from reliable_udp import ReliableUDP

utils.config["LOSS_PROB"] = 0.0
utils.config["CORRUPT_PROB"] = 0.0

client = ReliableUDP("127.0.0.1", 0)
server_addr = ("127.0.0.1", 8080)

print("\n[TEST 4] POST request\n")

client.handshake_client(server_addr)

body = "Hello Server"

request = f"""POST /save HTTP/1.0
Host: localhost
Content-Length: {len(body)}

{body}
"""

client.send(request, server_addr)

response, _ = client.receive()
print("\nRESPONSE:\n", response)

client.close(server_addr)