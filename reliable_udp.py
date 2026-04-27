import socket
import time

from torch import addr
from packet import Packet
from utils import simulate_loss, simulate_corruption

TIMEOUT = 2


class ReliableUDP:
    # creates UDP socket and initializes sequence numbers 
    def __init__(self, ip, port, is_server=False):
        #socket creation
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # bind socket: assigns ip and port numbers
        self.sock.bind((ip, port))

        # sets timeout for client (for retransmission), but not for server (wait indefinitely)
        self.sock.settimeout(None if is_server else TIMEOUT)

        self.seq = 0
        self.last_received_seq = -1  # for duplicate detection

    # CONNECTION HANDSHAKE 
    def handshake_server(self):
        while True:
            pkt, addr = self.receive_raw()

            if pkt.flags == "SYN":
                print("[SERVER] SYN received")

                reply = Packet(seq=0, ack=0, flags="SYNACK")
                self.sock.sendto(reply.to_json().encode(), addr)

                print("[SERVER] SYN-ACK sent")

                ack, _ = self.receive_raw()
                if ack.flags == "ACK" and ack.is_valid():
                    print("[SERVER] Connection established\n")
                    return addr

    def handshake_client(self, server_addr):
        syn = Packet(seq=0, flags="SYN")
        self.sock.sendto(syn.to_json().encode(), server_addr)
        print("[CLIENT] SYN sent")

        synack, _ = self.receive_raw()
        if synack.flags == "SYNACK":
            print("[CLIENT] SYN-ACK received")

            ack = Packet(seq=0, flags="ACK")
            self.sock.sendto(ack.to_json().encode(), server_addr)

            print("[CLIENT] ACK sent → Connected\n")

    # SEND: stop and wait, if ACK not received within timeout, retransmit
    def send(self, data, addr):
        pkt = Packet(seq=self.seq, data=data, flags="DATA")

        while True:
            print(f"[CLIENT] Sending SEQ={pkt.seq}, FLAGS={pkt.flags}")

            # LOSS (DATA ONLY)
            if simulate_loss():
                print("[LOSS] Packet dropped")
                # do NOT send anything
            else:
                # make a fresh copy before corruption
                tx_pkt = Packet(
                    seq=pkt.seq,
                    data=pkt.data,
                    flags=pkt.flags
                )

                tx_pkt = simulate_corruption(tx_pkt)

                self.sock.sendto(tx_pkt.to_json().encode(), addr)

            # WAIT FOR ACK
            try:
                response, _ = self.sock.recvfrom(4096)
                ack_pkt = Packet.from_json(response.decode())

                print(f"[CLIENT DEBUG] got ACK={ack_pkt.ack}, expected={self.seq}, valid={ack_pkt.is_valid()}")

                if (
                    ack_pkt.flags == "ACK"
                    and ack_pkt.ack == self.seq
                    and ack_pkt.is_valid()
                ):
                    print("[SUCCESS] ACK received\n")
                    self.seq += 1
                    break

            except socket.timeout:
                print("[TIMEOUT] Retransmitting...\n")

    # RECEIVE 
    def receive(self):
        while True:
            pkt, addr = self.receive_raw()

            # 1. checksum validity: drop packet and do not ACK 
            if not pkt.is_valid():
                print("[CORRUPTION] Packet dropped")
                continue

            # 2. duplicate detection: igmore if same SEQ
            if pkt.flags == "DATA" and pkt.seq == self.last_received_seq:
                print("[DUPLICATE] Duplicate packet received, re-sending ACK")
                ack = Packet(ack=pkt.seq, flags="ACK")
                self.sock.sendto(ack.to_json().encode(), addr)
                continue

            self.last_received_seq = pkt.seq

            # CONTROL PACKETS 
            if pkt.flags in ["SYN", "SYNACK", "ACK", "FIN"]:
                return pkt, addr   # keep full packet for handshake

            # DATA PACKETS 
            if pkt.flags == "DATA":
                print(f"[SERVER DEBUG] sending ACK for SEQ={pkt.seq}")
                ack = Packet(ack=pkt.seq, flags="ACK")
                self.sock.sendto(ack.to_json().encode(), addr)

                print(f"[ACK SENT] ACK={pkt.seq}")
                return pkt.data, addr

    # RAW RECEIVE
    def receive_raw(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(4096)
                pkt = Packet.from_json(data.decode())
                return pkt, addr
            except Exception:
                # did not use continue to avoid deadlock
                time.sleep(0.01)

    # CLOSE CONNECTION
    def close(self, addr):
        fin = Packet(seq=self.seq, flags="FIN")
        self.sock.sendto(fin.to_json().encode(), addr)

        print("[FIN] Sent")

        ack, _ = self.receive_raw()
        if ack.flags == "ACK":
            print("[FIN] ACK received → Closed connection")