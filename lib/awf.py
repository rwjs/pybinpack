#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import *

def fits_in_bin(item, b, binsize, dimensions=1):

    if dimensions == 1:
        return (binsize[0] - sum(b)) >= item
    for dim in range(0, dimensions):
        # TODO - Rotation
        if (binsize[dim] - (sum(y[dim] for y in b))) >= item[dim]:
            return True
    return False


def pack(*items, **kwargs):
    """ Almost Worst-Fit. Offline.

    The items are packed into the second-emptiest bin. Some sources indicate
    that this heuristic is provably better than Worst Fit, but I have thus far
    been unable to locate anything definitive."""


    bins = kwargs.get('bins', [[]])
    dimensions = kwargs.get('dimensions', 1)
    key = kwargs.get('key', lambda x:x)
    binsize = kwargs.get('binsize', 800)

    weight = kwargs.get('weight', 1)

    if callable(key):
        key=(key, ) * dimensions
    if not hasattr(binsize, '__getitem__'):
        binsize = (binsize, ) * dimensions
    if not hasattr(weight, '__getitem__'):
        weight = (weight, ) * dimensions

    for item in items:
        for dim in range(0, dimensions):
            for name, checkme in (
                                    (item, 'item'), 
                                    (key, 'key'), 
                                    (binsize, 'binsize'),
                                    (weight, 'weight'),
                                 ):
                try:
                    checkme[dim]
                except IndexError:
                    raise TooFewDimensions("%s %s has too few dimensions" % (name, checkme))
                    break

        if dimensions == 1 and item > binsize[0]:
            yield DoesNotFitWarning("Does not fit - %s" % item)
            continue
        elif dimensions != 1 and any([v > binsize[d] for d,v in enumerate(item)]):
            yield DoesNotFitWarning(item)
            continue

        else:
            for b in bins[1:2] + bins[0:1] + bins[2:]: #almost-worst + worst + rest
                if fits_in_bin(item, b, binsize, dimensions):
                    b.append(item)
                    break
            else:
                bins.append([item]) # new bin

        if dimensions == 1:
            bins.sort(key=lambda b: sum(key[0](v) * weight[0] for v in b))
        else:
            bins.sort(key=lambda b: sum(sum(key[d](v) * weight[d] for d,v in enumerate(i)) for i in b))

    for b in bins:
#        print "DEBUG: >>%s<<" % b
        yield b
