#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import sys
#import lib.mffd
import lib

import timeit
import random


test_module='awf'

data = [random.randrange(1,699) for x in range(1000)]
#data = [int(x) for x in sys.stdin.readlines()]

timer = timeit.Timer('list(lib.%s.pack(*data))' % test_module, "from __main__ import data; import lib.%s" % test_module)

runtime = timer.timeit(number=10)
print "Runtime (10 runs): %s" % runtime 

bin_count, item_count = 0,0
sum_waste, sum_output = 0,0
exceeds, empties = False, False
mod = eval('lib.%s' % test_module)
for x in mod.pack(*data):
    sum_output += sum(x)
    lsum = 800 - sum(x)
    sum_waste += lsum
    bin_count +=1
    item_count += len(x)
    exceeds = exceeds or lsum < 0
    empties = empties and len(x)
#    print "%s |\t%s\t%s" % (str(bin_count).zfill(3),lsum, x)

print "Space to pack:\t%i" % sum(data)
print "Best Possible:\t%i" % round((sum(data) / 800) - 0.5)
print "Bins used:\t%i" % bin_count
print "Total waste:\t%i" % sum_waste
if bin_count != 0:
    print "Average waste:\t", sum_waste / bin_count # avgwaste
else:
    print "Average waste:\t0"
print "Correctness (number of items):\t", item_count == len(data)
print "Correctness (sum of items):\t", sum(data) == sum_output
print "Correctness (no overflowing bins):\t", not exceeds
print "Correctness (no empty bins):\t", not empties
print
