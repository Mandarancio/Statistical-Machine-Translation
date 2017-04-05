import math
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
        # self.__expectation__= {}
        self.__epsilon__ = epsilon
        self.__t__ = ts
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
        count = defaultdict(lambda: defaultdict(float))
        # Number of classes
        total = defaultdict(float)
        probabilites = defaultdict(lambda: 1)
        print('   counting...')
        for c in data:
            s = c['source'].split()
            t = c['target'].split()
            s_total = defaultdict(float)
            for w in s:
                for k in t:
                    s_total[w] += self.__t__[w][k]
            for w in s:
                for k in t:
                    p = self.__t__[w][k]
                    count[w][k] += p/s_total[w]
                    total[k]+= p/s_total[w]
            del s_total
        print('   normalizing...')
        for e in count:
            for f in count[e]:
                count[e][f]/=total[f]
        del total
        return count

    def __maximization(self, exp):
        """
        maximization step
        """
        return exp

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
                diff += math.fabs(teta[x][k]-self.__t__[x][k])
                size+=1
        if self.__Debug__:
            print('   average diff: {}'.format(diff/size))
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
            exp = self.__maximization(exp)
            diff = self.__diff(teta)
            counter += 1
            del self.__t__
            self.__t__ = exp
            if diff <= self.__epsilon__:
                converged = True
                if self.__Debug__:
                    print('\n --- CONVERGED AFTER {} iterations ---\n'.format(counter))
        return self.__t__
