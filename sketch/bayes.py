from itertools import product


# Currently, we're using only DE and US numbers to associate changesets between repos.
# So, we're only seeing a subset of the data here.

# These are the numbers gotten from queries.sql
# Data represents all changesets after the repo split and excluding all changesets with only build.env (i.e., pinning changesets)
data = {
    "GSD":1214,
    "GSD,JDCore":94,
    "GSD,JDCore,VTCore":14,
    "GSD,VTCore":27,
    "JDCore":162,
    "JDCore,VTCore":2,
    "VTCore":79,
}
# Data3 represents all changesets after the repo split, but including the build.env
data3 = {
    "GSD":1208,
    "GSD,JDCore":82,
    "GSD,JDCore,VTCore":50,
    "GSD,VTCore":42,
    "JDCore":154,
    "JDCore,VTCore":3,
    "VTCore":66,
}
# Data2 represents all changesets including those predating the repo split
data2 = {
    "GSD":6064,
    "JDCore2":164,
    "VTCore2":66,
    "GSD,JDCore2":426,
    "GSD,JDCore2,VTCore2":50,
    "GSD,VTCore2":42,
    "JDCore2,VTCore2":3
}

# Probability of A within all cases of B; if B is not given, B = everything
def pX(a, b=''):
    bData = filter(lambda x: b in x[0], data.items())
    aWithinB = filter(lambda y: a in y[0], bData)
    num = sum(map(lambda x: x[1], aWithinB))
    denom = sum(map(lambda x: x[1], bData))
    rtn = num / float(denom)
    return rtn

def b(a,b):
    pA = pX(a)
    pB = pX(b)
    pBWhenA = pX(b, a)
    pAWhenB = pBWhenA * pA / pB
    expr = "P(%s|%s) * P(%s) / P(%s) = %3.3f * %3.3f / %3.3f" % (b, a, b, a, pBWhenA, pB, pA)
    return (expr, pAWhenB * 100)

# These are the pairings we want to compare
keys = ["GSD","VTCore","JDCore","GSD,JDCore","GSD,VTCore", "JDCore,VTCore"]

class strify(object):
    def __init__(self, x):
        (i,j) = x
        (expr, prob) = b(i,j)
        p = "P(%s|%s)" % (i,j)
        self.prob = prob
        self.s = "%20.20s = %73.73s = %.2f%%" % (p, expr, prob)

    def __str__(self):
        return self.s

    def __lt__(self, other):
        return self.prob < other.prob
        

def isNonsense(x):
    if x:
        (i,j) = x
        return (i not in j) and (j not in i) and not (',' in i and ',' in j)
    return False

def main():
    print "Bayesian Probability: P(A|B) = P(B|A) * P(A) / P(B)"
    print "I.e., what is the chance of A changing when B changes?\n"

    pairs = filter(isNonsense, product(keys, keys))
    data = map(strify, pairs)
    sortedData = sorted(data, reverse=True)
    printableData = map(str, sortedData)
    print "\n".join(printableData)


if __name__ == '__main__':
        main()
