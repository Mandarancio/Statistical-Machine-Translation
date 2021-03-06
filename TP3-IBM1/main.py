#! /usr/bin/python3
# Martino Ferrari
import core.train as t
import core.ibm1 as ibm1
import argparse
import json
import os.path
import sys
import operator
import time


def train(conf):
    '''
    take the configuration and run the em on it.
    :param conf: configuration for the training
    :return: return translation table
    '''
    return t.train(conf)


def align(source, target, translation_table):
    '''
    compute best alignement of the proposed translation
    :param source: original sentence
    :param target: translated sentence
    :param translation_table: translation probabilites table
    :return: best alignement computed by IBM model 1
    '''
    tm = ibm1.IBM1(translation_table)
    alignement, _ = tm.best_alignment(source.split(), target.split())
    return alignement


def test(config, translation_table):
    '''
    Compute alignements and probability on the test data using IBM model 1
    :param config: configuration
    :translation_table: translation table needed for the translation model
    :return: the list of alignements and its probabilites [(al., prob),..]
    '''
    tm = ibm1.IBM1(translation_table)
    sourcepath = config['testing']['sourcefile']
    targetpath = config['testing']['targetfile']
    alignements = []
    parallel_corpus = {}
    with open(sourcepath) as source, open(targetpath) as target:
        for s, t in zip(source, target):
            alignement, prob = tm.best_alignment(s.split(), t.split())
            parallel_corpus[(s, t)] = prob
            alignements.append((alignement, prob))
    return alignements, parallel_corpus


def score(config, test_results):
    '''
    compute precision, recall and f1 score
    of the computed results vs the gold file
    :param config: configuration
    :param test_results: results of the test function
    :return: (precision, recall, f1)
    '''
    guessed = 0
    correct = 0
    total = 0
    t = config['testing']
    with open(t['goldfile']) as goldfile:
        for guess, gold in zip(test_results, goldfile):
            gold = gold.strip().split()
            guess = guess[0]
            guessed += len(guess)
            total += len(gold)
            for g in gold:
                s = int(g.split('-')[1])
                t = int(g.split('-')[0])
                if s < len(guess) and guess[s] == t:
                    correct += 1
        precision = correct / guessed
        recall = correct / total
        f1 = 2 * precision * recall / (precision + recall)

        return (precision, recall, f1)


def write_alignments(outputpath, test_results):
    '''
    write down the alignments on a file in the standard format
    :param outputpath: destination
    :param test_results: computed alignments
    '''
    with open(outputpath, 'w') as f:
        for aln, _ in test_results:
            for i in range(0, len(aln)):
                f.write('{}-{} '.format(aln[i], i))
            f.write('\n')


def write_translations(outputpath, parallel_corpus):
    '''
    write down the translation ordered by its probability
    :param outputpath: destination
    :param parallel_corpus: translations and its probabilites
    '''
    sorted_corpus = sorted(parallel_corpus.items(), key=operator.itemgetter(1),
                           reverse=True)
    with open(outputpath, 'w') as f:
        for sentences, probability in sorted_corpus:
            source = sentences[0].replace('\n', '')
            target = sentences[1].replace('\n', '')
            f.write("{:.3E} : {} <==> {}\n".format(probability, source,
                                                   target))


def __args_to_conf__(args):
    conf = {
        "training": {
            "sourcefile": args.traindata + ".en",
            "targetfile": args.traindata + ".es",
            "nsentences": args.nsentences,
            "translationfile": "resources/tt_en_es.json",
            "em_maxiters": args.em_maxiters,
            "em_epsilon": 0.0001
        },
        "testing": {
            "sourcefile": args.testdata + ".en",
            "targetfile": args.testdata + ".es",
            "goldfile": args.testdata + ".align",
            "alignsfile": "test/myalignments",
            "translationsfile": "test/mytranslations",
            "probsfile": "test/myprobs"
        }
    }
    return conf


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='IBM1 Em & translation model')
    parser.add_argument('--conf', dest='conf',
                        default=None,
                        help='use a json config file (default: None)')
    parser.add_argument('-i', dest='em_maxiters',
                        default=10,
                        help='em max iterations (default: 10)')
    parser.add_argument('-n',  dest='nsentences',
                        default=-1,
                        help='em max iterations (default: -1 [all])')
    parser.add_argument('-t',  dest='traindata',
                        default='training/europarl_50k_es_en',
                        help='training file (default: t../europarl_50k_es_en)')
    parser.add_argument('-s',  dest='testdata',
                        default='test/test',
                        help='test file (default: t../test)')
    args = parser.parse_args()
    conf = __args_to_conf__(args)
    if args.conf is not None:
        with open(args.conf) as f:
            conf = json.load(f)
    if os.path.isfile(conf['training']['translationfile']):
        print('Translation Table exists exists!\nLoading...')
        with open(conf['training']['translationfile']) as f:
            tt = json.load(f)
    else:
        print('Generating Translation Table...')
        co = time.time()
        tt = train(conf)
        co = time.time() - co
        print("Time to train {}s".format(co))
        output = conf['training']['translationfile']
        print("Saving translation_table to {}".format(output))
        with open(output, 'w') as f:
            json.dump(tt, f)

    print('Evaluating...')
    als, parallel_corpus = test(conf, tt)
    write_alignments(conf['testing']['alignsfile'], als)
    write_translations(conf['testing']['translationsfile'], parallel_corpus)
    precision, recall, f1 = score(conf, als)
    print('precision: {:.3f}\nrecall: {:.3f}\nF1: {:.3f}'.format(precision,
                                                                 recall, f1))
