import hashlib
import json

# UDP doesnt include packet structure, so we define our own
class Packet:
    def __init__(self, seq=0, ack=0, flags="", data="", checksum=None):
        self.seq = seq
        self.ack = ack
        self.flags = flags  # SYN, SYNACK, ACK, DATA, FIN
        self.data = data
        self.checksum = checksum or self.calculate_checksum()

    def calculate_checksum(self):
        content = f"{self.seq}{self.ack}{self.flags}{self.data}"
        return hashlib.md5(content.encode()).hexdigest()

    def to_json(self):
        return json.dumps({
            "seq": self.seq,
            "ack": self.ack,
            "flags": self.flags,
            "data": self.data,
            "checksum": self.checksum
        })

    @staticmethod
    def from_json(json_str):
        data = json.loads(json_str)

        pkt = Packet(
            seq=data.get("seq", 0),
            ack=data.get("ack", 0),
            flags=data.get("flags", ""),
            data=data.get("data", ""),
            checksum=data.get("checksum", "")
        )

        return pkt

    def is_valid(self):
        return self.checksum == self.calculate_checksum()
    
    # changes data to simulate corruption, but keeps checksum the same (invalid)
    def corrupt_packet(self):
        self.data = "CORRUPTED_DATA"
        
    # for debugging and Wireshark analysis
    def __str__(self):
        return f"Packet(seq={self.seq}, ack={self.ack}, flags={self.flags}, data={self.data})"