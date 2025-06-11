from unittest.mock import patch

import pytest

from script import Limits, PackageSorter, PackageType


@pytest.mark.parametrize(
    "package,expected",
    [
        (
            {"width": "10", "height": "20", "length": "30", "mass": "5"},
            {"width": 10.0, "height": 20.0, "length": 30.0, "mass": 5.0},
        ),
        (
            {"width": 1, "height": 1, "length": 1, "mass": 1},
            {"width": 1.0, "height": 1.0, "length": 1.0, "mass": 1.0},
        ),
    ],
)
def test_validate_units_valid(package, expected):
    sorter = PackageSorter()
    result = sorter._validate_units(package)
    assert result == expected


@pytest.mark.parametrize(
    "package",
    [
        {"width": "0", "height": "10", "length": "10", "mass": "1"},
        {"width": "10", "height": "-1", "length": "10", "mass": "1"},
        {"width": None, "height": "10", "length": "10", "mass": "1"},
        {"width": "abc", "height": "10", "length": "10", "mass": "1"},
    ],
)
def test_validate_units_invalid(package):
    sorter = PackageSorter()
    with pytest.raises(ValueError):
        sorter._validate_units(package)


@pytest.mark.parametrize(
    "package,expected",
    [
        ({"width": 200, "height": 200, "length": 200}, True),
        ({"width": 200, "height": 50, "length": 50}, True),
        ({"width": 10, "height": 10, "length": 10}, False),
        ({"width": 150, "height": 10, "length": 10}, True),
        ({"width": 10, "height": 150, "length": 10}, True),
        ({"width": 10, "height": 10, "length": 150}, True),
    ],
)
def test_is_bulky(package, expected):
    sorter = PackageSorter()
    result = sorter._is_bulky(package)
    assert result == expected


@pytest.mark.parametrize(
    "csv_data,expected",
    [
        # STANDARD
        (
            [{"width": "10", "height": "10", "length": "10", "mass": "10"}],
            {
                "standard": {"total": 1, "percentage": "100.00%"},
                "rejected": {"total": 0, "percentage": "0.00%"},
                "special": {"total": 0, "percentage": "0.00%"},
            },
        ),
        # SPECIAL (bulky)
        (
            [{"width": "200", "height": "10", "length": "10", "mass": "10"}],
            {
                "standard": {"total": 0, "percentage": "0.00%"},
                "rejected": {"total": 0, "percentage": "0.00%"},
                "special": {"total": 1, "percentage": "100.00%"},
            },
        ),
        # SPECIAL (heavy)
        (
            [{"width": "10", "height": "10", "length": "10", "mass": "25"}],
            {
                "standard": {"total": 0, "percentage": "0.00%"},
                "rejected": {"total": 0, "percentage": "0.00%"},
                "special": {"total": 1, "percentage": "100.00%"},
            },
        ),
        # REJECTED (bulky e heavy)
        (
            [{"width": "200", "height": "200", "length": "200", "mass": "25"}],
            {
                "standard": {"total": 0, "percentage": "0.00%"},
                "rejected": {"total": 1, "percentage": "100.00%"},
                "special": {"total": 0, "percentage": "0.00%"},
            },
        ),
        # Misto
        (
            [
                {"width": "10", "height": "10", "length": "10", "mass": "10"},
                {"width": "200", "height": "10", "length": "10", "mass": "10"},
                {"width": "10", "height": "10", "length": "10", "mass": "25"},
                {"width": "200", "height": "200", "length": "200", "mass": "25"},
            ],
            {
                "standard": {"total": 1, "percentage": "25.00%"},
                "rejected": {"total": 1, "percentage": "25.00%"},
                "special": {"total": 2, "percentage": "50.00%"},
            },
        ),
    ],
)
def test_sort(csv_data, expected):
    with patch.object(PackageSorter, "_ingest_csv", return_value=csv_data):
        sorter = PackageSorter()
        result = sorter.sort()
        for key in expected:
            assert result[key]["total"] == expected[key]["total"]
            assert result[key]["percentage"] == expected[key]["percentage"]


def test_limits():
    assert Limits.BULKY_LIMIT.value == 1000000
    assert Limits.WIDTH_LIMIT.value == 150
    assert Limits.HEIGHT_LIMIT.value == 150
    assert Limits.LENGTH_LIMIT.value == 150
    assert Limits.HEAVY_LIMIT.value == 20


def test_package_type():
    assert PackageType.STANDARD.value == "STANDARD"
    assert PackageType.REJECTED.value == "REJECTED"
    assert PackageType.SPECIAL.value == "SPECIAL"
