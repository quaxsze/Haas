import os
import hashlib

from string import ascii_letters
from itertools import product

from app import app, celery
from app.hash_utils import hash_str, CHARSET, BF_MAXLEN, BF_MINLEN


@celery.task()
def compute_hash(data, algorithm):
    return hash_str(data, algorithm)


@celery.task
def brute_force(hash_in, hash_type):
        for i in range(BF_MINLEN, BF_MAXLEN+1):
            for p in product(CHARSET, repeat=i):
                word = ''.join(p)
                if hash_str(word, hash_type) == hash_in:
                    return word


@celery.task
def dict_attack(hash_in, hash_type, wordlist):
    for word in wordlist:
        if hash_str(word, hash_type) == hash_in:
            return word