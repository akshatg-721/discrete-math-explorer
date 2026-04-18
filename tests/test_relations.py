"""Comprehensive tests for the relations module.

Tests every function in relations.py with multiple test cases using
plain assert statements and the def test_X() pattern.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from relations import (
    build_relation, is_reflexive, is_symmetric, is_antisymmetric,
    is_transitive, is_equivalence_relation, count_possible_relations,
    warshall, compose, equivalence_classes
)


# ──────────────────────────────────────────────
# build_relation tests
# ──────────────────────────────────────────────
def test_build_relation_basic():
    """Verify relation creation from selected Cartesian product entries."""
    pairs = [(1, 1), (1, 2), (2, 1), (2, 2)]
    R = build_relation(pairs, [0, 3])
    assert R == {(1, 1), (2, 2)}


def test_build_relation_all():
    """Verify selecting all indices returns all pairs."""
    pairs = [(1, 2), (3, 4)]
    R = build_relation(pairs, [0, 1])
    assert R == {(1, 2), (3, 4)}


def test_build_relation_empty():
    """Verify empty selection returns empty relation."""
    pairs = [(1, 2), (3, 4)]
    R = build_relation(pairs, [])
    assert R == set()


def test_build_relation_out_of_range():
    """Verify out-of-range indices are safely ignored."""
    pairs = [(1, 2), (3, 4)]
    R = build_relation(pairs, [0, 5, 10])
    assert R == {(1, 2)}


# ──────────────────────────────────────────────
# is_reflexive tests
# ──────────────────────────────────────────────
def test_is_reflexive_true():
    """Verify reflexive relation on base set."""
    R = {(1, 1), (2, 2), (1, 2)}
    assert is_reflexive(R, {1, 2}) is True


def test_is_reflexive_false():
    """Verify non-reflexive relation detection."""
    R = {(1, 1), (1, 2)}  # Missing (2, 2)
    assert is_reflexive(R, {1, 2}) is False


def test_is_reflexive_single():
    """Verify reflexive on single-element set."""
    assert is_reflexive({(1, 1)}, {1}) is True


def test_is_reflexive_empty_set():
    """Verify reflexive on empty base set (vacuously true)."""
    assert is_reflexive(set(), set()) is True


# ──────────────────────────────────────────────
# is_symmetric tests
# ──────────────────────────────────────────────
def test_is_symmetric_true():
    """Verify symmetric relation detection."""
    R = {(1, 2), (2, 1)}
    assert is_symmetric(R) is True


def test_is_symmetric_false():
    """Verify non-symmetric relation detection."""
    R = {(1, 2)}  # Missing (2, 1)
    assert is_symmetric(R) is False


def test_is_symmetric_self_pairs():
    """Verify relation with only self-pairs is symmetric."""
    R = {(1, 1), (2, 2)}
    assert is_symmetric(R) is True


def test_is_symmetric_empty():
    """Verify empty relation is symmetric (vacuously true)."""
    assert is_symmetric(set()) is True


# ──────────────────────────────────────────────
# is_antisymmetric tests
# ──────────────────────────────────────────────
def test_is_antisymmetric_true():
    """Verify antisymmetric relation detection."""
    R = {(1, 2), (1, 1), (2, 2)}  # a ≤ b pattern
    assert is_antisymmetric(R) is True


def test_is_antisymmetric_false():
    """Verify non-antisymmetric relation detection."""
    R = {(1, 2), (2, 1)}  # Both directions with distinct elements
    assert is_antisymmetric(R) is False


def test_is_antisymmetric_self_only():
    """Verify relation with only self-pairs is antisymmetric."""
    R = {(1, 1), (2, 2), (3, 3)}
    assert is_antisymmetric(R) is True


# ──────────────────────────────────────────────
# is_transitive tests
# ──────────────────────────────────────────────
def test_is_transitive_true():
    """Verify transitive relation detection."""
    R = {(1, 2), (2, 3), (1, 3)}
    assert is_transitive(R) is True


def test_is_transitive_false():
    """Verify non-transitive relation detection."""
    R = {(1, 2), (2, 3)}  # Missing (1, 3)
    assert is_transitive(R) is False


def test_is_transitive_chain():
    """Verify longer transitive chain."""
    R = {(1, 2), (2, 3), (3, 4), (1, 3), (1, 4), (2, 4)}
    assert is_transitive(R) is True


def test_is_transitive_empty():
    """Verify empty relation is transitive (vacuously true)."""
    assert is_transitive(set()) is True


# ──────────────────────────────────────────────
# is_equivalence_relation tests
# ──────────────────────────────────────────────
def test_is_equivalence_relation_true():
    """Verify equivalence relation detection."""
    # Relation: "same parity" on {1, 2, 3, 4}
    # Equivalence classes: {1,3} and {2,4}
    A = {1, 2}
    R = {(1, 1), (2, 2), (1, 2), (2, 1)}
    assert is_equivalence_relation(R, A) is True


def test_is_equivalence_relation_false_not_reflexive():
    """Verify non-equivalence relation (missing reflexivity)."""
    A = {1, 2}
    R = {(1, 2), (2, 1)}  # Missing (1,1), (2,2)
    assert is_equivalence_relation(R, A) is False


def test_is_equivalence_relation_identity():
    """Verify identity relation is an equivalence relation."""
    A = {1, 2, 3}
    R = {(1, 1), (2, 2), (3, 3)}
    assert is_equivalence_relation(R, A) is True


# ──────────────────────────────────────────────
# count_possible_relations tests
# ──────────────────────────────────────────────
def test_count_possible_relations_basic():
    """Verify counting formula 2^(|A|*|B|)."""
    assert count_possible_relations({1, 2}, {1, 2}) == 16


def test_count_possible_relations_asymmetric():
    """Verify counting with different set sizes."""
    assert count_possible_relations({1}, {1, 2, 3}) == 8  # 2^(1*3) = 8


def test_count_possible_relations_empty():
    """Verify counting with empty set."""
    assert count_possible_relations(set(), {1, 2}) == 1  # 2^0 = 1


# ──────────────────────────────────────────────
# warshall tests
# ──────────────────────────────────────────────
def test_warshall_basic():
    """Verify transitive closure computation."""
    R = {(1, 2), (2, 3)}
    elements = [1, 2, 3]
    closure = warshall(R, elements)
    assert (1, 2) in closure
    assert (2, 3) in closure
    assert (1, 3) in closure  # Transitive: 1→2→3 implies 1→3


def test_warshall_already_transitive():
    """Verify Warshall on already transitive relation adds nothing new."""
    R = {(1, 2), (2, 3), (1, 3)}
    elements = [1, 2, 3]
    closure = warshall(R, elements)
    assert closure == R


def test_warshall_cycle():
    """Verify Warshall on a cycle produces full connectivity."""
    R = {(1, 2), (2, 3), (3, 1)}
    elements = [1, 2, 3]
    closure = warshall(R, elements)
    # In a cycle, every node can reach every other node
    for a in elements:
        for b in elements:
            assert (a, b) in closure, f"Missing ({a},{b}) in closure"


# ──────────────────────────────────────────────
# compose tests
# ──────────────────────────────────────────────
def test_compose_basic():
    """Verify relation composition."""
    R = {("A", "B"), ("B", "C")}
    S = {("B", "x"), ("C", "y")}
    result = compose(R, S)
    assert ("A", "x") in result  # A→B in R, B→x in S
    assert ("B", "y") in result  # B→C in R, C→y in S


def test_compose_no_match():
    """Verify composition with no matching middle elements."""
    R = {(1, 2)}
    S = {(3, 4)}
    result = compose(R, S)
    assert result == set()


def test_compose_identity():
    """Verify composition with identity-like relation."""
    R = {(1, 1), (2, 2)}
    S = {(1, "a"), (2, "b")}
    result = compose(R, S)
    assert (1, "a") in result
    assert (2, "b") in result


# ──────────────────────────────────────────────
# equivalence_classes tests
# ──────────────────────────────────────────────
def test_equivalence_classes_two_classes():
    """Verify partitioning into two equivalence classes."""
    A = {1, 2, 3, 4}
    # Same parity equivalence: {1,3} and {2,4}
    R = {
        (1, 1), (2, 2), (3, 3), (4, 4),  # Reflexive
        (1, 3), (3, 1),                    # 1 ↔ 3
        (2, 4), (4, 2),                    # 2 ↔ 4
    }
    classes = equivalence_classes(R, A)
    assert len(classes) == 2
    # Check that each class is correct (order-independent)
    class_sets = [frozenset(c) for c in classes]
    assert frozenset({1, 3}) in class_sets
    assert frozenset({2, 4}) in class_sets


def test_equivalence_classes_identity():
    """Verify identity relation gives each element its own class."""
    A = {1, 2, 3}
    R = {(1, 1), (2, 2), (3, 3)}
    classes = equivalence_classes(R, A)
    assert len(classes) == 3


def test_equivalence_classes_single_class():
    """Verify full equivalence (all equal) gives one class."""
    A = {1, 2, 3}
    R = {(a, b) for a in A for b in A}  # All pairs
    classes = equivalence_classes(R, A)
    assert len(classes) == 1
    assert classes[0] == A
