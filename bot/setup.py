import os

# local
from utils import file

if not os.path.exists(file("auth.csv")):
    with open(file("auth.csv"), "w") as f:
        f.write("user;pass\n")

if not os.path.exists(file("stats.csv")):
    with open(file("stats.csv"), "w") as f:
        f.write("wins;losses\n0;0")