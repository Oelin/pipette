# pipette, a simple functional pipelining framework.


import functools


def map(function):
    
    def ret(iterable):
        
        for value in iterable:
            try:
                yield function(value) or value
            except: pass
    
    return ret


def filter(predicate):
    
    def ret(iterable):
        for value in iterable:
            if predicate(value): yield value
    
    return ret


def reduce(function):
    
    def ret(iterable):
        result = next(iterable)
        
        for value in iterable:
            result = function(result, value)
        
        yield result
    
    return ret


def serialise(iterator):
    
    def ret(iterable):
        
        for value in iterable:
            for nested in iterator(value):
                yield nested
    
    return ret


def collect(function):
    
    def ret(iterable):
        yield function(list(iterable))
    
    return ret


def pipe(*iterators):
    
    def ret(iterable):
        return functools.reduce(lambda a, b: b(a), iterators, iterable)
    
    return ret


class Pipe:
    
    def __init__(self):
        self.stages = []
    
    def then(self, *stages):
        self.stages += stages
        
    def __call__(self, iterable):
        return pipe(*self.stages)(iterable)
