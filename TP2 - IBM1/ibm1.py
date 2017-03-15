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
        if e in self.__ts__ and f in self.__ts__[e]:
            return self.__ts__[e][f]
        return 0

    '''
    compute the probability of certain aligment
    in the IBM1  model each aligment is equiprobable
    '''
    def q(self, a, f, e, normed=False):
        f_len = len(f)
        e_len = len(e)
        if normed:
            return 1./(e_len**f_len)
        return 1./((1+e_len)**f_len)

    '''
    compute the probability of a certain translation f and a certain aligment a
    '''
    def p(self, f, a, e, normed=False):
        ret = 1
        for j in range(0, len(f)):
            # print(e[a[j]]+' -> '+f[j]+' : '+str(self.t(f[j], e[a[j]])))
            # debug output
            ret *= self.t(f[j], e[a[j]])
        return self.q(a, f, e, normed)*ret

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

    def all_allignement(self, f, e, normed=False):
        als = alligments(f, e)
        pbs = []
        for i in range(0, len(als)):

            pt = self.p(f, als[i], e, normed)
            pbs.append(pt)
        return als, pbs
