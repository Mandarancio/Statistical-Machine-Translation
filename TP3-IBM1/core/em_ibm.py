import math
from collections import defaultdict
import sys


def print_teta(teta):
    """
    Pretty print for translation table
    :param teta: translation table
    """
    for k in teta:
        print(' - ' + k + ' : ')
        for kk in teta[k]:
            print('   + ' + kk + ' : ' + str(teta[k][kk]))


class EM_ibm1:
    """
    Simple EM algorithm for the IBM1 model
    :param ts: initial translation probabilites table (used as teta)
    :param epsilon: convergence epsilon value
    :param debug: debug flag
    """

    def __init__(self, ts, epsilon=1e-5):
        # self.__expectation__= {}
        self.__epsilon__ = epsilon
        self.__t__ = ts

    def tetas(self):
        """
        :return: the tetas of the EM, equivalent to the translation table
        """
        return self.__t__

    def __step(self, data):
        """
        optimization step
        :param data: training data
        :return: new translation table
        """
        # counter
        count = defaultdict(lambda: defaultdict(float))
        # Normalizer factor for class
        total = defaultdict(float)
        sys.stdout.write('   counting: 0 sentences')
        sys.stdout.flush()
        counter = 0
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
                    count[w][k] += p / s_total[w]
                    total[k] += p / s_total[w]
            del s_total
            counter += 1
            sys.stdout.write('\r   counting: {} senteces'.format(counter))
        print()
        sys.stdout.write('   normalizing: 0 words')
        counter = 0
        for e in count:
            for f in count[e]:
                count[e][f] /= total[f]
                counter += 1
            sys.stdout.write('\r   normalizing: {} words'.format(counter))
        print('')
        del total
        return count

    def __diff(self, teta):
        """
        difference between new tetas and old tetas
        :param teta: new translation table
        :return: avarage difference between new and old translation table
        """
        diff = 0
        size = 0
        print('  Computing difference...')
        for x in teta:
            for k in teta[x]:
                diff += math.fabs(teta[x][k] - self.__t__[x][k])
                size += 1
        print('   average diff: {}'.format(diff / size))
        return diff / size

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
            print('\n Iteration:  {}'.format(counter + 1))
            print('  Expectation step...')
            exp = self.__step(data)
            print('  Maximation step...')
            # diff = self.__diff(exp)
            counter += 1
            del self.__t__
            self.__t__ = exp
            # if diff <= self.__epsilon__:
            #     converged = True
            #     if self.__Debug__:
            #        print('\n --- CONVERGED AFTER {} iterations ---\n'.format(
            #                 counter))
        return self.__t__
