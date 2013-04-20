#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __init__ import *

def pack(*items, **kwargs):
    """ Next-Fit Decreasing

    Next-Fit is perhaps the simplest packing heuristic; it simply packs items in
    the next available bin. This algorithm differs only from Next-Fit
    Decreasing in having a 'sort'; that is, the items are pre-sorted (largest
    to smallest)."""

    key = kwargs.get('key', (lambda x:x,))
    if not hasattr(key, '__getitem__'):
        key=(key,)
    binsize = kwargs.get('binsize', 800)
    if not hasattr(binsize, '__getitem__'):
        binsize=(binsize,)
    bins = kwargs.get('bins', [[]])
    dimensions = kwargs.get('dimensions', getattr(binsize, '__len__', lambda: 1)())

    items = sorted(items, key=key, reverse=True) # largest -> smallest

    _bad_item= None

    for item in items:
        for dim in range(0, dimensions):
            if item is _bad_item: # run out the rest of the dimensions
                continue

            size_item = key[0](item) if dimensions == 1 else key[dim](item[dim])
#
#             Older python versions (< 2.4.1);
#           size_item = (lambda k:key(k), lambda k:key(item[k]))[dimensions == 1]()
#           
            if size_item > binsize[dim]:
               yield DoesNotFitWarning(item)
               break
       else:
            for target in bins:
                if size_item <= (binsize - sum(target)):
                    target.append(item)
                    dim=float('inf')
                    break
            else:
                bins.append([item])
                continue

    for item in bins:
        yield item
