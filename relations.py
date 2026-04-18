"""Relation operations module for the Discrete Mathematics Explorer project.

Provides functions for building relations, checking relation properties
(reflexive, symmetric, antisymmetric, transitive), testing for equivalence
relations, computing transitive closures via Warshall's algorithm,
composing relations, and extracting equivalence classes.
"""


def build_relation(cartesian_pairs: list, selected_indices: list) -> set:
    """Build a relation by selecting specific ordered pairs from a Cartesian product list.

    Mathematical idea:
        A relation R from A to B is any subset of the Cartesian product A × B.
        This function lets the user pick which ordered pairs to include by index.

    Formula:
        R ⊆ A × B

    Real-world example:
        Building a "student is enrolled in course" relation from all possible
        student-course pairs. The user selects which enrollments are active.

    Args:
        cartesian_pairs: A list of tuples from cartesian_product().
        selected_indices: A list of integer indices into cartesian_pairs.

    Returns:
        A set of the selected tuples forming the relation R.
    """
    return {cartesian_pairs[i] for i in selected_indices if 0 <= i < len(cartesian_pairs)}


def is_reflexive(R: set, A: set) -> bool:
    """Check whether relation R is reflexive on set A.

    Mathematical idea:
        A relation on A is reflexive if every element relates to itself.
        Every (a, a) must appear in R for all a in A.

    Formula:
        Reflexive ⟺ ∀a ∈ A, (a, a) ∈ R

    Real-world example:
        "Has same age as" is reflexive because each person has the same age
        as themselves. If A = {Alice, Bob}, then both (Alice, Alice) and
        (Bob, Bob) must be in R.

    Args:
        R: The relation as a set of tuples.
        A: The base set.

    Returns:
        True if R is reflexive on A, False otherwise.
    """
    return all((a, a) in R for a in A)


def is_symmetric(R: set) -> bool:
    """Check whether relation R is symmetric.

    Mathematical idea:
        A relation is symmetric if whenever (a, b) is in R, then (b, a) is
        also in R. Relations hold in both directions for every related pair.

    Formula:
        Symmetric ⟺ ∀a, b, (a, b) ∈ R ⇒ (b, a) ∈ R

    Real-world example:
        "Is a sibling of" is symmetric: if Alice is a sibling of Bob,
        then Bob is a sibling of Alice.

    Args:
        R: The relation as a set of tuples.

    Returns:
        True if R is symmetric, False otherwise.
    """
    return all((b, a) in R for (a, b) in R)


def is_antisymmetric(R: set) -> bool:
    """Check whether relation R is antisymmetric.

    Mathematical idea:
        A relation is antisymmetric if for distinct elements a and b, both
        (a, b) and (b, a) cannot be true at the same time. The only case
        where both (a, b) ∈ R and (b, a) ∈ R is when a = b.

    Formula:
        Antisymmetric ⟺ ∀a, b, ((a, b) ∈ R and (b, a) ∈ R) ⇒ a = b

    Real-world example:
        "Less than or equal to" on numbers is antisymmetric: if a ≤ b and
        b ≤ a, then a = b.

    Args:
        R: The relation as a set of tuples.

    Returns:
        True if R is antisymmetric, False otherwise.
    """
    for (a, b) in R:
        if a != b and (b, a) in R:
            return False
    return True


def is_transitive(R: set) -> bool:
    """Check whether relation R is transitive.

    Mathematical idea:
        A relation is transitive if related chains imply a direct relation.
        If (a, b) and (b, c) are in R, then (a, c) must also be in R.

    Formula:
        Transitive ⟺ ∀a, b, c, ((a, b) ∈ R and (b, c) ∈ R) ⇒ (a, c) ∈ R

    Real-world example:
        "Is an ancestor of" is transitive: if Alice is an ancestor of Bob,
        and Bob is an ancestor of Carol, then Alice is an ancestor of Carol.

    Args:
        R: The relation as a set of tuples.

    Returns:
        True if R is transitive, False otherwise.
    """
    # Use nested loops over all pairs in R
    for (a, b) in R:
        for (c, d) in R:
            # If the second element of one pair matches the first of another
            if b == c and (a, d) not in R:
                return False
    return True


def is_equivalence_relation(R: set, A: set) -> bool:
    """Check whether relation R is an equivalence relation on A.

    Mathematical idea:
        An equivalence relation must satisfy three properties simultaneously:
        reflexive, symmetric, and transitive. If all three hold, R partitions
        A into disjoint equivalence classes.

    Formula:
        Equivalence ⟺ Reflexive ∧ Symmetric ∧ Transitive

    Real-world example:
        "Has the same remainder mod n" on integers is an equivalence relation.
        For mod 3: {0,3,6,...}, {1,4,7,...}, {2,5,8,...} are equivalence classes.

    Args:
        R: The relation as a set of tuples.
        A: The base set.

    Returns:
        True if R is an equivalence relation on A, False otherwise.
    """
    # Check each property individually and print status
    ref = is_reflexive(R, A)
    sym = is_symmetric(R)
    trans = is_transitive(R)

    print(f"  ├─ Reflexive:   {'✓ PASS' if ref else '✗ FAIL'}")
    print(f"  ├─ Symmetric:   {'✓ PASS' if sym else '✗ FAIL'}")
    print(f"  └─ Transitive:  {'✓ PASS' if trans else '✗ FAIL'}")

    return ref and sym and trans


def count_possible_relations(A: set, B: set) -> int:
    """Count total possible relations from A to B.

    Mathematical idea:
        If |A| = m and |B| = n, then |A × B| = mn. Any subset of A × B can
        be a relation, so the number of possible relations is 2^(mn). Each
        pair in A × B is independently included or excluded, giving two
        choices per pair.

    Formula:
        Number of relations from A to B = 2^(|A| · |B|)

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


def warshall(R: set, elements: list) -> set:
    """Compute the transitive closure of relation R using Warshall's algorithm.

    Mathematical idea:
        Warshall's algorithm computes the transitive closure R⁺ of a relation
        R by iteratively considering each element as an intermediate node.
        If there exists a path from i to k and from k to j, then there is a
        path from i to j. The algorithm runs three nested loops over all
        elements.

    Formula:
        R⁺ = smallest transitive relation containing R.
        After iteration k: M[i][j] = M[i][j] OR (M[i][k] AND M[k][j])

    Time complexity: O(n³) where n = |elements|

    Real-world example:
        In a social network, if Alice follows Bob and Bob follows Carol,
        the transitive closure reveals Alice can reach Carol indirectly.

    Args:
        R: The relation as a set of tuples.
        elements: Sorted list of unique elements appearing in the relation.

    Returns:
        The transitive closure as a set of tuples.
    """
    n = len(elements)
    # Map elements to indices
    index_of = {elem: i for i, elem in enumerate(elements)}

    # Initialize n×n boolean matrix from the relation
    matrix = [[False] * n for _ in range(n)]
    for (a, b) in R:
        if a in index_of and b in index_of:
            matrix[index_of[a]][index_of[b]] = True

    # Store initial matrix for step-by-step visualization
    steps = []
    steps.append([row[:] for row in matrix])  # Initial state

    print(f"\n{'─' * 50}")
    print("Warshall's Algorithm — Step-by-step")
    print(f"{'─' * 50}")
    _print_matrix(matrix, elements, "Initial Matrix")

    # Warshall's algorithm — three nested loops (k, i, j)
    for k in range(n):
        new_pairs = []
        for i in range(n):
            for j in range(n):
                if not matrix[i][j] and matrix[i][k] and matrix[k][j]:
                    matrix[i][j] = True
                    new_pairs.append((elements[i], elements[j]))

        steps.append([row[:] for row in matrix])  # Snapshot after step k

        print(f"\n  Step k={k} (intermediate node: {elements[k]}):")
        if new_pairs:
            print(f"    New pairs added: {new_pairs}")
        else:
            print("    No new pairs added.")
        _print_matrix(matrix, elements, f"Matrix after k={k}")

    # Convert matrix back to set of tuples
    closure = set()
    for i in range(n):
        for j in range(n):
            if matrix[i][j]:
                closure.add((elements[i], elements[j]))

    print(f"\n{'─' * 50}")
    print(f"  Transitive Closure R⁺ = {closure}")
    print(f"{'─' * 50}")

    # Attach steps as an attribute so visualizer can use them
    warshall.last_steps = steps

    return closure


def _print_matrix(matrix: list, elements: list, title: str):
    """Helper to print a labeled boolean matrix.

    Args:
        matrix: 2D list of booleans.
        elements: Element labels for rows/columns.
        title: Title for the printout.
    """
    n = len(elements)
    # Determine column width based on element labels
    col_w = max(len(str(e)) for e in elements) + 2

    print(f"\n    {title}:")
    # Column headers
    header = " " * (col_w + 4) + "".join(str(e).center(col_w) for e in elements)
    print(f"    {header}")
    print(f"    {' ' * (col_w + 4)}{'─' * (col_w * n)}")

    for i, elem in enumerate(elements):
        row_str = "".join(
            ("1" if matrix[i][j] else "0").center(col_w)
            for j in range(n)
        )
        print(f"    {str(elem).rjust(col_w)} │ {row_str}")


def compose(R: set, S: set) -> set:
    """Compute the composition R ∘ S of two relations.

    Mathematical idea:
        The composition R ∘ S connects pairs through an intermediate link.
        If (a, b) ∈ R and (b, c) ∈ S, then (a, c) ∈ R ∘ S. The middle
        element b acts as a bridge.

    Formula:
        R ∘ S = {(a, c) | ∃b such that (a, b) ∈ R and (b, c) ∈ S}

    Real-world example:
        If R = "student takes course" and S = "course is taught by professor",
        then R ∘ S = "student is taught by professor".

    Args:
        R: First relation as a set of tuples.
        S: Second relation as a set of tuples.

    Returns:
        The composition R ∘ S as a set of tuples.
    """
    result = set()
    for (a, b) in R:
        for (c, d) in S:
            if b == c:
                result.add((a, d))
    return result


def equivalence_classes(R: set, A: set) -> list:
    """Partition set A into equivalence classes induced by relation R.

    Mathematical idea:
        If R is an equivalence relation on A, it partitions A into disjoint
        equivalence classes. Each class [a] = {x ∈ A | (a, x) ∈ R}. The
        classes are non-empty, mutually disjoint, and their union is A.

    Formula:
        [a] = {x ∈ A | (a, x) ∈ R} for each a ∈ A
        A = [a₁] ∪ [a₂] ∪ ... ∪ [aₖ] (disjoint union)

    Real-world example:
        Grouping students by their graduation year. Students with the same
        year form one equivalence class.

    Note:
        Only call this if is_equivalence_relation() returns True.

    Args:
        R: An equivalence relation as a set of tuples.
        A: The base set.

    Returns:
        A list of sets, each representing one equivalence class.
    """
    # Use a union-find / BFS approach
    # Build adjacency: for each a, find all b such that (a, b) ∈ R
    visited = set()
    classes = []

    for element in sorted(A, key=str):
        if element in visited:
            continue
        # BFS to find all elements equivalent to this one
        eq_class = set()
        queue = [element]
        while queue:
            current = queue.pop(0)
            if current in eq_class:
                continue
            eq_class.add(current)
            # Find neighbors: elements related to current
            for (a, b) in R:
                if a == current and b in A and b not in eq_class:
                    queue.append(b)
                if b == current and a in A and a not in eq_class:
                    queue.append(a)
        visited |= eq_class
        classes.append(eq_class)

    return classes
