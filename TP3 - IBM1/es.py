import sys
import json
import ibm1
import em_ibm as em
from collections import defaultdict


def read_training(sourcepath, targetpath):
    source = open(sourcepath, 'r')
    target = open(targetpath, 'r')
    datas = []
    for i in range(0, 5):
        datas.append({
            "source": source.readline(),
            "target": target.readline()
        })
    return datas


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
    training_data = read_training(s_path, t_path)
    i_em = em.EM_ibm1(defaultdict(), debug=True)
    i_em.optimize(training_data)
