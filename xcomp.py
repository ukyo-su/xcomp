from contextlib import contextmanager
from itertools import product


def comp(collector):
    def decorator(func):
        return collector(func())
    return decorator


def multi_comp(*collectors):
    def decorator(func):
        return tuple(c(v) for c, v in zip(collectors, zip(*func())))
    return decorator


class BreakReduce(Exception):
    pass


class ContinueReduce(Exception):
    pass


@contextmanager
def ignore(exception):
    try:
        yield
    except exception:
        pass


def multi_reduce_comp(*inits, for_=None, for_nest=None,
                      result=lambda *args: args):
    if for_ is for_nest is None:
        raise TypeError("an Iterable should be specified")

    if for_ is not None:
        for_nest = (for_,)

    def decorator(func):
        accums = inits
        with ignore(BreakReduce):
            for vs in product(*for_nest):
                with ignore(ContinueReduce):
                    accums = func(*accums, *vs)
        return result(*accums)
    return decorator


def reduce_comp(init, for_=None, for_nest=None,
                result=lambda x: x):
    def multi_result(*args):
        return result(args[0]),

    def decorator(func):
        def multi(*args):
            return func(*args),
        return multi_reduce_comp(init, for_nest=for_nest,
                                 for_=for_, result=multi_result)(multi)[0]
    return decorator


def delay_arg(func, *args, **kwargs):
    def delayed(arg):
        return func(arg, *args, **kwargs)
    return delayed
