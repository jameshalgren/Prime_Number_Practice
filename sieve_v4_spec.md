# Sieve Visualizer v4.0 Specification

This document details the visual and mathematical specification for version 4.0 of the Sieve Demonstration Tool.

## 1. Core Visual Concept: Strikeout Lines & Interference
Instead of static cell colors, v4.0 uses **continuous overlay lines (polylines)** representing the "strikeouts" of numbers $p$.

* **Oblique Alignment:** Connecting multiples $p \to 2p \to 3p \to \dots$ creates diagonal lines.
* **No Horizontal Lines:** To preserve clean visual channels, any wrap-arounds that result in a purely horizontal transition (same-row steps) are skipped/broken, partitioning the strikeouts into parallel diagonal columns.
* **Last Column Vertical Rule:** With each increase in grid width $W$, a vertical line populates down the last column (Column $W$), representing the strikeout of all multiples of $W$ ($W, 2W, 3W, \dots$). All other lines slide and tilt dynamically.
* **Primal vs Non-Primal Strikeout Overlap & Line Strength (Issue #3):** 
  * A user toggle allows toggling non-prime strikeouts (e.g., $4, 6, 8, 9, 10, 12 \dots$).
  * When **Only Prime Strikeouts** are selected, lines are drawn with single standard thickness per prime.
  * When **Non-Prime Strikeouts** are enabled, composite numbers also emit strikeout lines along their prime factor paths. This causes multi-factor composite nodes (e.g., 6, which overlaps 2, 3, and 6) to accumulate overlapping lines, multiplying line strength/thickness proportionally to their degree of non-primalness ($\Omega(n)$).

---

## 2. Interactive UI Capabilities
* **Sieve Length Slider:** Instantly controls the maximum number of cells in the grid.
* **Grid Width Slider:** Instantly controls the number of columns, shifting the cell positions and migrating the strikeout lines.
* **Line Width Slider:** Controls the base stroke thickness of the overlay lines.
* **Non-Prime Strikeout Toggle:** Checkbox to toggle non-prime composite strikeout paths and trigger multi-factor line strength stacking.
* **Responsive Scrolling:** Grid cells have a fixed size ($45\text{px} \times 45\text{px}$), allowing the container to naturally expand/contract and show scrollbars when necessary.

---

## 3. Mathematical Principles & Clarifications
1. **Last Column Multiples:** In a grid of width $W$, cells $W, 2W, 3W, \dots$ always align vertically in column $W-1$ (0-indexed). This creates a stationary vertical channel for grid-width multiples.
2. **Multi-Factor Line Strength Stacking:** When composite strikeouts are enabled, the visual weight of line paths through number $n$ grows proportionally to its prime factor count $\Omega(n)$ and divisor structure, visually revealing the degree of non-primalness.

---

## 4. v4.2: The Period-Locked Stripe Algorithm

Earlier drafts (v4.1) tried to fix "too oblique / near-horizontal" lines by splitting a connecting segment at the grid's left/right seam whenever it exceeded a fixed obliquity threshold. That approach was abandoned — verified against live testing to be both geometrically wrong (the split stubs were themselves flat) and conceptually wrong (it treated obliquity capping as a per-segment patch rather than a property of the period itself).

### 4.1 The real rule

Connecting *immediate* consecutive multiples of a period $p$ forces a column shift of exactly $p - W$ on every row-crossing transition (this is mathematically forced, not a stylistic choice — see §4.3). For $p \le W/2$, $|p - W| > p$, i.e. the line is *more oblique than the period's own value* — exactly the near-horizontal artifact that kept coming up.

**The fix:** connect every $k$-th multiple of $p$ instead of every multiple, where

$$k = \max\left(1, \left\lfloor \frac{W}{p} \right\rfloor\right)$$

Each of the $k$ starting phases ($p, 2p, \dots, kp$) is walked independently using stride $S = kp$. This single formula unifies every case:

* **If $p$ divides $W$ exactly:** $k = W/p$ and $S = kp = W$, i.e. each phase is a pure *vertical* line — and there are $k$ of them, one per residue $p, 2p, \dots, kp$. This generalizes the old single "last column" case (which is just $p = W$, $k=1$) to *every* divisor of $W$: e.g. the "2" strikeout is vertical (as two, four, or more parallel lines) at every even width, and "3" is vertical at every width that's a multiple of 3.
* **Otherwise:** $k = \lfloor W/p \rfloor$ is guaranteed to keep the resulting shift $|kp - W|$ strictly smaller than $p$ — satisfying "never more oblique than the period's own value." For example, period 5 in a 9-wide grid: $k=1$, shift $-4$, already under the cap of 5, so it stays a direct 4:1 diagonal. Period 2 in a 5-wide grid: $k=2$, shift $-1$ (vs. the uncapped $k=1$ shift of $-3$).

### 4.2 Candy-striping

Within a single phase, a "row that doesn't advance" is still possible near the column seam — this breaks the phase into separate visible line segments ("candy stripes") rather than ever drawing a flat horizontal line, preserving the original "no horizontal lines" rule. Verified example, period 2 in a 5-wide grid, values 1–30:

```
phase p*1=2, stride 4: [2, 6] | [10, 14, 18, 22, 26]
phase p*2=4, stride 4: [4, 8, 12, 16] | [20, 24, 28]
```

### 4.3 Default slope direction

For $p < W$, a row-crossing transition's column shift is *mathematically forced* to be negative (ascending "/" — lower-left to upper-right when read top-to-bottom) — there is no free stylistic choice for the common case. A future "minimize slope" toggle could flip specific transitions to "\" when that direction is shallower still (deferred; see §6).

### 4.4 Vertical is plural

When $p$ divides $W$, "vertical" means $k = W/p$ *separate* parallel vertical lines (one per residue), not a single line — this is required to accurately show every struck cell, not just a representative one.

---

## 5. Persistent Color System

* **Fixed prime color identity:** colors are assigned by each prime's position in a *fixed* global list (primes up to the width slider's maximum, 30), not by position within whatever subset of primes happens to be active at the current width. This is what keeps "7 is purple, 3 is gold, 5 is orange" stable as the width slider changes the *set* of primes being struck out.
* **Composite color modes:** composites (only relevant once non-prime strikeouts are shown) default to inheriting their smallest prime factor's color ("family" mode — hue shows which prime family a node belongs to; thickness, scaled by $\Omega(n)$, shows how composite it is). A toggle switches to "individual" mode, giving each composite its own persistent identity color instead.
* **Last-column emphasis:** the multiples-of-$W$ line — the grid's own defining period — uses whatever persistent color its value $W$ would use anywhere else (not a hardcoded highlight color), drawn at emphasized (thicker) weight so the current width's defining period stays easy to spot.

---

## 6. Width-Driven Strikeout Selection

The default (and, for now, only) behavior: the sieve strikes out exactly the primes $p \le W$ — the primes that appear at least once in row 0 — rather than primes $\le \sqrt{N}$. This set grows and shrinks as the width slider moves; a prime only gets a strikeout line once the grid is at least that wide. Non-prime strikeouts (when toggled on) follow the same bound: composite periods $4 \le k \le W$.

A deferred **"Set Strikeout Max"** control would let a user extend the strikeout set beyond $W$ (e.g. include a specific larger prime, or a hand-picked list of periods, "specified below the sieve"). Not yet implemented — the default ($p \le W$) needed to be validated first.

---

## 7. Rendering polish (v4.2 follow-up)

1. **Edge-to-edge line rendering (done):** every drawn stripe's first segment is extrapolated up to the sieve's true top edge ($y=0$), and its last segment down to the sieve's true bottom edge ($y = \lceil N/W \rceil \times \text{cellSize}$), rather than stopping at the center of its first/last struck cell. Since every period $p \le W$ has its first multiple in row 0 by construction, the "extend to top" case always applies.
2. **Zoom / scroll (done):** `html, body` now use a fixed `height: 100%` instead of `min-height: 100vh` — the earlier CSS let the page grow to fit the grid instead of constraining the workspace, so the workspace's own `overflow: auto` never actually triggered a scrollbar, hiding any content below the viewport with no way to reach it. A Zoom slider now also controls cell size directly (via a `--cell-size` CSS variable), independent of scrolling.

## 8. v4.3: Zoom-Driven Legibility & the Partial-Sieve Boundary

* **Text scales with zoom:** cell font size is `clamp(6px, cellSize * 0.32, 22px)`, tracking the same `--cell-size` CSS variable the Zoom slider already drove — legible whether zoomed in to inspect a few rows or zoomed out to see large-scale pattern structure.
* **Stronger prime highlighting:** `.prime-origin` cells now use a brighter fill, bolder text color, and an inset border, making primes easier to pick out at a glance (previously a faint background tint only).
* **Sieve Length raised to 5,000** (from 600) now that zooming out makes larger-scale patterns visible. Empirically, rendering 5,000 DOM cells takes roughly 50ms — comfortably interactive. See §9 for the path beyond this.
* **Rough-composite highlighting — the partial-sieve boundary:** for a strikeout set limited to primes $\le W$, every composite $i < \text{nextPrime}^2$ (nextPrime = the first prime beyond $W$, i.e. the first prime appearing in row 2) is *guaranteed* struck out, since its smallest prime factor is $\le \sqrt{i} < \text{nextPrime} \le W$. At $i = \text{nextPrime}^2$ itself that guarantee first fails (e.g. $i=25=5^2$ when $W=3$: $25$'s only prime factor is $5$, which exceeds $W$). Composites at or beyond this boundary whose smallest prime factor exceeds $W$ are flagged with a distinct amber highlight — they are not prime, but the currently-drawn strikeout lines haven't caught them. These are **rough numbers** in the standard sieve-theory sense (a $y$-rough number has no prime factor $< y$); highlighting the composite ones makes visible exactly what a *partial* sieve has missed, which is the experiment's whole pedagogical point — not just "here are the primes," but "here is what remains ambiguous until the sieve is extended far enough."

## 9. On Maximum Feasible Size / Scaling to N > 1,000,000 (parked)

The current architecture creates one real DOM element per number. That's the actual ceiling, not canvas drawing — a few thousand DOM nodes plus a full rebuild on every slider tick stays comfortably interactive (~50ms at N=5,000); tens of thousands would visibly lag; millions of DOM nodes would be unusable regardless of how simple each node is. Canvas line-drawing itself is comparatively cheap and could plausibly handle tens of thousands of stroked segments per frame without being the bottleneck.

Reaching $N > 10^6$ requires an architecture change, parked for later:
* Render numbers and gridlines entirely on canvas — no per-cell DOM nodes at all.
* **Virtualize**: only compute and draw the rows currently within the scrolled viewport (plus a small buffer), recomputing as the user scrolls — the same technique a spreadsheet or map tile-loader uses. Strikeout lines would need to be computed as ray/segment intersections with the visible viewport rectangle rather than walked cell-by-cell from $1$.
* At extreme scale, prime-checking itself would want a precomputed sieve (typed array bitset) rather than trial division per cell.

## 10. PARKED: Non-Prime (Composite) Strikeout Piggyback Model — pick up here

Explicitly paused mid-design (per user: "Hold on the composite strikeouts") in favor of 4 unrelated dashboard/UI features (§11). **Resume here, not from scratch.**

### Confirmed so far
* Composites should **not** get independent `k = floor(W/k)` geometry (today's behavior). This only applies to *non-prime* strikeouts — prime-only strikeout rendering is unaffected and already correct/validated.
* **Prime powers** (4, 8, 9, 25, ...): unambiguous, single possible host. Ride exactly on the base prime's existing line geometry (same phases, same stride); mark the composite's own multiples with extra thickness. E.g. 4 always uses 2's exact stripe shape.
* **Multi-distinct-prime-factor composites** (6, 10, 12, 15, ...): ride on **all** distinct prime factors simultaneously (not a single chosen host) — e.g. 6 rides on both 2's geometry and 3's geometry at once.

### Worked example that needs to be reconciled (unresolved)
User's description of the "6" strikeout across widths 6, 7, 8:
* **W=6, W=7:** a "triple-wide" strikeout — the prime-3 line, plus 2's and 3's contributions to 6, all coincide into one stacked line (diagonal at W=7, vertical/last-column at W=6).
* **W=8:** a double-wide strikeout down the vertical "6" column (since 2 is fully vertical at W=8), **plus separately** a double-wide strikeout along the oblique 3-strikeout line.

I verified the W=6/W=7 triple-coincidence numerically (2's and 3's phase that starts exactly at value 6 produce the identical point sequence 6,12,18,... in both cases, because at those widths `floor(W/2)*2 == floor(W/3)*3 == 6`). That part checks out.

**The discrepancy:** at W=8, I computed that riding on 2 (fully vertical there) only lets you mark *isolated points* (6, 30, 54, ... — every 3rd point on that vertical, spaced by `lcm(6,8)=24`), not a continuous doubled line-segment, since no two *consecutive* points on 2's stride-8 vertical are both multiples of 6. Riding on 3 does give a genuine continuous run (6→12→18 is a real diagonal chain of true multiples of 6). This was the open question posed back to the user (not yet answered): does "double-wide strikeout in a vertical line down the 6 column" mean isolated doubled points are the expected/correct visual, or is there a different intended geometry?

### Still completely unaddressed
* How the future reduced-obliquity ("\\" flip) toggle interacts with composite piggybacking at all — user stated explicitly this hasn't been thought through yet.
* Exact visual treatment of "double/triple emphasis" (thickness scale factor vs. a second overlay color) — not yet decided.

---

## 11. v4.4: Dashboard, Factor Disclosure, Anchor Circles, Adjustable Strikeout Max

* **Info dashboard:** a compact, small-font bar under the header showing, for the *grid width* $W$ (deliberately independent of the strikeout max — see below): the largest prime $\le W$ and its primorial; the next prime beyond $W$ and its primorial; and a **"Next-prime square"** figure — the square of the next prime *above the active strikeout set* (so this one tracks Max Strikeout Value, not $W$ directly; the two coincide whenever locked). Labeled with the subtext "(sieve is guaranteed-complete up to this value)". Clicking that figure scrolls the grid to that cell.
* **Factor disclosure:** rough-composite cells (§8) get a `title` tooltip showing their full prime factorization (e.g. "35 = 5 × 7"), so hovering a flagged "dirty number" shows *why* it's composite even though nothing has struck it out yet.
* **Anchor (keyhole) circles:** every actively-struck, top-row prime ($p \le \min(W, \text{maxStrikeout})$) gets a ring drawn in its own persistent color around its cell. The prime's own strikeout line does **not** pass through the circle: the first segment of that prime's line starts at the circle's boundary (computed via `pointAtDistance`) rather than at the cell center, and the top-edge extension (§7) is skipped for that specific segment — a "keyhole," so the prime's own number is never visually struck by its own line. Only scoped to $p \le W$ for now (§12 item 5 tracks the $p > W$ case).
* **Adjustable Max Strikeout Value:** a new slider (range matches the width slider, 2–30) plus a "Lock to Grid Width" checkbox (default checked). Locked, it silently tracks $W$ (today's default behavior, unchanged). Unlocking — either via the checkbox or by directly dragging the slider itself — decouples it, so the strikeout *set* (which primes/composites get lines, and where the rough-composite boundary falls) can be explored independently of the grid's own layout. This is what §6's deferred "Set Strikeout Max" became.
* Noted for later: a text box for arbitrary numeric entry (rather than only a bounded slider), and/or widening the slider's own range, are both open possibilities, not yet built. Also noted: the dashboard could eventually show *both* the $W$-based and strikeout-set-based figures side by side, rather than picking one.

---

## 12. Deferred / Future Work

1. ~~**Set Strikeout Max UI**~~ — implemented, see §11 (Max Strikeout Value slider + lock toggle).
2. **Minimize-slope / reduced-obliquity toggle** (§4.3) — per-period choice of "\" over "/" when it's actually shallower, for readability at large $W$ and large primes. Prioritized *ahead of* animated width transitions per user direction, but itself now blocked behind resolving the composite piggyback model (§10).
3. **Fractional Sieves / Smooth Animation:** smooth, continuous sliding transitions as $N$ or $W$ change, while still only ever displaying integer cross-outs at rest — i.e. animating between two valid integer grid states (interpolating cell position and line geometry) rather than supporting truly fractional widths. Deferred as its own follow-up given the scope (continuous-width cell layout + a redraw loop synced to the animation, rather than the current instant-redraw-on-slider-input model), and now ordered *after* the reduced-obliquity feature.
4. **N > 1,000,000 rendering** (§9) — canvas-only, virtualized rendering; parked.
5. **Strikeout periods greater than the grid width:** now reachable in practice since Max Strikeout Value can be unlocked and set above $W$ (§11). A prime $p > W$ no longer originates in row 0, so today's anchor-circle scoping (only primes $\le W$ get a keyhole circle) and the "every phase's first point is in row 0" assumption behind edge-extension (§4, §7) don't yet cover this case. Anchor circles and edge-extension both currently degrade gracefully (no crash, just no circle / an odd extrapolation) rather than being actively designed for it — needs its own pass once picked up.
6. **Text-entry / wider-range control for Max Strikeout Value** (§11) — noted by the user as a later possibility, not yet built.
7. **Dual-basis dashboard** (§11) — show both $W$-based and strikeout-set-based primorial/boundary figures at once, rather than only $W$-based.
8. **Grade rough-composite ("dirty number") highlighting by $\Omega(n)$ or near-primeness:** today every rough composite (§8) gets the same flat amber highlight regardless of how composite it actually is. Distinct from the *already-implemented* $\Omega(n)$-scaled thickness for composite strikeout *lines* (§5, for numbers that already have a line drawn through them) — this would instead grade the *unstruck* "dirty" numbers themselves, e.g. semiprimes ($\Omega=2$) shown differently from $k$-almost-primes ($\Omega \ge 3$), so a rough number's degree of compositeness is visible even before any line ever reaches it. Not yet designed (color gradient? border weight? a small $\Omega(n)$ badge alongside the existing factor-disclosure tooltip?) — checked against the prompt log and not something previously specified, so starting fresh here rather than assuming a prior design.
