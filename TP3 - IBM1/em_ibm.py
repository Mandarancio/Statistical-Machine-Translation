import math
import ibm1
from collections import defaultdict


def print_teta(teta):
    for k in teta:
        print(' - '+k+' : ')
        for kk in teta[k]:
            print('   + '+kk+' : '+str(teta[k][kk]))


class EM_ibm1:
    """
    Simple EM algorithm for the IBM1 model
    :param ts: initial translation probabilites table (used as teta)
    :param epsilon: convergence epsilon value
    :param debug: debug flag
    """
    def __init__(self, ts, epsilon=1e-5, debug=False):
        self.__tetas__ = ts
        # self.__expectation__= {}
        self.__epsilon__ = epsilon
        self.__ibm1__ = ibm1.IBM1(ts)
        self.__Debug__ = debug

    def tetas(self):
        """
        :return: the tetas of the EM, equivalent to the translation table
        """
        return self.__tetas__

    def __expectation(self, data):
        """
        expectation step
        """
        # Computed expectation
        exp = defaultdict()
        # Number of classes
        probabilites = defaultdict()
        for x in self.__tetas__:
            exp[x] = defaultdict()
            probabilites[x] = 1
            for k in self.__tetas__[x]:
                exp[x][k] = 0

            # Number of realizations
            # M = len(x)

        for c in data:
            f = ibm1.split(c['source'])
            e = ibm1.split(c['target'])
            als, probs = self.__ibm1__.all_alignments(f, e)
            if self.__Debug__:
                print('\n'+' '.join(e))
            for j in range(0, len(als)):
                p = probs[j]
                r = []
                for x in als[j]:
                    r.append(e[x])
                if self.__Debug__:
                    print(' '.join(r)+' : '+str(p))

                denominator = 0
                for x in probabilites:
                    if (x in f):
                        # print('x: '+x)
                        probabilites[x] = 1
                        for k in r:
                            probabilites[x] *= (self.__tetas__[x][k] ** p)
                for x in exp:
                    if x in f:
                        for k in r:
                            exp[x][k] += probabilites[x]

        for x in exp:
            d = 0
            for k in exp[x]:
                d += exp[x][k]
            for k in exp[x]:
                exp[x][k] /= d
        # print_teta(exp)

        return exp

    def __maximization(self, exp):
        """
        maximization step
        """
        # new tetas
        tetas = {}
        for x in self.__tetas__:
            total = 0
            tetas[x] = {}
            for k in self.__tetas__[x]:
                tetas[x][k] = exp[x][k]
                total += exp[x][k]
            for k in self.__tetas__[x]:
                if total > 0:
                    tetas[x][k] /= total
        return tetas

    def __diff(self, teta):
        """
        difference between new tetas and old tetas
        """
        diff = 0
        for x in teta:
            for k in teta[x]:
                diff += math.fabs(teta[x][k]-self.__tetas__[x][k])
        return diff

    def optimize(self, data, MAX=1e9):
        """
        unsuperivised optimize function
        :param data: training dataset
        :param MAX: maximum number of iterations
        :return: optimized tetas (equivalent to the translation probabilites)
        """
        converged = False
        counter = 0
        while not converged and counter < MAX:
            if self.__Debug__:
                print('\n --- '+str(counter+1)+' --- ')
            exp = self.__expectation(data)
            teta = self.__maximization(exp)
            diff = self.__diff(teta)
            counter += 1
            self.__tetas__ = teta
            self.__ibm1__.set_ts(teta)
            if self.__Debug__:
                print('\n --- TS --- \n')
                print_teta(teta)
                print("\nWait for input for next iteration")
                input()
            if diff <= self.__epsilon__:
                converged = True
                if self.__Debug__:
                    print('\n --- CONVERGED AFTER '+str(counter)+' iterations '
                          + '---\n')
        return self.__tetas__
