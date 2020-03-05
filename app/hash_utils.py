import hashlib
import string
    
WORDLIST_DIR = "wordlists"

CHARSET = string.printable

BF_MINLEN = 1
BF_MAXLEN = 30


def hash_str(string, algorithm):
    h = getattr(hashlib, algorithm)()
    h.update(string.encode('utf-8'))
    return h.hexdigest()


TYPES_DICT = {
    32 : 'md5',
    40 : 'sha1',
    56 : 'sha224',
    64 : 'sha256',
    96 : 'sha384',
    128 : 'sha512'
    }


def validate_hash(hash_in):
    if hash_in.isalnum():
        length = len(hash_in)
        if TYPES_DICT.get(length, None):
            return TYPES_DICT[length]
        else:
            return None
    else:
        return None


def gen_wordlist(self):
    wlist = "list.txt"
    wfile = open(f"{WORDLIST_DIR}/{wlist}", 'r', encoding='utf-8')
    words = wfile.read()
    wfile.close()
    return words.split()