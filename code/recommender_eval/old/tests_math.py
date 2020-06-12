from numpy import long
from scipy.special import factorial
from scipy import stats

import math


def sign_test(n=0, n_a=0):
    return stats.binom_test(n_a, n, p=0.5)


def create_biases():
    pass


def analyze_whos_better(random, my, movie, user_data):
    if my.empty:
        return 1
    return 0
