import itertools


def split(sentence):
    return sentence.strip().split(' ')


def alignments(f, e):
    """
    Generate all possible alligments for a given couple of sentences
    :param f: source sentence
    :param e: target sentence
    :return: return all possible alignments
    """
    als = []
    for a in itertools.product(range(len(e)), repeat=len(f)):
        als.append(a)
    return als


class IBM1:
    """
    Class for the IBM1 translation model
    """

    def __init__(self, ts):
        """
        Constructor of the IBM1 model
        :param ts: the table of translation probabilites
        """
        self.__ts__ = ts

    def set_ts(self, ts):
        self.__ts__ = ts

    def t(self, fi, ei):
        """
        compute the probability of a certain word translation
        :param fi: source word
        :param ei: target word
        :return: return probability of t(fi|ei)
        """
        if fi in self.__ts__ and ei in self.__ts__[fi]:
            return self.__ts__[fi][ei]
        return 0
    
    def q(self, a, f, e):
        """
        compute the probability of certain aligment
        in the IBM1  model each aligment is equiprobable
        :param a: selected aligment
        :param f: source sentence
        :param e: target sentence
        :return: return 1./((1+e_len)**f_len)
        """
        f_len = len(f)
        e_len = len(e)
        return 1./((1+e_len)**f_len)

    def p(self, f, a, e):
        """
        compute the probability of a certain translation f
        and a certain aligment a
        :param f: source sentence
        :param a: selected alignment
        :param e: target sentence
        :return: return the probability of the selected alignment
        """
        ret = 1
        for j in range(0, len(a)):
            ret *= self.t(f[j], e[a[j]])
        return self.q(a, f, e)*ret

    def best_alignment(self, f, e):
        """
        Find the best possible aligment for a give couple of target and source
        :param f: source sentence
        :param e: target sentence
        :return: return the best aligment and its probability
        """
        als = alignments(f, e)
        selected = als[0]
        probability = self.p(f, selected, e)
        for a in als:
            pt = self.p(f, a, e)
            if pt > probability:
                probability = pt
                selected = a
        return selected, probability

    def translation_probabilty(self, f, e):
        """
        Compute the global translation probability for a give couple of target
        and source
        :param f: source sentence
        :param e: target sentence
        :return: total translation probability
        """
        als = alignments(f, e)
        total = 0
        for a in als:
            total += self.p(f, a, e)
        return total

    def all_alignments(self, f, e):
        """
        return all possible alignments for a give couple of target and source
        :param f: source sentence
        :param e: target sentence
        :return: all alligments ant its probabilites
        """
        als = alignments(f, e)
        pbs = []
        for i in range(0, len(als)):
            pt = self.p(f, als[i], e)
            pbs.append(pt)
        return als, pbs
