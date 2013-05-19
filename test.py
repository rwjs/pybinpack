#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
import sys
import timeit
import random
import lib

from common import *

######## Set defaults ###########
run_count=10
test_module='nf'
binsize=800
dimensions=1

######## Read arguments #########
try:
    sys.argv[1]
    exec('from lib import %s' % sys.argv[1])
    test_module = sys.argv[1]
except IndexError: 
    sys.stderr.write('No algorithm supplied, using default of %s\n' % test_module)
except ImportError:
    sys.stderr.write('No algorithm %s found, using default of %s\n' % (sys.argv[1], test_module))

try:
    run_count = int(sys.argv[2])
except IndexError:
    sys.stderr.write('No run count supplied, using default of %s\n' % run_count)
except TypeError:
    sys.stderr.write('Non-numeric run count supplied, using default of %s\n' % run_count)

try:
    dimensions = int(sys.argv[3])
except IndexError:
    sys.stderr.write('No dimensions supplied, using default of %s\n' % dimensions)
except TypeError:
    sys.stderr.write('Non-numeric dimensions supplied, using default of %s\n' % dimensions)

######## Generate Data ########
if dimensions == 1:
    data = [random.randrange(1,699) for x in range(1000)]
else:
    data = [[random.randrange(1,699) for y in range(0,dimensions)] for x in range(1000)]
    

########### Runtime ###########

runstr='list(lib.%s.pack(*data, dimensions=%i))' % (
        test_module, dimensions)
        
timer = timeit.Timer(runstr, "from __main__ import data; import lib.%s" % test_module)


runtime = timer.timeit(number=run_count)

if dimensions == 1:
    bin_count, item_count = 0,0
    sum_waste, sum_output = 0,0
else:
    bin_count = 0
    item_count = 0
    sum_waste = [0] * dimensions
    sum_output = [0] * dimensions
    binsize = [binsize] * dimensions
    lsum = [0] * dimensions

exceeds, empties = False, False
mod = eval('lib.%s' % test_module)

for x in mod.pack(*data, dimensions=dimensions):
    bin_count += 1
    item_count += len(x)
    empties = empties and len(x)
    if dimensions == 1:
        sum_output += sum(x)
        lsum = binsize - sum(x) # lsum - leftover space sum
        sum_waste += lsum
        exceeds = exceeds or lsum < 0
    else:
        for item in x:
            for e,d in enumerate(item):
                sum_output[e] += d
                lsum[e] = binsize[e] - d
                exceeds = exceeds or lsum < 0
                sum_waste[e] += lsum[e]

## Correctness
if dimensions == 1:
    print "Sum of items OK:         \t%s" % ( sum(data) == sum_output )
    print "Overpacking behaviour OK:\t%s" % (isinstance(mod.pack(binsize+1).next(), DoesNotFitWarning))
else:
    print "Sum of items OK:         \t%s" % all([(sum([x[d] for x in data]) == sum_output[d]) for d in range(0,dimensions)])
    print "Overpacking behaviour OK:\t%s" % (isinstance(mod.pack(binsize[0]+1).next(), DoesNotFitWarning))

print "Number of items OK:      \t%s" % (item_count == len(data))
print "No overflowing bins:     \t%s" % (not exceeds)
print "No empty bins:           \t%s" % (not empties)

## Stats
print "Runtime (%i run%s):    \t\t%s" % (run_count, '' if run_count is 1 else 's', runtime)
if dimensions == 1:
    print "Space to pack:           \t%i" % (sum(data))
    print "Best possible:           \t%i" % (round((sum(data) / binsize) - 0.5))
    print "Average waste:           \t%i" % ( sum_waste / bin_count )
else:
    print "Space to pack:           \t%s" % [sum([x[d] for x in data]) for d in range(0,dimensions)]
    print "Best possible:           \t%s" % [round((sum([x[d] for x in data]) / binsize[d]) - 0.5) for d in range(0, dimensions)]
    print "Average waste:           \t%s" % ([x / bin_count for x in sum_waste])
print "Bins used:               \t%i" % bin_count
print "Total waste:             \t%s" % sum_waste
if bin_count == 0:
    bin_count=float('inf')
