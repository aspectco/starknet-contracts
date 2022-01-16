import random

from utils.constants import MAX_RANGE_CHECK_BOUND, MAX_FELT_VAL
from utils.utils import uint256


def random_large_int_list(minimum, maximum, size):
    res = []
    for i in range(size):
        res.append(random.randint(minimum, maximum))
    return res

def generate_random_felt_list():
    return  list(range(0, 11)) + \
        random.sample(range(10, 99), 5) + \
        random.sample(range(1000, 9999), 5) + \
        random.sample(range(10000, 99999), 10) + \
        random_large_int_list(int("1"*32), MAX_RANGE_CHECK_BOUND, 50) + \
        [MAX_RANGE_CHECK_BOUND]

def generate_random_uint256_list():
    random_felt_list = generate_random_felt_list()
    return [uint256(i) for i in random_felt_list] + \
        [uint256(i) for i in random_large_int_list(2**128, 2**256, 20)] + \
        [uint256(2**256-1)]

