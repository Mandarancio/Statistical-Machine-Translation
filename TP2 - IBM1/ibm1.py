import itertools


def split(sentence):
    return sentence.split(' ')


def alligments(f, e):
    '''
    Generate all possible alligments
    '''
    als = []
    for a in itertools.product(range(len(e)), repeat=len(f)):
        als.append(a)
    return als


class IBM1:
    def __init__(self, ts):
        self.__ts__ = ts

    def set_ts(self, ts):
        self.__ts__ = ts

    '''
    compute the probability of a certain word translation
    '''
    def t(self, f, e):
        if f in self.__ts__ and e in self.__ts__[f]:
            return self.__ts__[f][e]
        return 0

    '''
    compute the probability of certain aligment
    in the IBM1  model each aligment is equiprobable
    '''
    def q(self, a, f, e):
        f_len = len(f)
        e_len = len(e)
        return 1./((1+e_len)**f_len)

    '''
    compute the probability of a certain translation f and a certain aligment a
    '''
    def p(self, f, a, e):
        ret = 1
        for j in range(0, len(a)):
            ret *= self.t(f[j], e[a[j]])
        return self.q(a, f, e)*ret

    '''
    Find the best possible aligment
    '''
    def best_alligment(self, f, e):
        als = alligments(f, e)
        selected = als[0]
        probability = self.p(f, selected, e)
        for a in als:
            pt = self.p(f, a, e)
            if pt > probability:
                probability = pt
                selected = a
        return selected, probability

    '''
    Compute the global translation probability
    '''
    def translation_probabilty(self, f, e):
        als = alligments(f, e)
        total = 0
        for a in als:
            total += self.p(f, a, e)
        return total

    def all_allignement(self, f, e):
        als = alligments(f, e)
        pbs = []
        for i in range(0, len(als)):
            pt = self.p(f, als[i], e)
            pbs.append(pt)
        return als, pbs
