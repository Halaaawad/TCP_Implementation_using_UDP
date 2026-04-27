import random

config = {
    "LOSS_PROB": 0.0,
    "CORRUPT_PROB": 0.0
}

#LOSS_PROB = 0.5
#CORRUPT_PROB = 0.5 #retransmission   
#LOSS_PROB = 0.8
#CORRUPT_PROB = 0.0  #packet loss
#LOSS_PROB = 0.3   #packet corruption
#CORRUPT_PROB = 0.7


# PACKET LOSS
def simulate_loss():
    """
    Simulates packet loss (packet never reaches receiver)
    """
    if random.random() < config["LOSS_PROB"]:
        print("[SIMULATION] PACKET LOST (not delivered)")
        return True
    return False


# CHECKSUM CORRUPTION 
def simulate_corruption(packet):
    if getattr(packet, "corrupted_once", False):
        return packet

    if random.random() < config["CORRUPT_PROB"]:
        print("[SIMULATION] CORRUPTION GENERATED")

        # Change ONLY the data
        packet.data = "CORRUPTED_DATA"
        # Keep old checksum → mismatch happens naturally

    return packet