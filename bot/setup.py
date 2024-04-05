import os

# local
from utils import file

if not os.path.exists(file("auth.csv")):
    with open(file("auth.csv"), "w") as f:
        f.write("user;pass\n")

if not os.path.exists(file("splashes.txt")):
    with open(file("splashes.txt"), "x") as f:
        pass