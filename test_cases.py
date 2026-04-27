from utils import LOSS_PROB, CORRUPT_PROB

print("Testing scenarios:")

print("1. No loss, no corruption")
LOSS_PROB = 0.0
CORRUPT_PROB = 0.0

print("2. With packet loss")
LOSS_PROB = 0.3

print("3. With corruption")
CORRUPT_PROB = 0.3