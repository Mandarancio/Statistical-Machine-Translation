import sys
import json
import em_ibm as em

if len(sys.argv) < 2:
    print("Config file needed!\nEx: config.json")
    sys.exit(0)

conf = sys.argv[1]

with open(conf) as data_file:
    config = json.load(data_file)

i_em = em.EM_ibm1(config["ts"], debug=config["debug"])
em.print_teta(i_em.optimize(config["sentences"], MAX=config["maxiteration"]))
