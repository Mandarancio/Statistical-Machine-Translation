#! /usr/bin/python3
# Martino Ferrari
import json
import sys
import core.train as T
import time

'''
Optional script to generate and store the translation tables, instead of
compute it on the fly every time.
'''

if __name__ == "__main__":
    if len(sys.argv) == 2:
        conf = sys.argv[1]
    conf = "conf.json"

    with open(conf) as data_file:
        config = json.load(data_file)

    print('Reading initial values and sentences...')

    output = config['training']['translationfile']
    t = time.time()
    teta = T.train(config)
    t = time.time() - t
    print("time to train {}s".format(t))
    print('save >> {}'.format(output))
    with open(output, 'w') as f:
        json.dump(teta, f)
