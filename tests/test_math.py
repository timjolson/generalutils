import pytest
from generalutils.math import constrain, rescale, deadband, tuple_distance


def test_constrain():
    # within limits
    assert constrain(0, 0, 10) == 0
    assert constrain(8, 0, 10) == 8
    assert constrain(10, 0, 10) == 10

    # outside limits
    assert constrain(11, 0, 10) == 10
    assert constrain(-1, 0, 10) == 0


def test_rescale():
    il, ih = 0, 100
    ol, oh = 100, 200

    # within range
    assert rescale(10, il, ih, ol, oh) == 110
    assert rescale(0, il, ih, ol, oh) == 100
    assert rescale(100, il, ih, ol, oh) == 200
    assert rescale(50, il, ih, ol, oh) == 150
    assert rescale(90, il, ih, ol, oh) == 190

    # change scale as well
    ol, oh = 1000, 2000
    assert rescale(10, il, ih, ol, oh) == 1100
    assert rescale(0, il, ih, ol, oh) == 1000
    assert rescale(100, il, ih, ol, oh) == 2000
    assert rescale(50, il, ih, ol, oh) == 1500
    assert rescale(90, il, ih, ol, oh) == 1900


    ## Test values outside range

    # constrain to limits
    assert rescale(110, il, ih, ol, oh, 'constrain') == 2000
    assert rescale(-10, il, ih, ol, oh, 'constrain') == 1000

    # ignore limits, accept value
    assert rescale(110, il, ih, ol, oh, 'ignore') == 2100
    assert rescale(-10, il, ih, ol, oh, 'ignore') == 900

    # set to average value
    assert rescale(110, il, ih, ol, oh, 'mid') == 1500
    assert rescale(-10, il, ih, ol, oh, 'mid') == 1500

    # set to provided value
    junk = object()
    assert rescale(110, il, ih, ol, oh, junk) == junk
    assert rescale(-10, il, ih, ol, oh, junk) == junk

    # set to provided value
    assert rescale(110, il, ih, ol, oh, None) is None
    assert rescale(-10, il, ih, ol, oh, None) is None

    # raise ValueError
    with pytest.raises(ValueError):
        rescale(110, il, ih, ol, oh, outside='raise')
    with pytest.raises(ValueError):
        rescale(-10, il, ih, ol, oh, outside='raise')


def test_deadband():
    # standard usage
    # provide magnitude
    assert deadband(0, 10) == 0
    assert deadband(9, 10) == 0
    assert deadband(10, 10) == 10
    assert deadband(11, 10) == 11
    assert deadband(-9, 10) == 0
    assert deadband(-10, 10) == -10
    assert deadband(-11, 10) == -11

    # magnitude, smooth
    assert deadband(0, 10, smooth=True) == 0
    assert deadband(9, 10, smooth=True) == 0
    assert deadband(10, 10, smooth=True) == 0
    assert deadband(11, 10, smooth=True) == 1
    assert deadband(-9, 10, smooth=True) == 0
    assert deadband(-10, 10, smooth=True) == 0
    assert deadband(-11, 10, smooth=True) == -1

    # offset center
    assert deadband(5, 10, 5) == 5
    assert deadband(14, 10, 5) == 5
    assert deadband(15, 10, 5) == 15
    assert deadband(16, 10, 5) == 16
    assert deadband(-4, 10, 5) == 5
    assert deadband(-5, 10, 5) == -5
    assert deadband(-6, 10, 5) == -6

    # offset center and different deadbands
    assert deadband(5, 10, center=5, lower_deadband=2) == 5
    assert deadband(15, 10, center=5, lower_deadband=2) == 15
    assert deadband(16, 10, center=5, lower_deadband=2) == 16
    assert deadband(4, 10, center=5, lower_deadband=2) == 5
    assert deadband(2, 10, center=5, lower_deadband=2) == 2

    # different deadbands, smooth
    assert deadband(5, deadband=10, lower_deadband=2, smooth=True) == 0
    assert deadband(10, deadband=10, lower_deadband=2, smooth=True) == 0
    assert deadband(15, deadband=10, lower_deadband=2, smooth=True) == 5
    assert deadband(-2, deadband=10, lower_deadband=2, smooth=True) == 0
    assert deadband(-6, deadband=10, lower_deadband=2, smooth=True) == -4

    # different deadbands, smooth, offset center
    assert deadband(5, deadband=10, center=5, lower_deadband=2, smooth=True) == 5
    assert deadband(15, deadband=10, center=5, lower_deadband=2, smooth=True) == 5
    assert deadband(16, deadband=10, center=5, lower_deadband=2, smooth=True) == 6
    assert deadband(3, deadband=10, center=5, lower_deadband=2, smooth=True) == 5
    assert deadband(2, deadband=10, center=5, lower_deadband=2, smooth=True) == 4
    assert deadband(1, deadband=10, center=5, lower_deadband=2, smooth=True) == 3


def test_tuple_distance():
    from math import sqrt
    assert tuple_distance((0, ), (1, )) == 1
    assert tuple_distance((0, 0), (1, 1)) == sqrt(2)

    assert tuple_distance((2, 2), (1, 1)) == sqrt(2)
    assert tuple_distance((2, 0), (1, 1)) == sqrt(2)
    assert tuple_distance((2, 2), (-2, 2)) == 4
    assert tuple_distance((2, 2), (-2, -2)) == 4 * sqrt(2)

    assert tuple_distance((2, 2, 2), (-2, 2, 2)) == 4

    with pytest.raises(TypeError):
        tuple_distance((0, 1), (1, 2, 3))
    with pytest.raises(TypeError):
        tuple_distance((0, 1, 2), (1, 2))

