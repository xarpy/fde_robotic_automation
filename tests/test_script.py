from pytest import mark

from script import Limits, PackageSorter, PackageType


@mark.parametrize(
    "width, height, length, mass, expected",
    [(200, 200, 200, 200, True), (200, 50, 50, 50, True), (10, 10, 10, 10, False)],
)
def test_is_bulky(width, height, length, mass, expected):
    """function is_bulk unit test"""
    instance = PackageSorter(
        width,
        height,
        length,
        mass,
    )
    result = instance._is_bulky()
    assert result == expected


@mark.parametrize(
    "width, height, length, mass, expected",
    [
        (10, 10, 10, 10, PackageType.STANDARD.value),
        (200, 50, 50, 10, PackageType.SPECIAL.value),
        (10, 10, 10, 25, PackageType.SPECIAL.value),
        (200, 200, 200, 25, PackageType.REJECTED.value),
    ],
)
def test_sort_package(width, height, length, mass, expected):
    """function sort unit test"""
    instance = PackageSorter(
        width,
        height,
        length,
        mass,
    )
    result = instance.sort()
    assert result == expected


@mark.parametrize("bulky, width, height, length, heavy", [(1000000, 150, 150, 150, 20)])
def test_limits(bulky, width, height, length, heavy):
    """function Limits class unit test"""
    assert Limits.BULKY_LIMIT.value == bulky
    assert Limits.WIDTH_LIMIT.value == width
    assert Limits.HEIGHT_LIMIT.value == height
    assert Limits.LENGTH_LIMIT.value == length
    assert Limits.HEAVY_LIMIT.value == heavy
    assert Limits.HEAVY_LIMIT.value == heavy
