#! /usr/bin/env python3

import random
import string

def randompassword(size=20):
    chars = string.ascii_letters + string.digits + string.punctuation
    pw = "".join([random.choice(chars) for i in range (size)])
    print(pw)

def randompassphrase(size=4):
    f = open('/usr/share/dict/cracklib-small','r')
    words = f.readlines()
    words = [w[:-1] for w in words]
    pph = ' '.join([random.choice(words) for i in range(size)])
    print(pph)

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        randompassphrase(int(sys.argv[1]))
    else:
        randompassphrase()

