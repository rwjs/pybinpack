#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

class DoesNotFitWarning(Warning):
    pass

class TooFewDimensions(Warning):
    pass

class GoTo(Warning):
    pass

class PersistentGenerator(object):
    """Generic generator which does not die after raising `StopIteration`.

    Useful for ensuring online packers are polymorphic with offline packers
     (in a syntactically convenient manner).
    """

    def __init__(self, *items, **kwargs):

        self.key = kwargs.get('key', lambda x:x)
        self.binsize = kwargs.get('binsize', 800)
        self.bins = kwargs.get('bins', [[]])
        self.unpacked_items=list(items)

    def __iter__(self):
        return self

    def next(self):
        self.bins.sort(self.key)
        if self.bins:
            return self.bins.pop(0)
        else:
            raise StopIteration

    def __call__(self, *items):
        self.bins += items
        return self

