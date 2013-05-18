#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import *

def pack(*items, **kwargs):
    """ Next-Fit

    This is perhaps the simplest packing heuristic; it simply packs items in
    the next available bin."""

    key = kwargs.get('key', lambda x:x)
    binsize = kwargs.get('binsize', 800)
    bins = kwargs.get('bins', [[]])

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
