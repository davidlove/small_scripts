#! /usr/bin/env python3

import argparse
import math
import random
import string


def _read_wordlist(dictionary_file, max_len=None, skip_chars=''):
    """Read a dictionary file and return all words shorter than maxlen"""
    with open(dictionary_file) as f:
        words = [w[:-1] for w in f.readlines() if not any(c in w for c in skip_chars)]
    if max_len is not None:
        return [w for w in words if len(w) <= max_len and not any(c in w for c in skip_chars)]
    return words


def randompassword(size=20):
    chars = string.ascii_letters + string.digits + string.punctuation
    pw = "".join([random.choice(chars) for i in range (size)])
    print(pw)


def randompassphrase(words, size):
    pph = ' '.join([random.choice(words) for i in range(size)])
    return pph


def password_entropy(words, size):
    return int(math.log2(len(words)**size))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--num_words', type=int, default=4)
    parser.add_argument('-l', '--max-length', type=int, default=None)
    parser.add_argument('-f', '--file', type=str, default='/usr/share/dict/cracklib-small')
    parser.add_argument('-s', '--skip-chars', type=str, default='')
    args = parser.parse_args()

    words = _read_wordlist(args.file, args.max_length, args.skip_chars)
    rp = randompassphrase(words, args.num_words)
    print(rp)
    print(f'Num words: {len(words)}, entropy: {password_entropy(words, args.num_words)}')

