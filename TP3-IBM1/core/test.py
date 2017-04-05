#! /usr/bin/python3
# Martino Ferrari
import json
import ibm1
import sys


if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Config file needed!\nEx: config.json")
        sys.exit(0)
    print('loading translation table...')
    with open(sys.argv[1]) as f:
        tetas = json.load(f)

    s = "those guidelines are presented below ."
    t = "más abajo figuran dichas directrices ."

    print(t)
    print(s)

    t = t.split()
    s = s.split()
    tm = ibm1.IBM1(tetas)

    print(tm.best_alignment(s, t))
