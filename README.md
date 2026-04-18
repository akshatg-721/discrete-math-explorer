# Discrete Mathematics Explorer

## Project Description

Discrete Mathematics Explorer is a Python CLI application scaffold focused on foundational set theory and relation concepts.  
This phase contains structure and documentation-only stubs for implementation planned before the submission deadline.

## Tech Stack

- Python
- matplotlib
- matplotlib_venn
- itertools
- Python standard library

## Installation

1. Ensure Python 3.10+ is installed.
2. Navigate to the project directory:

```bash
cd discrete-math-explorer
```

3. Install dependencies:

```bash
pip install matplotlib matplotlib-venn
```

## How to Run

The CLI entry point will be:

```bash
python main.py
```

At this scaffold stage, `main.py` only includes the planned menu structure as comments.

## Folder Structure

```text
discrete-math-explorer/
├── main.py
├── sets.py
├── relations.py
├── visualizer.py
├── tests/
│   ├── test_sets.py
│   └── test_relations.py
└── README.md
```

## The Math Behind It

### Set Operations

- Parse set:
  - \( A = \{x \mid x \text{ appears in cleaned input}\} \)
- Union:
  - \( A \cup B = \{x \mid x \in A \text{ or } x \in B\} \)
- Intersection:
  - \( A \cap B = \{x \mid x \in A \text{ and } x \in B\} \)
- Difference:
  - \( A - B = \{x \mid x \in A \text{ and } x \notin B\} \)
- Symmetric Difference:
  - \( A \triangle B = (A - B) \cup (B - A) \)
- Subset:
  - \( A \subseteq B \iff \forall x (x \in A \Rightarrow x \in B) \)
- Power Set:
  - \( \mathcal{P}(A) = \{S \mid S \subseteq A\} \)
  - \( |\mathcal{P}(A)| = 2^{|A|} \)
- Cartesian Product:
  - \( A \times B = \{(a,b) \mid a \in A, b \in B\} \)
  - \( |A \times B| = |A| \cdot |B| \)

### Relations

- Relation from \( A \) to \( B \):
  - \( R \subseteq A \times B \)
- Reflexive (on \( A \)):
  - \( \forall a \in A,\ (a,a) \in R \)
- Symmetric:
  - \( \forall a,b,\ (a,b) \in R \Rightarrow (b,a) \in R \)
- Antisymmetric:
  - \( \forall a,b,\ ((a,b) \in R \land (b,a) \in R) \Rightarrow a=b \)
- Transitive:
  - \( \forall a,b,c,\ ((a,b) \in R \land (b,c) \in R) \Rightarrow (a,c) \in R \)
- Equivalence Relation:
  - Reflexive + Symmetric + Transitive
- Total number of possible relations from \( A \) to \( B \):
  - \( 2^{|A|\cdot|B|} \)

## Planned CLI Menu

1. Set Operations
2. Power Set Generator
3. Cartesian Product
4. Relation Builder and Property Checker
5. Visualizations
6. Real World Applications (extra feature)
7. Exit

## Notes

- This scaffold intentionally contains function signatures, docstrings, and mathematical comments only.
- No computational logic has been implemented in this stage.
