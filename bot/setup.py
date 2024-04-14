import os
from uuid import uuid4

# local
from utils import file

if not os.path.exists(file("auth.csv")):
    with open(file("auth.csv"), "w") as f:
        f.write(f"user;pass\n{uuid4().hex[:10]};{uuid4().hex[:10]}")

if not os.path.exists(file("splashes.txt")):
    with open(file("splashes.txt"), "x") as f:
        pass