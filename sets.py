"""Set operations module for the Discrete Mathematics Explorer project.

Provides functions for fundamental set operations including union, intersection,
difference, symmetric difference, subset checking, power set generation,
Cartesian product computation, and relation counting.
"""

import itertools


def parse_set(input_string: str) -> set:
    """Parse a raw input string into a cleaned, deduplicated set.

    Mathematical idea:
        Parsing a set from user input maps a raw textual representation into a
        clean finite set A. Since sets contain unique elements by definition,
        duplicates are removed so that each element appears exactly once.

    Formula:
        A = {x | x appears in cleaned_input}

    Real-world example:
        Building a unique list of registered usernames from repeated form
        submissions. E.g., input "alice, bob, alice, carol" → {alice, bob, carol}.

    Args:
        input_string: A string like "1 2 3", "{1,2,3}", "1,2,3", or "{a, b, c}".

    Returns:
        A Python set of parsed elements (integers if possible, strings otherwise).
    """
    # Strip surrounding whitespace and curly braces
    cleaned = input_string.strip().strip("{}")

    # Split on commas first; if no commas, split on whitespace
    if "," in cleaned:
        tokens = cleaned.split(",")
    else:
        tokens = cleaned.split()

    result = set()
    for token in tokens:
        token = token.strip()
        if not token:
            continue
        # Try converting to integer; fall back to string
        try:
            result.add(int(token))
        except ValueError:
            result.add(token)

    return result


def union(A: set, B: set) -> set:
    """Return the union of two sets.

    Mathematical idea:
        Union combines everything that belongs to A or B (or both).
        It produces the full coverage of elements across two sets.

    Formula:
        A ∪ B = {x | x ∈ A or x ∈ B}

    Real-world example:
        Combining customers from two mailing lists into one master list.
        If list A = {Alice, Bob} and list B = {Bob, Carol}, the master
        list is {Alice, Bob, Carol}.

    Args:
        A: First set.
        B: Second set.

    Returns:
        The union A ∪ B.
    """
    return A | B


def intersection(A: set, B: set) -> set:
    """Return the intersection of two sets.

    Mathematical idea:
        Intersection keeps only elements shared by both A and B.
        It captures common membership between sets.

    Formula:
        A ∩ B = {x | x ∈ A and x ∈ B}

    Real-world example:
        Finding students enrolled in both Mathematics and Computer Science
        courses. If Math = {Alice, Bob, Carol} and CS = {Bob, Carol, Dave},
        the common students are {Bob, Carol}.

    Args:
        A: First set.
        B: Second set.

    Returns:
        The intersection A ∩ B.
    """
    return A & B


def difference(A: set, B: set) -> set:
    """Return the set difference A - B.

    Mathematical idea:
        Difference keeps elements in A that are not in B.
        This is directional, so A - B is generally different from B - A.

    Formula:
        A - B = {x | x ∈ A and x ∉ B}

    Real-world example:
        Finding users who subscribed this month but were not previously
        subscribed. If new = {Alice, Bob, Dave} and old = {Alice, Carol},
        the truly new subscribers are {Bob, Dave}.

    Args:
        A: First set (minuend).
        B: Second set (subtrahend).

    Returns:
        The difference A - B.
    """
    return A - B


def symmetric_difference(A: set, B: set) -> set:
    """Return the symmetric difference of two sets.

    Mathematical idea:
        Symmetric difference keeps elements that belong to exactly one of
        A or B. It removes shared elements and keeps non-overlapping ones.

    Formula:
        A △ B = (A - B) ∪ (B - A) = {x | x ∈ A ⊕ x ∈ B}

    Real-world example:
        Identifying features available in version 1 or version 2 of
        software, but not both. If v1 = {dark_mode, search} and
        v2 = {search, autocomplete}, then exclusive features are
        {dark_mode, autocomplete}.

    Args:
        A: First set.
        B: Second set.

    Returns:
        The symmetric difference A △ B.
    """
    return A ^ B


def is_subset(A: set, B: set) -> bool:
    """Check whether A is a subset of B.

    Mathematical idea:
        A is a subset of B if every element of A is also in B.
        This checks containment between sets.

    Formula:
        A ⊆ B ⟺ ∀x (x ∈ A ⇒ x ∈ B)

    Real-world example:
        Verifying that all required permissions for a role are included in
        a user's granted permissions. If required = {read, write} and
        granted = {read, write, delete}, then required ⊆ granted.

    Args:
        A: The candidate subset.
        B: The candidate superset.

    Returns:
        True if A ⊆ B, False otherwise.
    """
    return A.issubset(B)


def power_set(A: set) -> list:
    """Return the power set of A as a list of frozensets.

    Mathematical idea:
        The power set of A is the set of all subsets of A, including the
        empty set ∅ and A itself. If |A| = n, then the power set has
        exactly 2^n subsets.

    Formula:
        P(A) = {S | S ⊆ A}, and |P(A)| = 2^|A|

    Real-world example:
        Generating all possible teams from a fixed group of employees.
        For employees = {Alice, Bob, Carol}, the 2^3 = 8 possible teams
        range from {} (no one) to {Alice, Bob, Carol} (everyone).

    Args:
        A: The input set.

    Returns:
        A list of frozensets, each representing one subset of A.
    """
    elements = sorted(A, key=str)
    # Use itertools.chain and itertools.combinations to generate all subsets
    # r ranges from 0 (empty set) to len(A) (the full set)
    return [
        frozenset(combo)
        for combo in itertools.chain.from_iterable(
            itertools.combinations(elements, r)
            for r in range(len(elements) + 1)
        )
    ]


def cartesian_product(A: set, B: set) -> list:
    """Return the Cartesian product A × B as a list of tuples.

    Mathematical idea:
        The Cartesian product pairs each element of A with each element of B
        in ordered pairs. Order matters: (a, b) is generally not the same as
        (b, a).

    Formula:
        A × B = {(a, b) | a ∈ A and b ∈ B}, and |A × B| = |A| × |B|

    Real-world example:
        Generating all possible (day, shift) assignments for scheduling.
        If days = {Mon, Tue} and shifts = {morning, evening}, then
        A × B = {(Mon,morning), (Mon,evening), (Tue,morning), (Tue,evening)}.

    Args:
        A: First set.
        B: Second set.

    Returns:
        A list of (a, b) tuples for all a ∈ A, b ∈ B.
    """
    return list(itertools.product(sorted(A, key=str), sorted(B, key=str)))


def count_possible_relations(A: set, B: set) -> int:
    """Count the total number of possible relations from A to B.

    Mathematical idea:
        A relation R from A to B is any subset of A × B. Since |A × B| = |A|·|B|,
        there are 2^(|A|·|B|) possible subsets, each corresponding to one
        possible relation. Each pair (a, b) is independently included or
        excluded, giving two choices per pair.

    Formula:
        Number of relations from A to B = 2^(|A| × |B|)

    Real-world example:
        Counting all possible ways to define "can access" mappings between
        users and resources. With 3 users and 4 resources, there are
        2^(3×4) = 2^12 = 4096 possible access configurations.

    Args:
        A: First set (domain).
        B: Second set (codomain).

    Returns:
        An integer representing the total count of possible relations.
    """
    return 2 ** (len(A) * len(B))
