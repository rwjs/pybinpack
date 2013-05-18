#!/usr/bin/env python
# -*- coding: utf-8 -*-

from common import *

def pack(*items, **kwargs):
    """ Almost Worst-Fit. Offline, 1-dimension.

    The items are packed into the second-emptiest bin. Some sources indicate
    that this heuristic is provably better than Worst Fit, but I have thus far
    been unable to locate anything definitive."""

    key = kwargs.get('key', (lambda x:x, ))
    binsize = kwargs.get('binsize', 800)
    bins = kwargs.get('bins', [[]])
    dimensions = kwargs.get('dimensions', 1)

    bins.sort(key=lambda x:sum(x))

    for item in items:
        for dim in range(0, dimensions):
            size_item = key(item)
            if size_item > binsize:
                yield DoesNotFitWarning(item)
                continue
            try:
                assert binsize - sum(bins[1]) >= size_item
                # IndexError if no bins[1], AssertionError if not fit.
                bins[1].append(item)
            except (AssertionError, IndexError):
                if bins and binsize - sum(bins[0]) >= size_item:
                # At least one bin exists and the item fits in it
                    bins[0].append(item)
                else:
                # Create new bin
                    bins.append([item])
            bins.sort(key=lambda x:sum(x)) 
            # TimSort is quite efficient for partially sorted lists..
        for b in bins:
            yield b
