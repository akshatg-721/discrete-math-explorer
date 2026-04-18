"""Visualization module for the Discrete Mathematics Explorer project.

Provides matplotlib-based visualizations for set operations (Venn diagrams),
relation matrices, power set trees, Cartesian product grids, and Warshall's
algorithm step-by-step matrices.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib_venn import venn2, venn2_circles
import numpy as np


def plot_venn_diagram(A: set, B: set, operation: str):
    """Plot a Venn diagram for two sets and a selected set operation.

    Mathematical idea:
        A two-set Venn diagram visualizes region membership for A, B, and
        overlaps between them. Different operations highlight different regions:
        union (A ∪ B), intersection (A ∩ B), difference (A - B), and
        symmetric difference (A △ B).

    Formula:
        Regions are based on |A - B|, |B - A|, and |A ∩ B|.

    Real-world example:
        Visualizing overlap between users who bought Product X and users who
        bought Product Y to understand cross-selling opportunities.

    Args:
        A: First set.
        B: Second set.
        operation: One of "union", "intersection", "difference",
                   "symmetric_difference".
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#1a1a2e")

    # Compute Venn region sizes
    only_a = len(A - B)
    only_b = len(B - A)
    both = len(A & B)

    v = venn2(subsets=(only_a, only_b, both),
              set_labels=("Set A", "Set B"), ax=ax)

    # Style the labels
    for text in v.set_labels:
        if text:
            text.set_color("white")
            text.set_fontsize(14)
            text.set_fontweight("bold")

    for text in v.subset_labels:
        if text:
            text.set_color("white")
            text.set_fontsize(11)

    # Add circles outline
    circles = venn2_circles(subsets=(only_a, only_b, both), ax=ax,
                            linewidth=2, color="white")

    # Define colors for highlighting
    highlight_color = "#00d2ff"
    dim_color = "#2a2a4a"
    active_color = "#16c79a"

    # Color regions based on operation
    ids = ["10", "01", "11"]  # only_a, only_b, intersection
    operation_map = {
        "union":                {"10": active_color, "01": active_color, "11": active_color},
        "intersection":         {"10": dim_color,    "01": dim_color,    "11": highlight_color},
        "difference":           {"10": active_color, "01": dim_color,    "11": dim_color},
        "symmetric_difference": {"10": active_color, "01": active_color, "11": dim_color},
    }

    colors = operation_map.get(operation, operation_map["union"])
    for region_id in ids:
        patch = v.get_patch_by_id(region_id)
        if patch:
            patch.set_color(colors[region_id])
            patch.set_alpha(0.7)
            patch.set_edgecolor("white")

    # Compute the result set for the legend
    op_funcs = {
        "union": A | B,
        "intersection": A & B,
        "difference": A - B,
        "symmetric_difference": A ^ B,
    }
    result = op_funcs.get(operation, A | B)

    op_symbols = {
        "union": "A ∪ B",
        "intersection": "A ∩ B",
        "difference": "A - B",
        "symmetric_difference": "A △ B",
    }

    title = f"Venn Diagram — {op_symbols.get(operation, operation)}"
    ax.set_title(title, fontsize=16, fontweight="bold", color="white", pad=20)

    # Legend
    legend_text = f"Result: {sorted(result, key=str)}"
    legend_patch = mpatches.Patch(color=active_color, label=legend_text)
    ax.legend(handles=[legend_patch], loc="lower right", fontsize=10,
              facecolor="#1a1a2e", edgecolor="white", labelcolor="white")

    plt.tight_layout()
    plt.show()


def plot_relation_matrix(R: set, elements: list):
    """Plot a relation matrix visualization for relation R.

    Mathematical idea:
        A relation matrix (adjacency matrix) represents R ⊆ A × A as a
        binary matrix M, where M[i][j] = 1 if (aᵢ, aⱼ) ∈ R, otherwise 0.

    Formula:
        M_ij = 1 if (aᵢ, aⱼ) ∈ R, else 0

    Real-world example:
        Showing which employees are assigned to which projects in a binary
        assignment grid. A filled cell means "is assigned to".

    Args:
        R: The relation as a set of tuples.
        elements: Sorted list of unique elements (used for both rows and cols).
    """
    n = len(elements)
    index_of = {elem: i for i, elem in enumerate(elements)}

    # Build the boolean matrix
    matrix = np.zeros((n, n), dtype=int)
    for (a, b) in R:
        if a in index_of and b in index_of:
            matrix[index_of[a]][index_of[b]] = 1

    fig, ax = plt.subplots(figsize=(max(6, n + 2), max(6, n + 2)))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#1a1a2e")

    # Use a green/dark colormap
    cmap = plt.cm.colors.ListedColormap(["#1a1a2e", "#16c79a"])
    bounds = [-0.5, 0.5, 1.5]
    norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)

    im = ax.imshow(matrix, cmap=cmap, norm=norm, aspect="equal")

    # Label rows and columns
    str_elements = [str(e) for e in elements]
    ax.set_xticks(range(n))
    ax.set_xticklabels(str_elements, fontsize=12, color="white")
    ax.set_yticks(range(n))
    ax.set_yticklabels(str_elements, fontsize=12, color="white")

    # Add text annotations in cells
    for i in range(n):
        for j in range(n):
            text_color = "#1a1a2e" if matrix[i][j] == 1 else "#555555"
            ax.text(j, i, str(matrix[i][j]), ha="center", va="center",
                    fontsize=14, fontweight="bold", color=text_color)

    # Add gridlines
    ax.set_xticks([x - 0.5 for x in range(1, n)], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, n)], minor=True)
    ax.grid(which="minor", color="#333355", linewidth=1)
    ax.tick_params(which="minor", size=0)

    # Colorbar
    cbar = fig.colorbar(im, ax=ax, ticks=[0, 1], shrink=0.6)
    cbar.ax.set_yticklabels(["0 (not in R)", "1 (in R)"], color="white")
    cbar.ax.yaxis.set_tick_params(color="white")

    ax.set_title("Relation Matrix", fontsize=16, fontweight="bold",
                 color="white", pad=15)
    ax.set_xlabel("Column elements", fontsize=12, color="white")
    ax.set_ylabel("Row elements", fontsize=12, color="white")

    plt.tight_layout()
    plt.show()


def plot_power_set_tree(A: set):
    """Plot a tree/lattice visualization for the power set of A.

    Mathematical idea:
        The power set can be visualized as a subset lattice where each level
        corresponds to subset size. Layer 0 = empty set, Layer n = A itself.
        Lines connect subsets that differ by exactly one element.

    Formula:
        P(A) = {S | S ⊆ A}, with |P(A)| = 2^|A|

    Real-world example:
        Visualizing all possible feature bundles from a fixed set of product
        features to understand which combinations are available.

    Args:
        A: The input set.
    """
    import itertools

    elements = sorted(A, key=str)
    n = len(elements)

    # Generate all subsets grouped by size
    layers = {}
    for r in range(n + 1):
        combos = list(itertools.combinations(elements, r))
        layers[r] = [frozenset(c) for c in combos]

    # Assign positions: x spread per layer, y = layer number
    positions = {}
    node_labels = {}
    total_layers = n + 1

    fig, ax = plt.subplots(figsize=(max(10, 2 ** n * 1.5), max(6, total_layers * 2)))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#1a1a2e")

    for layer_idx, subsets in layers.items():
        count = len(subsets)
        for i, subset in enumerate(subsets):
            # Center the nodes in each layer
            x = (i - (count - 1) / 2) * 2.5
            y = -layer_idx * 2  # Top-down
            positions[subset] = (x, y)
            # Label
            if len(subset) == 0:
                label = "∅"
            else:
                label = "{" + ", ".join(str(e) for e in sorted(subset, key=str)) + "}"
            node_labels[subset] = label

    # Draw edges: connect subsets that differ by exactly one element
    for r in range(n):
        for parent in layers[r]:
            for child in layers[r + 1]:
                if parent.issubset(child) and len(child - parent) == 1:
                    x0, y0 = positions[parent]
                    x1, y1 = positions[child]
                    ax.plot([x0, x1], [y0, y1], color="#555588", linewidth=1,
                            zorder=1, alpha=0.6)

    # Draw nodes
    for subset, (x, y) in positions.items():
        layer_size = len(subset)
        # Color gradient by layer
        colors = ["#e94560", "#ff6b6b", "#ffa502", "#16c79a",
                  "#00d2ff", "#7c5cff", "#ff6bff", "#ffffff"]
        color = colors[layer_size % len(colors)]

        circle = plt.Circle((x, y), 0.4, facecolor=color, edgecolor="white",
                             linewidth=1.5, zorder=2, alpha=0.85)
        ax.add_patch(circle)

        label = node_labels[subset]
        fontsize = max(6, 11 - n)
        ax.text(x, y - 0.7, label, ha="center", va="top", fontsize=fontsize,
                color="white", fontweight="bold", zorder=3)

    # Labels for layers
    for layer_idx in range(total_layers):
        # Find y position from first node in layer
        if layers[layer_idx]:
            _, y = positions[layers[layer_idx][0]]
            ax.text(ax.get_xlim()[0] if ax.get_xlim()[0] != 0 else -5, y,
                    f"Size {layer_idx}", fontsize=10, color="#aaaacc",
                    va="center", ha="right")

    ax.set_title(f"Power Set Lattice of {{{', '.join(str(e) for e in elements)}}}\n"
                 f"|P(A)| = 2^{n} = {2**n} subsets",
                 fontsize=14, fontweight="bold", color="white", pad=20)
    ax.set_aspect("equal")
    ax.axis("off")
    plt.tight_layout()
    plt.show()


def plot_cartesian_product(A: set, B: set):
    """Plot a visual representation of the Cartesian product A × B.

    Mathematical idea:
        Cartesian product points are ordered pairs (a, b) with a ∈ A and
        b ∈ B. The plot represents these pairs as points on a grid.

    Formula:
        A × B = {(a, b) | a ∈ A, b ∈ B}, |A × B| = |A| × |B|

    Real-world example:
        Visualizing all possible menu combinations: (drink, main course).
        Each point on the grid is one possible combination.

    Args:
        A: First set.
        B: Second set.
    """
    sorted_a = sorted(A, key=str)
    sorted_b = sorted(B, key=str)

    fig, ax = plt.subplots(figsize=(max(6, len(sorted_a) * 1.5),
                                     max(6, len(sorted_b) * 1.5)))
    fig.patch.set_facecolor("#1a1a2e")
    ax.set_facecolor("#1a1a2e")

    # Color palette for elements of A
    palette = ["#e94560", "#16c79a", "#00d2ff", "#ffa502", "#7c5cff",
               "#ff6bff", "#ff6b6b", "#ffffff"]

    for i, a in enumerate(sorted_a):
        color = palette[i % len(palette)]
        for j, b in enumerate(sorted_b):
            ax.scatter(i, j, color=color, s=200, zorder=3, edgecolors="white",
                       linewidth=1.5)
            ax.annotate(f"({a},{b})", (i, j), textcoords="offset points",
                        xytext=(10, 5), fontsize=9, color="white",
                        fontweight="bold")

    # Gridlines
    ax.set_xticks(range(len(sorted_a)))
    ax.set_xticklabels([str(a) for a in sorted_a], fontsize=12, color="white")
    ax.set_yticks(range(len(sorted_b)))
    ax.set_yticklabels([str(b) for b in sorted_b], fontsize=12, color="white")

    ax.grid(True, color="#333355", linewidth=0.5, alpha=0.5)
    ax.set_xlabel("Set A elements", fontsize=12, color="white", labelpad=10)
    ax.set_ylabel("Set B elements", fontsize=12, color="white", labelpad=10)
    ax.set_title(f"Cartesian Product A × B\n|A × B| = {len(sorted_a)} × {len(sorted_b)} "
                 f"= {len(sorted_a) * len(sorted_b)} pairs",
                 fontsize=14, fontweight="bold", color="white", pad=15)
    ax.tick_params(colors="white")

    plt.tight_layout()
    plt.show()


def plot_warshall_steps(steps: list, elements: list):
    """Plot Warshall's algorithm step-by-step matrices as subplots.

    Mathematical idea:
        Each step k of Warshall's algorithm updates the reachability matrix
        by considering element k as an intermediate node. Visualizing each
        step shows how transitive connections are discovered progressively.

    Formula:
        After iteration k: M[i][j] = M[i][j] OR (M[i][k] AND M[k][j])

    Real-world example:
        In a network routing scenario, each step reveals new routes through
        a specific intermediate router, building up the full routing table.

    Args:
        steps: List of matrices (2D boolean lists), one per k iteration
               plus the initial state. steps[0] = initial, steps[k+1] = after step k.
        elements: Sorted list of unique elements (labels for rows/columns).
    """
    num_steps = len(steps)
    # Determine subplot grid
    cols = min(4, num_steps)
    rows = (num_steps + cols - 1) // cols

    fig, axes = plt.subplots(rows, cols, figsize=(cols * 4, rows * 4))
    fig.patch.set_facecolor("#1a1a2e")

    if num_steps == 1:
        axes = np.array([axes])
    axes = np.array(axes).flatten()

    n = len(elements)

    for idx in range(num_steps):
        ax = axes[idx]
        ax.set_facecolor("#1a1a2e")

        matrix = np.array(steps[idx], dtype=int)

        # Determine newly added cells (compare with previous step)
        if idx > 0:
            prev_matrix = np.array(steps[idx - 1], dtype=int)
            new_cells = (matrix - prev_matrix) > 0  # True where new
        else:
            new_cells = np.zeros_like(matrix, dtype=bool)

        # Create a colored matrix: 0=dark, 1=green, 2=cyan(new)
        display = np.zeros_like(matrix, dtype=int)
        display[matrix == 1] = 1
        display[new_cells] = 2

        cmap = plt.cm.colors.ListedColormap(["#1a1a2e", "#16c79a", "#00d2ff"])
        bounds = [-0.5, 0.5, 1.5, 2.5]
        norm = plt.cm.colors.BoundaryNorm(bounds, cmap.N)

        ax.imshow(display, cmap=cmap, norm=norm, aspect="equal")

        # Labels
        str_elems = [str(e) for e in elements]
        ax.set_xticks(range(n))
        ax.set_xticklabels(str_elems, fontsize=8, color="white")
        ax.set_yticks(range(n))
        ax.set_yticklabels(str_elems, fontsize=8, color="white")

        # Cell text
        for i in range(n):
            for j in range(n):
                color = "#1a1a2e" if matrix[i][j] else "#444466"
                ax.text(j, i, str(matrix[i][j]), ha="center", va="center",
                        fontsize=10, fontweight="bold", color=color)

        if idx == 0:
            ax.set_title("Initial", fontsize=10, color="white", fontweight="bold")
        else:
            ax.set_title(f"Step k={idx - 1}", fontsize=10, color="white",
                         fontweight="bold")

    # Hide unused subplots
    for idx in range(num_steps, len(axes)):
        axes[idx].set_visible(False)

    fig.suptitle("Warshall's Algorithm — Step-by-step Transitive Closure",
                 fontsize=14, fontweight="bold", color="white", y=1.02)
    plt.tight_layout()
    plt.show()
