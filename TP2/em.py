import math


class EM:
    def __init__(self, init_tetas, epsilon=1e-10):
        self.__tetas__ = init_tetas
        # self.__expectation__= {}
        self.__epsilon__ = epsilon

    def tetas(self):
        return self.__tetas__

    def __expectation(self, data):
        # Computed expectation
        exp = {}
        # Number of classes
        N = 1/len(self.__tetas__)
        probabilites = {}
        for x in self.__tetas__:
            exp[x] = {}
            probabilites[x] = 1
            for k in self.__tetas__[x]:
                exp[x][k] = 0

            # Number of realizations
            M = len(x)

        for r in data:
            events = {}
            for k in r:
                if k in events:
                    events[k] += 1
                else:
                    events[k] = 1
            denominator = 0
            for x in probabilites:
                probabilites[x] = 1
                for k in events:
                    probabilites[x] *= (self.__tetas__[x][k]**events[k])
                denominator += probabilites[x]
            for x in exp:
                for k in events:
                    exp[x][k] += (probabilites[x]/denominator)*events[k]
        return exp

    def __maximization(self, exp):
        # new tetas
        tetas = {}
        for x in self.__tetas__:
            total = 0
            tetas[x] = {}
            for k in self.__tetas__[x]:
                tetas[x][k] = exp[x][k]
                total += exp[x][k]
            for k in self.__tetas__[x]:
                tetas[x][k] /= total
        return tetas

    def __diff(self, teta):
        diff = 0
        for x in teta:
            for k in teta[x]:
                diff += math.fabs(teta[x][k]-self.__tetas__[x][k])
        return diff

    def optimize(self, data, MAX=1e9):
        converged = False
        counter = 0
        while not converged and counter < MAX:
            exp = self.__expectation(data)
            teta = self.__maximization(exp)
            diff = self.__diff(teta)
            counter += 1
            self.__tetas__ = teta
            if diff <= self.__epsilon__:
                converged = True
                print('converged after '+str(counter)+' iterations')
        return self.__tetas__
