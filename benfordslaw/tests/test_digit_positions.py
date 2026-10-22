"""Regression coverage for empirical extraction, independent of the null model."""

import numpy as np
import pandas as pd
import pytest
from decimal import Decimal
from fractions import Fraction

from benfordslaw import benfordslaw
from benfordslaw.benfordslaw import _count_digit, _count_first_two_digits


TRAILING_ZEROS = np.array([10, 20, 100, 120, 1000, 1010, 10000, 56780])


def test_last_digit_zero_is_counted_in_public_results():
    results = benfordslaw(pos=-1, method="mad", verbose=0).fit(np.arange(10, 20))

    assert results["N"] == 10
    np.testing.assert_array_equal(results["percentage_emp"][:, 0], np.arange(10))
    np.testing.assert_array_equal(results["percentage_emp"][:, 1], np.full(10, 10.0))


@pytest.mark.parametrize(
    "position, expected",
    [
        (-1, [8, 0, 0, 0, 0, 0, 0, 0, 0, 0]),
        (-2, [3, 2, 2, 0, 0, 0, 0, 0, 1, 0]),
        (-3, [3, 2, 0, 0, 0, 0, 0, 1, 0, 0]),
        (-4, [1, 2, 0, 0, 0, 0, 1, 0, 0, 0]),
        (-5, [0, 1, 0, 0, 0, 1, 0, 0, 0, 0]),
    ],
)
def test_trailing_zeroes_preserve_right_digit_positions(position, expected):
    counts, percentages, total, digits = _count_digit(TRAILING_ZEROS, position, range(10))

    np.testing.assert_array_equal(counts, expected)
    assert total == sum(expected)
    assert digits == list(range(10))
    np.testing.assert_allclose(percentages, np.array(expected) / total * 100)


@pytest.mark.parametrize("position", [-1, -2, -3, -4, -5])
def test_integer_valued_floats_match_integer_input(position):
    expected = _count_digit(TRAILING_ZEROS, position, range(10))
    observed = _count_digit(TRAILING_ZEROS.astype(float), position, range(10))

    np.testing.assert_array_equal(observed[0], expected[0])
    assert observed[2] == expected[2]


@pytest.mark.parametrize("position", [-6, -9])
def test_short_numbers_do_not_gain_zero_padding(position):
    counts, percentages, total, _ = _count_digit(TRAILING_ZEROS, position, range(10))

    np.testing.assert_array_equal(counts, np.zeros(10))
    assert total == 0
    assert np.all(np.isnan(percentages))


def test_last_digit_ignores_nonpositive_and_nonfinite_values():
    values = np.array([0, -10, np.nan, np.inf, -np.inf, 10, 21, 32], dtype=float)
    counts, _, total, _ = _count_digit(values, -1, range(10))

    np.testing.assert_array_equal(counts, [1, 1, 1, 0, 0, 0, 0, 0, 0, 0])
    assert total == 3


@pytest.mark.parametrize("values", [np.array([]), np.array([0, -1, np.nan, np.inf])])
def test_last_digit_without_valid_values_has_no_observations(values):
    counts, percentages, total, _ = _count_digit(values, -1, range(10))

    np.testing.assert_array_equal(counts, np.zeros(10))
    assert total == 0
    assert np.all(np.isnan(percentages))


def test_nonnumeric_values_are_not_silently_counted():
    with pytest.raises((TypeError, ValueError)):
        _count_digit(np.array(["not a number"]), -1, range(10))


@pytest.mark.parametrize('value', [12.5, 0.5, Decimal('0.5'), Fraction(1, 2)])
def test_fractional_values_have_no_implicit_last_integer_digit(value):
    with pytest.raises(ValueError, match="integer-valued"):
        _count_digit(np.array([value], dtype=object), -1, range(10))


def test_numeric_object_array_retains_preexisting_supported_input():
    counts, _, total, _ = _count_digit(np.array([12, 23], dtype=object), -1, range(10))
    np.testing.assert_array_equal(counts, [0, 0, 1, 1, 0, 0, 0, 0, 0, 0])
    assert total == 2


@pytest.mark.parametrize('include_missing', [False, True])
def test_public_fit_accepts_nullable_integer_dataframe_and_skips_pd_na(include_missing):
    rows = [12, 23, 10] + ([pd.NA] if include_missing else [])
    values = pd.DataFrame({'value': pd.array(rows, dtype='Int64')})
    result = benfordslaw(pos=-1, method='mad', verbose=0).fit(values)
    assert result['N'] == 3
    np.testing.assert_allclose(result['percentage_emp'][:, 1], np.array([1, 0, 1, 1, 0, 0, 0, 0, 0, 0]) / 3 * 100)


@pytest.mark.parametrize('position, expected_digit', [(-1, 2), (-2, 4)])
def test_arbitrarily_large_integer_digits_do_not_require_float_or_string_conversion(position, expected_digit):
    value = 10 ** 5000 + 42
    counts, _, total, _ = _count_digit(np.array([value], dtype=object), position, range(10))
    assert counts[expected_digit] == 1
    assert total == 1


def test_mixed_scalar_types_do_not_round_large_integer_inputs():
    values = [2 ** 64 + 1, 20.0, Decimal('32'), Fraction(43, 1), pd.NA, None]
    counts, _, total, _ = _count_digit(values, -1, range(10))
    np.testing.assert_array_equal(counts, [1, 0, 1, 1, 0, 0, 0, 1, 0, 0])
    assert total == 4


@pytest.mark.parametrize(
    "position, digit_range, expected",
    [
        (1, range(1, 10), [6, 1, 0, 0, 1, 0, 0, 0, 0]),
        (2, range(10), [6, 0, 1, 0, 0, 0, 1, 0, 0, 0]),
        (3, range(10), [4, 1, 0, 0, 0, 0, 0, 1, 0, 0]),
    ],
)
def test_leading_digit_counts_are_preserved(position, digit_range, expected):
    counts, _, total, _ = _count_digit(TRAILING_ZEROS, position, digit_range)

    np.testing.assert_array_equal(counts, expected)
    assert total == sum(expected)


def test_first_two_digit_counts_are_preserved():
    counts, _, total, digits = _count_first_two_digits(TRAILING_ZEROS)
    expected = np.zeros(90)
    expected[[0, 2, 10, 46]] = [5, 1, 1, 1]

    np.testing.assert_array_equal(counts, expected)
    assert total == 8
    assert digits == list(range(10, 100))


def test_fix_does_not_change_last_digit_reference_distribution():
    model = benfordslaw(pos=-1, method="mad", verbose=0)
    np.testing.assert_array_equal(model.leading_digits, np.full(10, 10.0))
