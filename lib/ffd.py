#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __init__ import *

def pack(*items, **kwargs):
    """ First-Fit Decreasing bin-packing heuristic.
    
    The items are sorted into 'decreasing' order (largest->smallest), then they
    are packed into the first bins that fit them. """

    key = kwargs.get('key', lambda x:x)
    binsize = kwargs.get('binsize', 800)
    bins = kwargs.get('bins', [[]])
    
    items = sorted(items, key=key, reverse=True) # largest -> smallest

    for e,item in enumerate(items):
        index_bins = 0
        size_item = key(item)
        if size_item > binsize:
            yield DoesNotFitWarning(item)
            continue
        while index_bins < len(bins):
        # `while` used (over `for`), as the list is being modified.
            target = bins[index_bins]
            avail_target = binsize - sum((key(x) for x in target))
            if size_item <= avail_target:
                target.append(item)
                break
            else:
                index_bins += 1
        else:
            bins.append([item])
        continue

    for b in bins:
        yield b
