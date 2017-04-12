#! /usr/bin/python3
# Martino Ferrari
import sys
import json
import core.em_ibm as em
from collections import defaultdict


def initialize_translation_table(datas):
    tetas = defaultdict(lambda: defaultdict(float))
    sentences = []
    for data in datas:
        sentences.append({
            "source": data[0],
            "target": data[1]
        })
        s = data[0].strip().split()
        t = data[1].strip().split()
        for w in s:
            for k in t:
                tetas[w][k] = 1

    print("Normalize relative frequencies")
    c = 0
    for w in tetas:
        for k in tetas[w]:
            tetas[w][k] /= len(tetas[w])
        c += 1
        sys.stdout.write('\r{} words'.format(c))
        sys.stdout.flush()
    print('')
    return sentences, tetas


def read_training(sourcepath, targetpath, nsentences=-1):
    print("Computing relative frequencies...")
    source = open(sourcepath, 'r')
    target = open(targetpath, 'r')
    count = 0
    for s in source:
        if nsentences > -1 and count >= nsentences:
            break
        t = target.readline()
        count += 1
        sys.stdout.write('\r{} lines'.format(count))
        sys.stdout.flush()
        yield [s, t]
    print('')


def train(config):
    t = config['training']
    s_path = t['sourcefile']
    t_path = t['targetfile']
    print('Using files: {}, {}'.format(s_path, t_path))

    sentences, tetas = initialize_translation_table(read_training(s_path,
                                                    t_path,
                                                    nsentences=t['nsentences'])
                                                    )

    i_em = em.EM_ibm1(tetas, epsilon=t['em_epsilon'])

    print('Optimizing...')

    teta = i_em.optimize(sentences, MAX=t['em_maxiters'])
    return teta


if __name__ == "__main__":
    if len(sys.argv) == 2:
        conf = sys.argv[1]
    conf = "conf.json"

    with open(conf) as data_file:
        config = json.load(data_file)
    print('Reading initial values and sentences...')

    output = config['training']['translationfile']

    teta = train(config)
    print('save >> {}'.format(output))
    with open(output, 'w') as f:
        json.dump(teta, f)
