"""
Created on Apr 16, 2019
@author: Ange Andries
@name: selector-collision-finder.py

"""

import argparse
import itertools
import math
import multiprocessing as mp
import time

from Cryptodome.Hash import keccak

# Default values
global seed
global maxCollisionNum
global params
global methodID

seed = ''
maxCollisionNum = 1
params = []
ti = time.time()

# Generating contract ABI types
M = [8, 16, 24, 32, 40, 48, 56, 64, 72, 80, 88, 96, 104, 112, 120, 128, 136, 144, 152, 160, 168, 176, 184, 192, 200,
     208, 216, 224, 232, 240, 248, 256]
N = list(range(1, 81))
uintL = ['uint' + str(num) for num in M]
intL = ['int' + str(num) for num in M]
fixedL = ['fixed' + str(x) + 'x' + str(y) for x in M for y in N]
ufixedL = ['u' + i for i in fixedL]
bytes = ['bytes', 'bytes8', 'bytes16', 'bytes24', 'bytes32']
types = list(itertools.chain.from_iterable(
    [uintL, intL, fixedL, ufixedL, bytes, ['address', 'bool', 'function', 'string', 'function']]))
types = list(itertools.chain.from_iterable([types, [str(i) + '[]' for i in types]]))

parser = argparse.ArgumentParser(description='Find a collision with a given function selector')
parser.add_argument('-i', '--input',
                    help='The input string representing the signature of the function. e.g: baz(uint32,bool)',
                    required=True)
parser.add_argument('-s', '--seed', help='The prefix the collision function should start with (default: '')',
                    required=False)
parser.add_argument('-c', '--maxColl', type=int, help='Number of collision to find before stopping (default: 1)',
                    required=False)
parser.add_argument('-p', '--params', nargs='*', action='append', metavar='type1 type2 .. typeN', choices=types,
                    help='List of parameters types for the collision function. (default: empty)', required=False)
args = parser.parse_args()


def singleProcessHash():
    """Use a single process to compute and return one collision."""
    count = 0
    ti = time.time()
    while True:
        if params:
            msg = seed + str(count) + '(' + ','.join(*params if params else '') + ')'
        else:
            msg = seed + str(count) + '()'
        k = keccak.new(digest_bits=256)
        k.update(msg.encode('utf-8'))
        seedID = k.hexdigest()[:8]
        if methodID == seedID:
            break
        count += 1

    print('Single-process run time: {:0.4f}'.format(time.time() - ti))
    print('Collision: ', msg)
    return msg


def findCollision(count):
    if params:
        msg = seed + str(count) + '(' + ','.join(*params if params else '') + ')'
    else:
        msg = seed + str(count) + '()'
    k = keccak.new(digest_bits=256)
    k.update(msg.encode('utf-8'))
    seedID = k.hexdigest()[:8]
    if methodID == seedID:
        return msg
    return


def multiProcessHash():
    """Use multiple processes to compute and return maxCollisionNum collisions."""
    mult = 1
    found = 0
    numValues = 10 ** 6
    chunkSize = math.ceil(numValues / mp.cpu_count())

    pool = mp.Pool(processes=mp.cpu_count())

    while found != maxCollisionNum:
        sample = range(numValues * (mult - 1), numValues * mult)
        mult += 1

        for msg in pool.imap_unordered(findCollision, sample, chunkSize):
            if msg != None:
                found += 1
                print('Found collision: ', msg)

        print("-----------------------------------------------")
        print("Number of values tested: ", numValues * mult)
        print("(Time elapsed: {:0.4f}s)".format(int(time.time() - ti)))
        print("-----------------------------------------------")

    pool.terminate()
    pool.join()

    print('Multi-process run time: {:0.4f}'.format(time.time() - ti))
    return


def showInfo(input):
    print('-----------------------------------------------')
    print('Solidity function selector collision finder')
    print('created by Ange Andries')
    print("Licence: GPL GNU")
    print('-----------------------------------------------')

    print('Input function: {}\nMethodID: 0x{}\nCollision prefix: {}'.format(input, methodID,
                                                                            seed if seed else 'No prefix'))
    if params:
        print('\nParameters types: {}'.format(', '.join(*params)))
    print('\nThe program will find {} collision(s) before stopping'.format(maxCollisionNum))


if __name__ == '__main__':

    if args.seed:
        seed = args.seed
    if args.maxColl:
        maxCollisionNum = args.maxColl
    if args.params:
        params = args.params

    k = keccak.new(digest_bits=256)
    k.update((args.input).encode('utf-8'))
    methodID = k.hexdigest()[:8]

    showInfo(args.input)
    # singleProcessHash()
    multiProcessHash()
