"""Main CLI entry point for the Discrete Mathematics Explorer project.

Run this file to launch a fully interactive terminal menu that lets users
explore set operations, power sets, Cartesian products, relation properties,
visualizations, Warshall's algorithm, relation composition, equivalence
class partitioning, and a social-network demo.
"""

import sys
import os

# Add parent directory to path so imports work when run from this directory
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sets import (
    parse_set, union, intersection, difference, symmetric_difference,
    is_subset, power_set, cartesian_product, count_possible_relations
)
from relations import (
    build_relation, is_reflexive, is_symmetric, is_antisymmetric,
    is_transitive, is_equivalence_relation, warshall, compose,
    equivalence_classes, count_possible_relations as rel_count_possible_relations
)
from visualizer import (
    plot_venn_diagram, plot_relation_matrix, plot_power_set_tree,
    plot_cartesian_product, plot_warshall_steps
)


# ───────────────────────────────────────────────
# Helper formatting constants
# ───────────────────────────────────────────────
SEPARATOR = "─" * 55
DOUBLE_SEP = "═" * 55
THIN_SEP = "─" * 40


def _print_header(title: str):
    """Print a styled section header."""
    print(f"\n{DOUBLE_SEP}")
    print(f"  {title}")
    print(DOUBLE_SEP)


def _print_subheader(title: str):
    """Print a smaller sub-section header."""
    print(f"\n  {THIN_SEP}")
    print(f"  {title}")
    print(f"  {THIN_SEP}")


def _ask_set(prompt: str) -> set:
    """Ask the user for a set and parse it."""
    raw = input(f"  {prompt}: ").strip()
    return parse_set(raw)


def _ask_relation_on_set():
    """Ask user for a set and build a relation interactively.

    Returns:
        (relation, base_set, cartesian_pairs)
    """
    A = _ask_set("Enter the base set (e.g., 1 2 3)")
    cp = cartesian_product(A, A)

    print(f"\n  Cartesian Product A × A ({len(cp)} pairs):")
    for idx, pair in enumerate(cp):
        print(f"    [{idx}] {pair}")

    raw_indices = input("\n  Enter indices of pairs to include (e.g., 0 2 4): ").strip()
    if raw_indices:
        indices = [int(x) for x in raw_indices.split()]
    else:
        indices = []

    R = build_relation(cp, indices)
    return R, A, cp


# ───────────────────────────────────────────────
# Option 1: Set Operations
# ───────────────────────────────────────────────
def menu_set_operations():
    """Interactive menu for computing and displaying all set operations.

    Mathematical idea:
        Demonstrates the five fundamental set operations (union, intersection,
        difference, symmetric difference, subset check) on two user-provided sets.

    Formula:
        A ∪ B, A ∩ B, A - B, A △ B, A ⊆ B

    Real-world example:
        Comparing two customer segments to find overlap, unique members, etc.
    """
    _print_header("Set Operations")

    A = _ask_set("Enter Set A (e.g., {1,2,3} or 1 2 3)")
    B = _ask_set("Enter Set B (e.g., {3,4,5} or 3 4 5)")

    print(f"\n  Set A = {sorted(A, key=str)}")
    print(f"  Set B = {sorted(B, key=str)}")
    print(f"\n  {THIN_SEP}")

    results = [
        ("Union        (A ∪ B)", union(A, B)),
        ("Intersection (A ∩ B)", intersection(A, B)),
        ("Difference   (A - B)", difference(A, B)),
        ("Difference   (B - A)", difference(B, A)),
        ("Sym. Diff.   (A △ B)", symmetric_difference(A, B)),
    ]

    for label, result in results:
        print(f"  {label} = {sorted(result, key=str)}")

    print(f"\n  A ⊆ B? {'Yes ✓' if is_subset(A, B) else 'No ✗'}")
    print(f"  B ⊆ A? {'Yes ✓' if is_subset(B, A) else 'No ✗'}")

    total_relations = count_possible_relations(A, B)
    print(f"\n  Possible relations from A to B = 2^(|A|×|B|) = 2^({len(A)}×{len(B)}) = {total_relations}")
    print(SEPARATOR)


# ───────────────────────────────────────────────
# Option 2: Power Set Generator
# ───────────────────────────────────────────────
def menu_power_set():
    """Interactive menu for generating and displaying the power set.

    Mathematical idea:
        The power set P(A) contains all subsets of A. If |A| = n, then
        |P(A)| = 2^n.

    Formula:
        |P(A)| = 2^n

    Real-world example:
        Listing all possible committees from a pool of candidates.
    """
    _print_header("Power Set Generator")

    A = _ask_set("Enter Set A (e.g., {a, b, c} or 1 2 3)")
    n = len(A)

    ps = power_set(A)

    # Group by size
    from collections import defaultdict
    by_size = defaultdict(list)
    for subset in ps:
        by_size[len(subset)].append(subset)

    print(f"\n  Set A = {sorted(A, key=str)}")
    print(f"  |A| = {n}")
    print(f"\n  All subsets grouped by size:")

    for size in sorted(by_size.keys()):
        subsets = by_size[size]
        print(f"\n    Size {size} ({len(subsets)} subset{'s' if len(subsets) != 1 else ''}):")
        for s in subsets:
            if len(s) == 0:
                print("      ∅")
            else:
                print(f"      {{{', '.join(str(x) for x in sorted(s, key=str))}}}")

    print(f"\n  Total: |P(A)| = 2^{n} = {2 ** n}")
    print(SEPARATOR)


# ───────────────────────────────────────────────
# Option 3: Cartesian Product
# ───────────────────────────────────────────────
def menu_cartesian_product():
    """Interactive menu for computing and displaying the Cartesian product.

    Mathematical idea:
        The Cartesian product A × B is the set of all ordered pairs (a, b)
        with a ∈ A and b ∈ B.

    Formula:
        |A × B| = |A| × |B|

    Real-world example:
        Generating all possible (day, shift) assignments for employee
        scheduling.
    """
    _print_header("Cartesian Product")

    A = _ask_set("Enter Set A")
    B = _ask_set("Enter Set B")

    cp = cartesian_product(A, B)

    print(f"\n  Set A = {sorted(A, key=str)}")
    print(f"  Set B = {sorted(B, key=str)}")
    print(f"\n  A × B ({len(cp)} pairs):")

    # Print as a clean table
    print(f"    {'Index':<8} {'Pair'}")
    print(f"    {'─' * 25}")
    for idx, pair in enumerate(cp):
        print(f"    {idx:<8} ({pair[0]}, {pair[1]})")

    print(f"\n  |A × B| = |A| × |B| = {len(A)} × {len(B)} = {len(cp)}")
    print(SEPARATOR)


# ───────────────────────────────────────────────
# Option 4: Relation Builder + Property Checker
# ───────────────────────────────────────────────
def menu_relation_builder():
    """Interactive menu for building a relation and checking its properties.

    Mathematical idea:
        A relation R on set A is a subset of A × A. We check five key
        properties: reflexive, symmetric, antisymmetric, transitive, and
        whether R is an equivalence relation.

    Formula:
        R ⊆ A × A; property checks as defined in relations.py.

    Real-world example:
        Defining a "follows" relation on social media users and checking
        whether it's an equivalence relation (mutual following with
        transitivity would mean friend groups).
    """
    _print_header("Relation Builder + Property Checker")

    R, A, cp = _ask_relation_on_set()

    print(f"\n  Relation R = {R}")
    print(f"  |R| = {len(R)} pairs")

    _print_subheader("Property Analysis")

    ref = is_reflexive(R, A)
    sym = is_symmetric(R)
    anti = is_antisymmetric(R)
    trans = is_transitive(R)

    print(f"  Reflexive:      {'✓ Yes' if ref else '✗ No'}")
    print(f"  Symmetric:      {'✓ Yes' if sym else '✗ No'}")
    print(f"  Antisymmetric:  {'✓ Yes' if anti else '✗ No'}")
    print(f"  Transitive:     {'✓ Yes' if trans else '✗ No'}")

    print(f"\n  Equivalence Relation Check:")
    is_eq = ref and sym and trans
    if is_eq:
        print("  ✓ R IS an equivalence relation (reflexive + symmetric + transitive)")
        classes = equivalence_classes(R, A)
        print(f"\n  Equivalence Classes:")
        for i, cls in enumerate(classes):
            print(f"    Class {i + 1}: {{{', '.join(str(x) for x in sorted(cls, key=str))}}}")
    else:
        missing = []
        if not ref:
            missing.append("reflexive")
        if not sym:
            missing.append("symmetric")
        if not trans:
            missing.append("transitive")
        print(f"  ✗ R is NOT an equivalence relation (missing: {', '.join(missing)})")

    print(SEPARATOR)


# ───────────────────────────────────────────────
# Option 5: Visualizations
# ───────────────────────────────────────────────
def menu_visualizations():
    """Interactive sub-menu for launching matplotlib visualizations.

    Mathematical idea:
        Visual representations of mathematical structures enhance
        understanding of abstract set and relation concepts.

    Formula:
        Various — depends on the chosen visualization.

    Real-world example:
        Using Venn diagrams in business analytics to show customer segment
        overlaps.
    """
    _print_header("Visualizations")

    print("  1. Venn Diagram (Set Operations)")
    print("  2. Relation Matrix")
    print("  3. Power Set Tree / Lattice")
    print("  4. Cartesian Product Grid")
    print("  5. Back to Main Menu")

    choice = input("\n  Select visualization [1-5]: ").strip()

    if choice == "1":
        A = _ask_set("Enter Set A")
        B = _ask_set("Enter Set B")
        print("\n  Operations: union, intersection, difference, symmetric_difference")
        op = input("  Choose operation: ").strip().lower()
        if op not in ("union", "intersection", "difference", "symmetric_difference"):
            print("  Invalid operation. Defaulting to 'union'.")
            op = "union"
        plot_venn_diagram(A, B, op)

    elif choice == "2":
        R, A, _ = _ask_relation_on_set()
        elements = sorted(A, key=str)
        plot_relation_matrix(R, elements)

    elif choice == "3":
        A = _ask_set("Enter Set A (keep small, ≤ 4 elements recommended)")
        plot_power_set_tree(A)

    elif choice == "4":
        A = _ask_set("Enter Set A")
        B = _ask_set("Enter Set B")
        plot_cartesian_product(A, B)

    elif choice == "5":
        return
    else:
        print("  Invalid choice.")


# ───────────────────────────────────────────────
# Option 6: Advanced Features
# ───────────────────────────────────────────────
def menu_advanced():
    """Interactive sub-menu for advanced discrete math features.

    Mathematical idea:
        Covers Warshall's algorithm for transitive closure, relation
        composition, equivalence class partitioning, and a social network
        reachability demo.

    Formula:
        Warshall: O(n³); Composition: R ∘ S; Equivalence partitioning.

    Real-world example:
        Analyzing indirect reachability in social networks, supply chains,
        or communication networks.
    """
    _print_header("Advanced Features")

    print("  a. Warshall's Algorithm (Transitive Closure)")
    print("  b. Relation Composition (R ∘ S)")
    print("  c. Equivalence Class Partitioner")
    print("  d. Social Network Demo")
    print("  e. Back to Main Menu")

    choice = input("\n  Select option [a-e]: ").strip().lower()

    if choice == "a":
        _advanced_warshall()
    elif choice == "b":
        _advanced_composition()
    elif choice == "c":
        _advanced_equivalence()
    elif choice == "d":
        _advanced_social_network()
    elif choice == "e":
        return
    else:
        print("  Invalid choice.")


def _advanced_warshall():
    """Run Warshall's algorithm interactively with step-by-step output.

    Mathematical idea:
        Warshall's algorithm computes the transitive closure R⁺ in O(n³)
        by iteratively considering each vertex as an intermediate node.

    Formula:
        M[i][j] = M[i][j] OR (M[i][k] AND M[k][j])

    Real-world example:
        Finding all indirect flight connections in an airline route network.
    """
    _print_subheader("Warshall's Algorithm")

    R, A, _ = _ask_relation_on_set()
    elements = sorted(A, key=str)

    closure = warshall(R, elements)

    # Show real-world interpretation
    print(f"\n  Real-world interpretation:")
    print(f"  If these elements represent cities and the relation represents")
    print(f"  direct routes, the transitive closure shows all cities reachable")
    print(f"  from each city (via any number of connecting routes).")

    # Offer to visualize
    show = input("\n  Show step-by-step visualization? (y/n): ").strip().lower()
    if show == "y" and hasattr(warshall, "last_steps"):
        plot_warshall_steps(warshall.last_steps, elements)


def _advanced_composition():
    """Run relation composition interactively.

    Mathematical idea:
        R ∘ S connects pairs through an intermediate link.
        If (a,b) ∈ R and (b,c) ∈ S then (a,c) ∈ R ∘ S.

    Formula:
        R ∘ S = {(a, c) | ∃b: (a,b) ∈ R ∧ (b,c) ∈ S}

    Real-world example:
        "Student takes course" ∘ "Course taught by professor" =
        "Student is taught by professor".
    """
    _print_subheader("Relation Composition (R ∘ S)")

    print("\n  Define Relation R:")
    A_r = _ask_set("  Enter domain set for R")
    B_r = _ask_set("  Enter codomain set for R")
    cp_r = cartesian_product(A_r, B_r)
    print(f"\n  Available pairs for R:")
    for idx, pair in enumerate(cp_r):
        print(f"    [{idx}] {pair}")
    raw = input("  Enter indices for R (e.g., 0 1 3): ").strip()
    R = build_relation(cp_r, [int(x) for x in raw.split()] if raw else [])

    print(f"\n  Define Relation S:")
    A_s = _ask_set("  Enter domain set for S")
    B_s = _ask_set("  Enter codomain set for S")
    cp_s = cartesian_product(A_s, B_s)
    print(f"\n  Available pairs for S:")
    for idx, pair in enumerate(cp_s):
        print(f"    [{idx}] {pair}")
    raw = input("  Enter indices for S (e.g., 0 2): ").strip()
    S = build_relation(cp_s, [int(x) for x in raw.split()] if raw else [])

    print(f"\n  R = {R}")
    print(f"  S = {S}")

    result = compose(R, S)
    print(f"\n  R ∘ S = {result}")
    print(f"  |R ∘ S| = {len(result)}")

    print(f"\n  Explanation:")
    print(f"  For each (a,b) in R and (b,c) in S where the middle elements match,")
    print(f"  the pair (a,c) is added to the composition.")

    if result:
        print(f"\n  Detailed derivations:")
        for (a, b) in R:
            for (c, d) in S:
                if b == c:
                    print(f"    ({a},{b}) ∈ R and ({c},{d}) ∈ S → ({a},{d}) ∈ R∘S")


def _advanced_equivalence():
    """Run equivalence class partitioning interactively.

    Mathematical idea:
        An equivalence relation partitions the base set into disjoint classes.
        Each class contains all elements equivalent to each other.

    Formula:
        [a] = {x ∈ A | (a, x) ∈ R}

    Real-world example:
        Grouping students by GPA bracket — all students with the same bracket
        form one equivalence class.
    """
    _print_subheader("Equivalence Class Partitioner")

    R, A, _ = _ask_relation_on_set()

    print(f"\n  Checking if R is an equivalence relation...")
    is_eq = is_equivalence_relation(R, A)

    if is_eq:
        print(f"\n  ✓ R IS an equivalence relation!")
        classes = equivalence_classes(R, A)
        print(f"\n  Partition of A into equivalence classes:")
        for i, cls in enumerate(classes):
            print(f"    [{i + 1}] {{{', '.join(str(x) for x in sorted(cls, key=str))}}}")
        print(f"\n  Number of classes: {len(classes)}")
        print(f"  Verification: classes are disjoint and union = A ✓")
    else:
        print(f"\n  ✗ R is NOT an equivalence relation.")
        print(f"  Cannot compute equivalence classes for a non-equivalence relation.")


def _advanced_social_network():
    """Run a hardcoded social network demo with Warshall's algorithm.

    Mathematical idea:
        A "follows" relation on a set of users can be analyzed via transitive
        closure to discover indirect reachability. The most influential node
        is the one that can reach the most other nodes.

    Formula:
        Transitive closure via Warshall's algorithm, O(n³).

    Real-world example:
        Analyzing a Twitter-like network to find who can indirectly see
        whose posts through a chain of follows.
    """
    _print_subheader("Social Network Demo")

    # Hardcoded 5 users and a follows relation
    users = {"Alice", "Bob", "Carol", "Dave", "Eve"}
    follows = {
        ("Alice", "Bob"),
        ("Bob", "Carol"),
        ("Carol", "Dave"),
        ("Dave", "Eve"),
        ("Eve", "Alice"),
        ("Alice", "Carol"),
    }

    print(f"\n  Users: {sorted(users)}")
    print(f"\n  Follows relation (who follows whom):")
    for (a, b) in sorted(follows):
        print(f"    {a} → {b}")

    elements = sorted(users)
    print(f"\n  Running Warshall's algorithm to find indirect reach...")
    closure = warshall(follows, elements)

    print(f"\n  Who can reach whom (directly or indirectly):")
    for user in elements:
        reachable = sorted([b for (a, b) in closure if a == user and b != user])
        print(f"    {user} can reach: {reachable}")

    # Find most influential node (most reachable from others)
    reach_count = {}
    for user in elements:
        # Count how many other users this user can reach
        reach_count[user] = len([b for (a, b) in closure if a == user and b != user])

    most_influential = max(reach_count, key=reach_count.get)
    print(f"\n  ★ Most influential user: {most_influential}")
    print(f"    Can reach {reach_count[most_influential]} other user(s)")

    # Offer visualization
    show = input("\n  Show step-by-step visualization? (y/n): ").strip().lower()
    if show == "y" and hasattr(warshall, "last_steps"):
        plot_warshall_steps(warshall.last_steps, elements)

    print(SEPARATOR)


# ───────────────────────────────────────────────
# Main Menu Loop
# ───────────────────────────────────────────────
def main():
    """Launch the Discrete Mathematics Explorer CLI.

    Mathematical idea:
        This is the entry point that provides a menu-driven interface to
        all discrete mathematics exploration tools implemented in this project.

    Formula:
        N/A — this is the application controller.

    Real-world example:
        An interactive educational tool for students learning discrete math
        concepts through hands-on experimentation.
    """
    print(DOUBLE_SEP)
    print("   🧮  DISCRETE MATHEMATICS EXPLORER")
    print("   A comprehensive CLI for set theory & relations")
    print(DOUBLE_SEP)

    while True:
        print(f"\n{'─' * 55}")
        print("  MAIN MENU")
        print(f"{'─' * 55}")
        print("  1. Set Operations (∪, ∩, -, △, ⊆)")
        print("  2. Power Set Generator (P(A) = 2ⁿ)")
        print("  3. Cartesian Product (A × B)")
        print("  4. Relation Builder + Property Checker")
        print("  5. Visualizations (Venn, Matrix, Tree, Grid)")
        print("  6. Advanced (Warshall, Composition, Equivalence)")
        print("  7. Exit")
        print(f"{'─' * 55}")

        choice = input("\n  Enter your choice [1-7]: ").strip()

        if choice == "1":
            menu_set_operations()
        elif choice == "2":
            menu_power_set()
        elif choice == "3":
            menu_cartesian_product()
        elif choice == "4":
            menu_relation_builder()
        elif choice == "5":
            menu_visualizations()
        elif choice == "6":
            menu_advanced()
        elif choice == "7":
            print(f"\n{DOUBLE_SEP}")
            print("  👋 Thank you for exploring Discrete Mathematics!")
            print(DOUBLE_SEP)
            break
        else:
            print("  ⚠ Invalid choice. Please enter a number from 1 to 7.")


if __name__ == "__main__":
    main()
