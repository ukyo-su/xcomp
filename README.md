# xcomp
Extended comprehension, inspired by Racket's for-syntax.

## Installation

```bash
pip install git+git://github.com/ukyo-su/xcomp@master
```

## comp(collector)

```python
from xcomp import comp

@comp(list)
def a():
    for i in range(5):
        yield i

# a == [0, 1, 2, 3, 4]

@comp(list)
def fizz_buzz():
    for i in range(30):
        if i % 15 == 0:
            yield "Fizz Buzz"
        elif i % 3 == 0:
            yield "Fizz"
        elif i % 5 == 0:
            yield "Buzz"
        else:
            yield i
```

## multi_comp(*collectors)

```python
from xcomp import multi_comp

data = [(0, 1), (2, 3)]

@multi_comp(list, list)
def a():
    for i, j in data:
        yield i, j

a_i, a_j = a

# a_i == [0, 2]
# a_j == [1, 3]
```

## reduce_comp(init, for_=None, for_nest=(), result=lambda x: x)

inspired by Racket's for/fold.

```python
from xcomp import reduce_comp, BreakReduce, ContinueReduce

@reduce_comp(0, for_=range(5))
def a(sum_, i):
    return sum_ + i

# a == 10

@reduce_comp([], for_nest=(range(3), range(2)))
def a(acc, i, j):
    return [*acc, (i, j)]

# a == [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1)]

@reduce_comp([], for_=range(5),
             result=lambda x: list(reversed(x)))
def a(acc, i):
    return [*acc, i]

# a == [4, 3, 2, 1, 0]

@reduce_comp(0, for_=range(100))
def a(acc, i):
    if i > 5:
        raise BreakReduce
    return acc + 1

# a == 6

@reduce_comp(0, for_=range(10))
def a(acc, i):
    if i < 5:
        raise ContinueReduce
    return acc + i

# a == 35
```

## multi_reduce_comp(*inits, for_=None, for_nest=(), result=lambda *args: args)

`reduce_comp` for multiple accumulators.

```python
from xcomp import multi_reduce_comp

@multi_reduce_comp(0, [],
                   for_=range(5))
def a(sum_, rev_list, i):
    return sum_ + i, [i, *rev_list]

a_sum, a_rev_list = a

# a_sum == 10
# a_rev_list == [4, 3, 2, 1, 0]

@multi_reduce_comp([], set(),
                   for_=[0, 1, 1, 2, 3, 4, 4, 4],
                   result=lambda acc, seen: list(reversed(acc)))
def a(acc, seen, i):
    if i in seen:
        return acc, seen
    else:
        return [i, *acc], {*seen, i}

# a == [0, 1, 2, 3, 4]
```

## delay_arg(func, *args, **kwargs)

`delay_arg(f, *args, **kwargs)(a)` means `f(a, *args, **kwargs)`

```python
from xcomp import delay_arg

@list
@delay_arg(map, range(5))
def a(i):
    return i * 2

# a == [0, 2, 4, 6, 8]
```
