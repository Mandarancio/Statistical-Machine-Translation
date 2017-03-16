import sys
import json
import ibm1


def sentence(sentence):
    return ' '.join(sentence)


def print_stats(a, pa, pt):
    print('  Best aligment: '+str(a))
    print('  Aligment probability: '+str(pa))
    print('  Translation probability: '+str(pt))


def get_source(config):
    return config['source'].split(' ')


def get_targets(config):
    targets = []
    for s in config['targets']:
        targets.append(s.split(' '))
    return targets


def get_target(config, n):
    return config['targets'][n].split(' ')


if len(sys.argv) < 2:
    print("Config file needed!\nEx: config.json")
    sys.exit(0)

conf = sys.argv[1]

with open(conf) as data_file:
    config = json.load(data_file)

ts = config['ts']
ibm = ibm1.IBM1(ts)
a = [0, 1, 2, 3]
f = get_source(config)
for e in get_targets(config):
    print('F: '+sentence(f))
    print('E: '+sentence(e))
    a, pa = ibm.best_alligment(f, e)
    pt = ibm.translation_probabilty(f, e)
    print_stats(a, pa, pt)
    print()
