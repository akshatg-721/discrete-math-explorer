"""Comprehensive tests for the sets module.

Tests every function in sets.py with multiple test cases using
plain assert statements and the def test_X() pattern.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sets import (
    parse_set, union, intersection, difference, symmetric_difference,
    is_subset, power_set, cartesian_product, count_possible_relations
)


# ──────────────────────────────────────────────
# parse_set tests
# ──────────────────────────────────────────────
def test_parse_set_space_separated():
    """Verify parse_set handles space-separated input."""
    result = parse_set("1 2 3")
    assert result == {1, 2, 3}, f"Expected {{1, 2, 3}}, got {result}"


def test_parse_set_comma_separated():
    """Verify parse_set handles comma-separated input."""
    result = parse_set("1,2,3")
    assert result == {1, 2, 3}, f"Expected {{1, 2, 3}}, got {result}"


def test_parse_set_with_braces():
    """Verify parse_set handles curly brace notation."""
    result = parse_set("{1, 2, 3}")
    assert result == {1, 2, 3}, f"Expected {{1, 2, 3}}, got {result}"


def test_parse_set_deduplicates():
    """Verify parse_set removes duplicate elements."""
    result = parse_set("1 2 2 3 3 3")
    assert result == {1, 2, 3}, f"Expected {{1, 2, 3}}, got {result}"


def test_parse_set_strings():
    """Verify parse_set handles string elements."""
    result = parse_set("a, b, c")
    assert result == {"a", "b", "c"}, f"Expected {{'a', 'b', 'c'}}, got {result}"


def test_parse_set_empty():
    """Verify parse_set handles empty input."""
    result = parse_set("")
    assert result == set(), f"Expected empty set, got {result}"


# ──────────────────────────────────────────────
# union tests
# ──────────────────────────────────────────────
def test_union_basic():
    """Verify union returns all unique elements from both sets."""
    assert union({1, 2}, {2, 3}) == {1, 2, 3}


def test_union_disjoint():
    """Verify union of disjoint sets is their full combination."""
    assert union({1, 2}, {3, 4}) == {1, 2, 3, 4}


def test_union_identical():
    """Verify union of identical sets is the same set."""
    assert union({1, 2, 3}, {1, 2, 3}) == {1, 2, 3}


def test_union_empty():
    """Verify union with empty set returns the other set."""
    assert union({1, 2}, set()) == {1, 2}
    assert union(set(), {3, 4}) == {3, 4}


# ──────────────────────────────────────────────
# intersection tests
# ──────────────────────────────────────────────
def test_intersection_basic():
    """Verify intersection returns only shared elements."""
    assert intersection({1, 2}, {2, 3}) == {2}


def test_intersection_disjoint():
    """Verify intersection of disjoint sets is empty."""
    assert intersection({1, 2}, {3, 4}) == set()


def test_intersection_identical():
    """Verify intersection of identical sets is the same set."""
    assert intersection({1, 2, 3}, {1, 2, 3}) == {1, 2, 3}


# ──────────────────────────────────────────────
# difference tests
# ──────────────────────────────────────────────
def test_difference_basic():
    """Verify difference computes directional set subtraction."""
    assert difference({1, 2, 3}, {2, 3, 4}) == {1}


def test_difference_no_overlap():
    """Verify difference with no overlap returns the full first set."""
    assert difference({1, 2}, {3, 4}) == {1, 2}


def test_difference_subset():
    """Verify difference when A is a subset of B returns empty."""
    assert difference({1, 2}, {1, 2, 3}) == set()


# ──────────────────────────────────────────────
# symmetric_difference tests
# ──────────────────────────────────────────────
def test_symmetric_difference_basic():
    """Verify symmetric difference excludes overlaps and keeps non-common."""
    assert symmetric_difference({1, 2, 3}, {2, 3, 4}) == {1, 4}


def test_symmetric_difference_disjoint():
    """Verify symmetric difference of disjoint sets is their union."""
    assert symmetric_difference({1, 2}, {3, 4}) == {1, 2, 3, 4}


def test_symmetric_difference_identical():
    """Verify symmetric difference of identical sets is empty."""
    assert symmetric_difference({1, 2}, {1, 2}) == set()


# ──────────────────────────────────────────────
# is_subset tests
# ──────────────────────────────────────────────
def test_is_subset_true():
    """Verify subset containment checks for true case."""
    assert is_subset({1, 2}, {1, 2, 3}) is True


def test_is_subset_false():
    """Verify subset check returns False when A is not a subset of B."""
    assert is_subset({1, 4}, {1, 2, 3}) is False


def test_is_subset_equal():
    """Verify equal sets are subsets of each other."""
    assert is_subset({1, 2, 3}, {1, 2, 3}) is True


def test_is_subset_empty():
    """Verify empty set is a subset of any set."""
    assert is_subset(set(), {1, 2, 3}) is True


# ──────────────────────────────────────────────
# power_set tests
# ──────────────────────────────────────────────
def test_power_set_count():
    """Verify power set has 2^n elements."""
    assert len(power_set({1, 2, 3})) == 8  # 2^3 = 8


def test_power_set_count_small():
    """Verify power set of 2 elements has 4 subsets."""
    assert len(power_set({1, 2})) == 4  # 2^2 = 4


def test_power_set_contains_empty():
    """Verify power set contains the empty set."""
    ps = power_set({1, 2, 3})
    assert frozenset() in ps


def test_power_set_contains_full():
    """Verify power set contains the full set."""
    ps = power_set({1, 2, 3})
    assert frozenset({1, 2, 3}) in ps


def test_power_set_empty_input():
    """Verify power set of empty set is {∅}."""
    ps = power_set(set())
    assert len(ps) == 1
    assert ps == [frozenset()]


# ──────────────────────────────────────────────
# cartesian_product tests
# ──────────────────────────────────────────────
def test_cartesian_product_basic():
    """Verify Cartesian product ordered pair generation."""
    result = cartesian_product({1, 2}, {3, 4})
    assert len(result) == 4  # 2 × 2
    # Check that all expected pairs are present
    result_set = set(result)
    assert (1, 3) in result_set
    assert (1, 4) in result_set
    assert (2, 3) in result_set
    assert (2, 4) in result_set


def test_cartesian_product_count():
    """Verify |A × B| = |A| × |B|."""
    A = {1, 2, 3}
    B = {"a", "b"}
    result = cartesian_product(A, B)
    assert len(result) == len(A) * len(B)  # 3 × 2 = 6


def test_cartesian_product_single():
    """Verify Cartesian product with single-element sets."""
    result = cartesian_product({1}, {2})
    assert len(result) == 1
    assert result[0] == (1, 2)


# ──────────────────────────────────────────────
# count_possible_relations tests
# ──────────────────────────────────────────────
def test_count_possible_relations_basic():
    """Verify counting formula 2^(|A|*|B|)."""
    assert count_possible_relations({1, 2}, {1, 2}) == 16  # 2^(2*2) = 16


def test_count_possible_relations_different_sizes():
    """Verify counting with different-sized sets."""
    assert count_possible_relations({1, 2, 3}, {1, 2}) == 64  # 2^(3*2) = 64


def test_count_possible_relations_single():
    """Verify counting with single-element sets."""
    assert count_possible_relations({1}, {1}) == 2  # 2^(1*1) = 2
