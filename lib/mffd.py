#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from common import *

if __name__ == "__main__":
    from ..__init__ import *
import ffd

def pack(*items, **kwargs):
    """ Modified First-Fit Decreasing bin-packing heuristic.

    Accepted Keyword Arguments:

     key : A callable which takes one argument and returns a value which can
            be __cmp__'d against the supplied binsize. This is (intentionally)
            identical to the sort() builtin's key= argument). Defaults to
            lambda x:x
     binsize: The capacity of a bin. Defaults to 800.
     bins: Any already-sorted bins. Default to nothing (ie, [[]]).

    According to Wikipedia;

    "MFFD[5] (a variant of FFD) uses no more than 71/60 OPT + 1 bins[6] 
    (i.e. bounded by about 1.18×opt, compared to about 1.22×opt for FFD)."

    The following description of the MFFD algorithm can be retrieved from 
    http://hackage.haskell.org/packages/archive/Binpack/0.4/doc/html/Data-BinPath.html
    courtesy of Björn B. Brandenburg.
    
    ============================================================================
    Let lst denote the list of items to be bin-packed, let x denote the size of 
    the smallest element in lst, and let cap denote the capacity of one bin. 

    lst is split into the four sub-lists, lA, lB, lC, lD.

    lA: All items strictly larger than cap/2. 
    lB: All items of size at most cap/2 and strictly larger than cap/3. 
    lC: All items of size at most cap/3 and strictly larger than (cap - x)/5.
    lD: The rest, i.e., all items of size at most (cap - x)/5. 

    Items are placed as follows:

    1. Create a list of length lA bins. Place each item in lA into its own 
       bin (while maintaining relative item order with respect to lst). 
       Note: relevant published analysis assumes that lst is sorted in order of 
       decreasing size.
    2. Take the list of bins created in Step 1 and reverse it.
    3. Sequentially consider each bin b. If the two smallest items in lC do NOT
       fit together into b of if there a less than two items remaining in lC,
       then pack nothing into b and move on to the next bin (if any). If they do
       fit together, then find the largest item x1 in lC that would fit together
       with the smallest item in lC into b. Remove x1 from lC. Then find the 
       largest item x2, x2 != x1, in lC that will now fit into b together with 
       x1. Remove x1* from lC. Place both x1 and x2 into b and move on to the 
       next item.
    4. Reverse the list of bins again.
    5. Use the FirstFit heuristic to place all remaining items, i.e., lB, lD, 
       and any remaining items of lC.
    ============================================================================
       * (I believe he means 'Remove x2 from lC', not 'Remove x1 from lC')
    """

    #Please note; this implementation is very different to the 

    # reference/description; probably because it was targetting purely
    # functional languages (and this is a somewhat procedural approach). I have
    # made this implementation intentionally verbose, due to the relative 
    # complexity of this algorithm. I plan to optimise it, but would welcome any
    # patches (with sufficient evidence of optimality)

    # Steps 1 & 2:
    key = kwargs.get('key', lambda x:x)
    binsize = kwargs.get('binsize', 800)
    bins = kwargs.get('bins', [])
   
    items = list(items) + bins
    items = sorted(items, key=key) # smallest -> largest

    list_a = []
    list_c = []
    index_item = 0
 
    while index_item < len(items):
        size_item = key(items[index_item])
        if size_item > binsize:
            yield DoesNotFitWarning(items[index_item])
            index_item += 1
            continue

        elif size_item > binsize/2:
            list_a.append([items.pop(index_item)])
            continue

        elif (size_item <= binsize/3 and size_item > ((binsize - size_item) / 5)):
            list_c.append(items.pop(index_item))
            continue

        else:
            index_item += 1
    
    index_a = 0

    # Step 3:
    while index_a < len(list_a):
        # `while` used (over `for`), as list is being modified during iteration.
        try:
            item_a = list_a[index_a][0]
            size_a = key(item_a)

            index_c1 = 0
            item_c1 = list_c[index_c1] # may raise IndexError
            size_c1 = key(item_c1)

            index_c2 = 1
            item_c2 = list_c[index_c2] # may raise IndexError
            size_c2 = key(item_c2)
 

            if sum((size_c1, size_c2, size_a)) > binsize:
                break # These are the smallest values, as this is
                      # a sorted list. No need to `index_a += 1 ; continue`
        except IndexError:
            index_a += 1
            continue # next item_a

        # select new item_c1
        if sum((size_c1, size_c2, size_a)) <= binsize:
            for index_c1_new, item_c1_new in enumerate(list_c):
                if index_c1_new in (index_c1, index_c2):
                    continue
                size_c1_new = key(item_c1_new)
                if sum((size_c1_new, size_c2, size_a)) > binsize:
                    break
                index_c1 = index_c1_new
                size_c1 = key(list_c[index_c1])

        # select new item_c2
        if sum((size_c1, size_c2, size_a)) <= binsize:
            for index_c2_new, item_c2_new in enumerate(list_c):
                if index_c2_new in (index_c1, index_c2): 

                    continue
                size_c2_new = key(item_c2_new)
                if sum((size_c1, size_c2_new, size_a)) > binsize:
                    break
                index_c2 = index_c2_new
                size_c2 = key(list_c[index_c2])

        assert index_c1 != index_c2, "Index collision"

        # Remove the larger index first (or it _will_ break)
        if index_c1 >= index_c2:
            item_c1 = list_c.pop(index_c1)
        item_c2 = list_c.pop(index_c2)
        if index_c1 < index_c2:
            item_c1 = list_c.pop(index_c1)

        list_a[index_a] += [item_c1, item_c2]
        index_a += 1

    # Step 4:
    list_a.reverse()

    # Step 5:
    items += list_c
    items.sort(key=key, reverse=True)

    for x in ffd.pack(*items, key=key, binsize=binsize, bins=list_a):
        yield x

