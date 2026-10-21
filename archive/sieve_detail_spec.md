# Sieve Demonstration Tool v3.0: Periodic Anti-Node Visualizer

This document details the architectural and mathematical principles behind the next-generation sieve visualization tool created in [`sieves_v3.html`](sieves_v3.html).

---

## 1. Core Visualizer Taxonomy

To align with the upstream specification, the visualization distinguishes between the following classes:

| Class | Math Definition | Description & Sieve Behavior |
| :--- | :--- | :--- |
| **Primes** | $\Omega(n) = 1$ | Confirmed primes within the *Quadratic Guarantee* interval $[1, p_{n+1}^2)$. |
| **Anti-Nodes** (RRS) | $\gcd(n, P_n\#) = 1$ | Gaps remaining in the residue system. These are potential primes/rough composites. |
| **Semiprimes** | $\Omega(n) = 2$ | Composite numbers formed by exactly two prime factors (e.g., $6, 10, 15$). |
| **k-Almost Primes** | $\Omega(n) \ge 3$ | Higher-order composites representing multi-prime intersection nodes. |
| **Nodes** (Multiples) | $\gcd(n, P_n\#) > 1$ | Points of periodic wave alignment (the multiples of active primes). |

---

## 2. Key Visualizations Implemented

We have implemented the following core visualizations in [`sieves_v3.html`](sieves_v3.html):

### A. Dynamic Interference Grid
* **Visual Representation:** Cells are colored using high-fidelity dark-mode HSL gradients mapped to their mathematical taxonomy (Primes, Semiprimes, $k$-Almost Primes, Nodes, and Anti-Nodes).
* **Interactive Inspector:** Hovering or clicking a cell dynamically calculates the **Divisor Function** $d(n)$, the **Prime Factorization count** $\Omega(n)$, the prime factors, the modulo class, and checks whether the element falls under the **Quadratic Guarantee** range.

### B. Wave Interference Tab
* **Square Waveforms:** Renders the periodic multiples of the chosen sieve primes as overlapping waveforms on a canvas.
* **Residue Gaps:** Displays the Master **Reduced Residue System (RRS)** timeline at the bottom, visually showing how "troughs" (gaps) in the overlapping periodic waves correspond to surviving anti-nodes.

### C. Symmetry & Sub-Cycles Tab
* **Palindromic Symmetry:** Verifies and visually pairs RRS elements symmetrically around the midpoint $P_n\# / 2$, demonstrating that if $x$ is an anti-node, then $P_n\# - x$ is also an anti-node.
* **Sub-Periodicity & Rotational Deletion:** Maps nested cycles (e.g., how the $30$-period sieve contains $5$ sub-cycles of the $6$-period sieve), showing the rotational deletion where the latest prime deletes exactly one anti-node per sub-period.

### D. Moduli Analysis & Mutations
* **Remainder Classes:** Breaks down residue class distributions modulo 3 ($3n+1$ vs $3n+2$) and modulo 4.
* **Pattern Mutations:** Displays real-time percentages and bar charts showing how the distribution of gaps shifts and mutates as the primorial width expands.

---

## 3. How to Launch and View
You can run a local server or directly open [`sieves_v3.html`](sieves_v3.html) in any modern web browser to interact with the visualizer.
