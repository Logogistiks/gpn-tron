import os

if not os.path.exists("auth.csv"):
    with open("auth.csv", "w") as f:
        f.write("user;pass\n")

if not os.path.exists("stats.txt"):
    with open("stats.csv", "w") as f:
        f.write("wins;losses\n0;0")