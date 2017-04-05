import sys
import json
from collections import defaultdict

def generate_training_data(datas):
    tetas = defaultdict(lambda: defaultdict(float))
    counter = defaultdict(float)
    sentences =[]
    for data in datas:
        sentences.append({
            "source": data[0],
            "target": data[1]
        })
        s = data[0].strip().split()
        t = data[1].strip().split()
        for w in s:
            for k in t:
                counter[w]+=1
                tetas[w][k]+=1
    print("Normalize relative frequencies")
    c = 0
    for w in counter:
        for k in tetas[w]:
            tetas[w][k]/=counter[w]
        c+=1
        sys.stdout.write('\r{} words'.format(c))
        sys.stdout.flush()
    print('')
    return sentences, tetas

def read_training(sourcepath, targetpath):
    print("Computing relative frequencies...")
    source = open(sourcepath, 'r')
    target = open(targetpath, 'r')
    count = 0
    for s in source:
        t = target.readline()
        count+=1 
        sys.stdout.write('\r{} lines'.format(count))
        sys.stdout.flush()
        yield [s,t]
    print('')


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Config file needed!\nEx: config.json")
        sys.exit(0)

    conf = sys.argv[1]

    with open(conf) as data_file:
        config = json.load(data_file)
    folder = config['training']['path']
    s_path = folder + config['training']['sourcefile']
    t_path = folder + config['training']['targetfile']
    print('Using files: {}, {}'.format(s_path, t_path))
    o_path = folder + config['training']['datafile']
    sentences, tetas = generate_training_data(read_training(s_path, t_path))
    print('Saving training data >> {}'.format(o_path))
    with open(o_path,"w") as f:
        output = {
            "sentences": sentences,
            "tetas" : tetas
        }
        json.dump(output,f)
    