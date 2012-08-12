#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __init__ import *

def pack(*items, **kwargs):
    """ Next-Fit Decreasing

    Next-Fit is perhaps the simplest packing heuristic; it simply packs items in
    the next available bin. This algorithm differs only from Next-Fit
    Decreasing in having a 'sort'; that is, the items are pre-sorted (largest
    to smallest)."""

    key = kwargs.get('key', lambda x:x)
    binsize = kwargs.get('binsize', 800)
    bins = kwargs.get('bins', [[]])

    items = sorted(items, key=key, reverse=True) # largest -> smallest

    for item in items:
        size_item = key(item)
        if size_item > binsize:
            yield DoesNotFitWarning(item)
            continue
        for target in bins:
            if size_item <= (binsize - sum(target)):
                target.append(item)
                break
        else:
            bins.append([item])
    for item in bins:
        yield item
