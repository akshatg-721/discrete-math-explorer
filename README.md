# 🧮 Discrete Mathematics Explorer

<div align="center">

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Tests](https://img.shields.io/badge/Tests-68%20Passed-4ade80?style=for-the-badge&logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-a29bfe?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Complete-00b894?style=for-the-badge)

**A Python CLI application that brings Discrete Mathematics to life — through working code, step-by-step algorithms, and interactive visualizations.**

*Set Theory · Cartesian Products · Relations · Warshall's Algorithm · Graph Reachability*

</div>

---

## 📌 Overview

Discrete Mathematics Explorer is a fully working, tested Python CLI application implementing core Discrete Mathematics concepts. Every mathematical concept is explicitly connected to its algorithm and its code — with real-world interpretations for each feature.

Built as a university Discrete Mathematics project, it goes significantly beyond the base requirements with named algorithms, step-by-step matrix traces, and applied real-world demonstrations.

---

## ✨ Features

### Core Features
| Feature | Description | Formula |
|---|---|---|
| **Set Operations** | Union, Intersection, Difference, Symmetric Difference, Subset | A ∪ B, A ∩ B, A − B, A △ B |
| **Power Set Generator** | All possible subsets of a set | \|P(A)\| = 2ⁿ |
| **Cartesian Product** | Every ordered pair (a, b) from two sets | \|A × B\| = \|A\| × \|B\| |
| **Relation Builder** | Build relations from Cartesian product, check all 5 properties | R ⊆ A × B |
| **Relation Counter** | Count all possible relations between two sets | 2^(\|A\|×\|B\|) |

### Relation Properties Checked
- ✅ **Reflexive** — ∀a ∈ A: (a, a) ∈ R
- ✅ **Symmetric** — (a,b) ∈ R → (b,a) ∈ R
- ✅ **Antisymmetric** — (a,b) ∈ R ∧ (b,a) ∈ R → a = b
- ✅ **Transitive** — (a,b) ∈ R ∧ (b,c) ∈ R → (a,c) ∈ R
- ✅ **Equivalence** — Reflexive + Symmetric + Transitive

### Extra Features (Beyond Spec)
| Feature | Description |
|---|---|
| **Warshall's Algorithm** | Computes transitive closure with full step-by-step matrix trace at every intermediate vertex k — O(n³) |
| **Relation Composition (R ∘ S)** | If (a,b) ∈ R and (b,c) ∈ S then (a,c) ∈ R∘S — the mathematical foundation of SQL JOINs |
| **Equivalence Class Partitioner** | Automatically groups elements into equivalence classes for valid equivalence relations |
| **Social Network Influence Demo** | Models a follower graph, applies Warshall's to find indirect reach, identifies most influential node |

### Visualizations
- 🔵 **Venn Diagram** — Set operations with matplotlib-venn
- 🟩 **Relation Matrix Heatmap** — 0/1 boolean matrix with labeled axes
- 🌳 **Power Set Tree** — Layered branching diagram of all subsets
- 📍 **Cartesian Product Grid** — Scatter plot of all (a, b) pairs
- 🔄 **Warshall Step Matrices** — Sequence of heatmaps showing algorithm progress per k step

---

## 🧠 The Math Behind It

### Set Operations
A ∪ B = {x | x ∈ A or x ∈ B}
A ∩ B = {x | x ∈ A and x ∈ B}
A − B = {x | x ∈ A and x ∉ B}
A △ B = (A − B) ∪ (B − A)

### Power Set
For a set A with n elements, the power set P(A) contains every possible subset:
|P(A)| = 2ⁿ
**Why 2ⁿ?** For each element, you independently choose to include it or not — 2 choices × n elements → 2ⁿ total subsets.

### Cartesian Product & Relations
A × B = {(a, b) | a ∈ A, b ∈ B}
|A × B| = |A| × |B|
Number of possible relations = 2^(|A| × |B|)

### Warshall's Algorithm — Transitive Closure
Finds all pairs (i, j) where j is reachable from i, directly or through any chain:

```python
for k in range(n):           # intermediate vertex
    for i in range(n):
        for j in range(n):
            M[i][j] = M[i][j] or (M[i][k] and M[k][j])
```

**Time Complexity:** O(n³)

**Intuition:** For each possible "middle stop" k — if you can go i→k AND k→j, mark i→j as reachable. The matrix prints after every k step so you see the algorithm thinking in real time.

### Relation Composition
(a, c) ∈ R∘S  ⟺  ∃b : (a,b) ∈ R  ∧  (b,c) ∈ S
**Real world:** R = "enrolled in" (Students → Courses), S = "taught by" (Courses → Professors) → R∘S = Students → Professors directly. This is the mathematical foundation of SQL JOINs.

---

## 🚀 Getting Started

### Prerequisites
```bash
python3 --version   # 3.8 or higher required
```

### Install Dependencies
```bash
pip install matplotlib matplotlib-venn pytest
```

### Run
```bash
git clone https://github.com/akshatg-721/discrete-math-explorer.git
cd discrete-math-explorer
python3 main.py
```

### Run Tests
```bash
python3 -m pytest tests/ -v
```

---

## 📁 Project Structure
discrete-math-explorer/
├── main.py               # CLI entry point — 7-option menu
├── sets.py               # All set operations (9 functions)
├── relations.py          # Relations + Warshall's (10 functions)
├── visualizer.py         # matplotlib visualizations (5 plots)
├── tests/
│   ├── test_sets.py      # 34 test cases
│   └── test_relations.py # 34 test cases
└── README.md

---

## 🖥️ CLI Menu
═══════════════════════════════════════════════════════
🧮  DISCRETE MATHEMATICS EXPLORER
A comprehensive CLI for set theory & relations
═══════════════════════════════════════════════════════

Set Operations (∪, ∩, -, △, ⊆)
Power Set Generator (P(A) = 2ⁿ)
Cartesian Product (A × B)
Relation Builder + Property Checker
Visualizations (Venn, Matrix, Tree, Grid)
Advanced (Warshall, Composition, Equivalence)
Exit
───────────────────────────────────────────────────────
Option 6 sub-menu:
6a. Warshall's Algorithm (Step-by-Step Transitive Closure)
6b. Relation Composition (R ∘ S)
6c. Equivalence Class Partitioner
6d. Social Network Influence Demo


---

## ✅ Test Results
68 passed in 0.10s
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
tests/test_sets.py        34 passed
tests/test_relations.py   34 passed

---

## 🌍 Real World Applications

| DM Concept | Real World Application |
|---|---|
| Sets | Database tables, tag systems, search filters |
| Cartesian Product | SQL JOIN operations, coordinate systems |
| Relations | Social graphs, access control, scheduling |
| Transitive Closure | Network reachability, GPS routing, influence analysis |
| Equivalence Classes | Grouping, clustering, partitioning |
| Relation Composition | Multi-hop queries, indirect connections |

---

## 👨‍💻 Author

**Akshat Goyal** — B.Tech CSE · BML Munjal University
[GitHub](https://github.com/akshatg-721)

---

## 📄 License

Restricted