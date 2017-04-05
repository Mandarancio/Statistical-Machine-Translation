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
    def __init__(self, ts, epsilon=1e-3, debug=False):
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
        exp = defaultdict(lambda: defaultdict(float))
        # Number of classes
        probabilites = defaultdict(lambda: 1)
    
        for c in data:
            s = ibm1.split(c['source'])
            t = ibm1.split(c['target'])
            for w in s:
                for k in t:
                    exp[w][k] += self.__ibm1__.t(w,k)
        return exp

    def __maximization(self, exp):
        """
        maximization step
        """
        # new tetas
        tetas = exp
        for x in self.__tetas__:
            total = 0
            for k in self.__tetas__[x]:
                total += tetas[x][k]
            if total > 0:     
                for k in self.__tetas__[x]:
                    tetas[x][k] /= total
        return tetas

    def __diff(self, teta):
        """
        difference between new tetas and old tetas
        """
        diff = 0
        size = 0
        if self.__Debug__:
            print('  Computing difference...')
        for x in teta:
            for k in teta[x]:
                diff += math.fabs(teta[x][k]-self.__tetas__[x][k])
                size+=1
        if self.__Debug__:
            print('  average diff: {}'.format(diff/size))
        return diff/size

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
                print('\n Iteration:  {}'.format(counter+1))
                print('  Expectation step...')
            exp = self.__expectation(data)
            if self.__Debug__:
                print('  Maximation step...')
            teta = self.__maximization(exp)
            diff = self.__diff(teta)
            counter += 1
            self.__tetas__ = teta
            self.__ibm1__.set_ts(teta)
            if diff <= self.__epsilon__:
                converged = True
                if self.__Debug__:
                    print('\n --- CONVERGED AFTER {} iterations ---\n'.fomat(counter))
        return self.__tetas__
