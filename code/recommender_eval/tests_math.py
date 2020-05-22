from numpy import long
from scipy.special import factorial
from scipy import stats

import math


def sign_test(n=0, n_a=0):
    return stats.binom_test(n_a, n, p=0.5)


print(sign_test(100_000, 50_000))
