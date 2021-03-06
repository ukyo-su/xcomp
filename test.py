import pytest

from xcomp import (comp, multi_comp, delay_arg, multi_reduce_comp, reduce_comp,
                   BreakReduce, ContinueReduce)


def test_list_comp():
    @comp(list)
    def actual():
        for i in range(5):
            yield i

    assert actual == list(range(5))


def test_dict_comp():
    @comp(dict)
    def actual():
        for i in range(5):
            yield str(i), i

    expected = {str(i): i for i in range(5)}

    assert actual == expected


def test_sum_comp():
    @comp(sum)
    def actual():
        for i in range(5):
            yield i

    assert actual == sum(range(5))


def test_sum_list_comp():
    @multi_comp(sum, list)
    def actual():
        for i in range(5):
            yield i, i * 2

    actual_sum, actual_list = actual
    assert actual_sum == sum(range(5))
    assert actual_list == [i * 2 for i in range(5)]


def test_sum_reduce_comp():
    @reduce_comp(0, for_=range(5))
    def actual(sum_, i):
        return sum_ + i

    assert actual == sum(range(5))


def test_result_reduce_comp():
    @reduce_comp(0, for_=range(5),
                 result=lambda x: x / 2)
    def actual(sum_, i):
        return sum_ + i

    assert actual == 5


def test_sum_rev_list_multi_reduce_comp():
    @multi_reduce_comp(0, [],
                       for_=range(5))
    def actual(sum_, rev_list, i):
        return sum_ + i, [i, *rev_list]

    actual_sum, actual_rev_list = actual

    assert actual_sum == sum(range(5))
    assert actual_rev_list == list(reversed(range(5)))


def test_unique_multi_reduce_comp():
    @multi_reduce_comp([], set(),
                       for_=[0, 1, 1, 2, 3, 4, 4, 4],
                       result=lambda acc, seen: list(reversed(acc)))
    def actual(acc, seen, i):
        if i in seen:
            return acc, seen
        else:
            return [i, *acc], {*seen, i}

    assert actual == [0, 1, 2, 3, 4]


def test_break_reduce_comp():
    @reduce_comp(0, for_=range(100))
    def actual(acc, i):
        if i > 5:
            raise BreakReduce
        return acc + 1

    assert actual == 6


def test_continue_reduce_comp():
    @reduce_comp(0, for_=range(10))
    def actual(acc, i):
        if i < 5:
            raise ContinueReduce
        return acc + i

    assert actual == sum(range(5, 10))


def test_nest_reduce_comp():
    @reduce_comp([], for_nest=(range(3), range(2),))
    def actual(acc, i, j):
        return [*acc, (i, j)]

    assert actual == [(i, j) for i in range(3) for j in range(2)]


def test_empty_reduce_comp():
    @reduce_comp(0, for_=[])
    def actual(sum_, i):
        return sum_ + i

    assert actual == 0


def test_empty_multi_reduce_comp():
    @multi_reduce_comp(0, [], for_=[])
    def actual(sum_, acc, i):
        return sum_ + i, [*acc, i]

    actual_sum, actual_acc = actual

    assert actual_sum == 0
    assert actual_acc == []


def test_no_for_reduce_comp():
    with pytest.raises(TypeError):
        @reduce_comp(0)
        def actual(sum_):
            return sum_


def test_no_for_multi_reduce_comp():
    with pytest.raises(TypeError):
        @multi_reduce_comp(0, [])
        def actual(sum_, acc):
            return sum_, acc


def test_map_delay_arg():
    @delay_arg(map, range(5))
    def actual(i):
        return i * 2

    assert list(actual) == list(map(lambda i: i * 2, range(5)))
