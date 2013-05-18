pybinpack
=========

A collection of bin-packing heuristics for Python.

Multi-dimension Bin-Packing Logic
=========

 * Multi-dimension items can be supplied by wrapping each dimension in an iterable (eg, list, tuple). This is processed as a parallel array, where the index of the wrapper corresponds to the dimension index.
 * Multi-dimension binsizes can also be supplied wrapped in an iterable (eg, list, tuple). If a `dimension` keyword argument is supplied, the length of the binsize iterable must match this.
 * Multiple keys can also be supplied wrapped in an iterable. As with binsizes, there must be as many keys as dimensions *if* multiple keys are supplied, however, if a single key is supplied (ie, not wrapped in an iterable), that key will be used for all dimensions.
 * The number of dimensions in the bin packing instance is determined by;
    1. The 'dimensions' keyword argument (kwarg), or
    2. By the length of the length of 'binsize' if no kwarg supplied (specifically binsize.__len__), or 
    3. Defaulting to 1 if binsize is not iterable and no kwarg supplied.
 * All multi-dimension iterable-wrapping logic is only required if the number of dimensions exceeds one. If it does not; items, keys and binsizes will be examined as they are.
 * Items with too few dimensions **yields** `TooFewDimensions`. Excess dimensions are simply ignored.

TODO
====

 * Add more heuristics.
 * Write optimised solutions (both space and time).
 * Include more documentation.
 * Add support for multi-dimensional packing (will require a lot of work)
 * Add online packing heuristics
 * Consider adding support for variable bin sizes (this may require a custom type with a 'size' attribute).
 * Ship the test unit(s) in main.py elsewhere.
