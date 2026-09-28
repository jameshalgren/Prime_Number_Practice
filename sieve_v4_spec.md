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
2. **Minimize-slope / reduced-obliquity toggle** (§4.3) — now planned, see §13.5. Original note: per-period choice of "\" over "/" when it's actually shallower, for readability at large $W$ and large primes. Prioritized *ahead of* animated width transitions per user direction, but itself now blocked behind resolving the composite piggyback model (§10).
3. **Fractional Sieves / Smooth Animation:** smooth, continuous sliding transitions as $N$ or $W$ change, while still only ever displaying integer cross-outs at rest — i.e. animating between two valid integer grid states (interpolating cell position and line geometry) rather than supporting truly fractional widths. Deferred as its own follow-up given the scope (continuous-width cell layout + a redraw loop synced to the animation, rather than the current instant-redraw-on-slider-input model), and now ordered *after* the reduced-obliquity feature.
4. **N > 1,000,000 rendering** (§9) — canvas-only, virtualized rendering; parked.
5. **Strikeout periods greater than the grid width:** now reachable in practice since Max Strikeout Value can be unlocked and set above $W$ (§11). A prime $p > W$ no longer originates in row 0, so today's anchor-circle scoping (only primes $\le W$ get a keyhole circle) and the "every phase's first point is in row 0" assumption behind edge-extension (§4, §7) don't yet cover this case. Anchor circles and edge-extension both currently degrade gracefully (no crash, just no circle / an odd extrapolation) rather than being actively designed for it — needs its own pass once picked up.
6. **Text-entry / wider-range control for Max Strikeout Value** (§11) — noted by the user as a later possibility, not yet built.
7. **Dual-basis dashboard** (§11) — show both $W$-based and strikeout-set-based primorial/boundary figures at once, rather than only $W$-based.
8. **Grade rough-composite ("dirty number") highlighting by $\Omega(n)$ or near-primeness:** today every rough composite (§8) gets the same flat amber highlight regardless of how composite it actually is. Distinct from the *already-implemented* $\Omega(n)$-scaled thickness for composite strikeout *lines* (§5, for numbers that already have a line drawn through them) — this would instead grade the *unstruck* "dirty" numbers themselves, e.g. semiprimes ($\Omega=2$) shown differently from $k$-almost-primes ($\Omega \ge 3$), so a rough number's degree of compositeness is visible even before any line ever reaches it. Not yet designed (color gradient? border weight? a small $\Omega(n)$ badge alongside the existing factor-disclosure tooltip?) — checked against the prompt log and not something previously specified, so starting fresh here rather than assuming a prior design.

---

## 13. v4.5 Plan (Prompt 22) — not yet implemented

Proposed build order (each step checked with `tests/visual_check.js` before moving on):

### 13.1 Click-to-edit slider values
Clicking the number shown above any slider (Sieve Length, Grid Width, Line Width, Zoom, Max Strikeout) turns it into an integer text box. Enter or blur commits, Escape cancels. The value is clamped to the slider's own min/max, then the normal `input` path runs, so a typed Max Strikeout still unlocks it (§11). This also covers §12.6 (text entry for Max Strikeout).

### 13.2 Dashboard additions
* **Smallest primorial greater than W:** the smallest $P\#$ with $P\# > W$. Examples: $W=7 \to 30$, $W=30 \to 210$, $W=210 \to 2310$. This is the next width that "multiplies all the available simple primes," i.e. the next width at which every smaller prime's line is vertical. It is shown next to the existing Primorial($p \le W$) and next-prime primorial figures.
* **Prime factorization of W:** e.g. $360 = 2^3 \cdot 3^2 \cdot 5$. Widths built from small primes ($6, 12, 30, 60, 120, 180, 210, 360, \dots$) show noticeably organized prime patterns, so W's factorization should always be visible.
* **BigInt:** all primorial figures are computed as `BigInt`. Plain JS numbers lose precision above $2^{53}$, which primorials pass at $53\#$. Very large values are shown abbreviated (e.g. `≈3.26e19`, with the full digits in a tooltip).

### 13.3 Renderer rewrite for widths up to several thousand (pulls in §9)
**Deferred (Prompt 25):** the current DOM renderer was measured at W = 2160 ($2^4 \cdot 3^3 \cdot 5$): about 90 ms per redraw at N = 20,000, about 440 ms at 50,000, and 1.2–2.1 s at 100,000, with no errors and lines drawn at every zoom tested. The lag comes from sieve length N (one DOM cell per number), not width. That is acceptable for now, so the width and Max Strikeout slider limits were raised to 2160 without a rewrite, and 13.4 was built first. Note: browser canvas-size limits (canvas width is W × cell size) may still blank the lines on some browsers at high zoom with large W.

The DOM-cell grid already struggles with long sieves, and the browser also limits canvas size (roughly 16k–32k px per side, and a total-area cap). Widths in the thousands need:
* Cells drawn on a canvas instead of one DOM element per number. Numbers are only drawn as text when the cell size is large enough to read; otherwise cells are color-only.
* A **viewport-sized canvas**: only the currently visible rows and columns (plus a small margin) are drawn, and redrawn on scroll. An oversized spacer element provides the scrollbars. Strikeout lines are clipped to the visible area rather than walked from 1 to N.
* A precomputed prime / smallest-prime-factor table (typed array) instead of trial-division `isPrime` per cell.
* Hover tooltips (factorization, §11) done by hit-testing the mouse position against the grid, since there are no longer DOM cells to carry a `title`.
* Colors for primes beyond 29 (`PRIME_COLOR_ORDER` is fixed at 10 primes): switch to a generated hue per prime index so large primes don't repeat colors as much.
Doing this before 13.4/13.5 means cell shading and the slope rule are built once, on the new renderer.

### 13.4 Strikeout-line toggle + Ω grading (includes §12.8) — implemented
Implemented in `index.html`: "Show Strikeout Lines" (default on; off also hides the anchor circles) and "Grade Unstruck Composites by Ω" (default off). Verified at Max Strikeout = 2, N = 120: amber 9, 15, 21, 25, 33, …; red 27, 45, 63, 75, 99, 105, 117; purple 81; nothing drawn on the canvas with lines off. Built order is now 13.4 → 13.1 → 13.2 → 13.5, with 13.3 deferred.
* **"Show strikeout lines"** checkbox (default on). Off skips all line/anchor drawing, so only the cell pattern is visible.
* **"Grade unstruck composites by Ω"** checkbox (default off; confirmed in the Prompt 22 follow-up):
  * Primes: unchanged, the existing cyan `.prime-origin` highlight. (It reads as grey on the user's dark-mode screen; the exact current color is what's wanted.)
  * Struck composites: unchanged, the plain grey-blue cell.
  * Unstruck ("dirty") composites: the same cells amber-highlighted today (at or past the next-prime square, smallest prime factor > max strikeout). Off: flat amber as today. On: graded by $\Omega(n)$:
    * $\Omega = 2$ (semiprime): amber, the current rough-composite color
    * $\Omega = 3$: red
    * $\Omega \ge 4$: purple
  * Example: Max Strikeout = 2 leaves every odd composite ≥ 9 unstruck. With grading on, 9, 15, 21, 25 are amber; 27, 45, 63, 75 red; 81, 135 purple.
  * Colors should match the `sieve_detail.html` taxonomy (semiprime `#d97706`, almost-prime `#dc2626`, purple `#a855f7`) or be tuned to the current rough-composite amber, keeping the same "faint fill + inset outline + colored text" style.
* Considered and dropped for now: shading *every* composite by Ω, struck or not ("All by Ω"). The user wants the distinction only among the numbers the partial sieve has missed.

### 13.5 Least-oblique slope control (§12.2)
A single global switch: **Slope: Default "/" | Least oblique**.
* Default "/": today's rule, $k = \lfloor W/p \rfloor$, shift $kp - W \le 0$.
* Least oblique: also consider the "\" option, $k' = \lceil W/p \rceil$, shift $k'p - W \ge 0$, and use whichever shift has the smaller magnitude. A tie goes to "/". Check against Prompt 15 for $p=5$: W=6 "/" 1:1, W=7 "/" 1:2, W=8 "\" 1:2, W=9 "\" 1:1, W=10 vertical. All match.
* Implementation notes:
  * With "\", some phases start in row 1 ($k'p > W$), so the "first point is always in row 0" assumption behind top-edge extension (§7) no longer holds. The top extension is applied only when the phase's first point is in row 0; otherwise the stripe starts at its first point.
  * Stripes are broken by a more general rule: connect two consecutive points only if the step between them matches the phase's intended (row step, column shift). This includes today's "same row → break" case and the new case where a "\" line would wrap across the seam.
  * Keyholes are unchanged: phase 1 still starts at $p$ in row 0.
* **Composites** (interim, per Prompt 22): a composite's line may never be more oblique than its smallest prime factor's. It uses that prime's chosen geometry (same $k$, same direction) and only adds emphasis on the parts of the host line that are its own multiples. The extra factors emphasize lines already on the board; they add no new geometry. This partly settles §10 in favor of one host (the smallest prime factor). §10's multiple-host idea and the W=8 "isolated points vs. continuous segment" question stay open.
* The user questioned whether the composite-strikeout option is worth keeping at all (Prompt 22). With Ω-graded shading of the unstruck composites (13.4), cell shading may cover the "degree of non-primeness" goal better than stacked line thickness. Revisit this before investing more in §10.

### 13.6 Slope-control alternatives considered (recorded per user request, not planned)
1. **Global two-way (chosen):** Default "/" vs. least oblique, for all prime lines at once. The simplest control, and it keeps the "/" default that best shows periodicity.
2. **Three-way: "/", least oblique, most oblique.** "Most oblique" always picks the larger-magnitude shift of "/" and "\". This is mainly for comparison: it exaggerates the tilt to make the change from vertical to maximally tilted at mid-period easy to see, and flipping between the three would show how much of the visible structure depends on the drawing choice rather than on the math (the struck cells are identical in all three).
3. **Global plus per-prime overrides:** a global mode, plus a small row of per-prime checkboxes (like the prime grid in `sieve_detail.html`) that flip individual periods between "/" and "\". This matches the Prompt 19 wording "defaulting to off per period," and lets someone isolate one prime's behavior while leaving the others in the default.
4. **Always "\" (descending only):** the mirror of the default, for comparing the two directions. It gives no readability benefit on its own.
5. **Automatic by threshold:** flip to "\" only when the "/" shift is more than some fraction of W (e.g. $> W/2$), or only for primes above some size. This keeps small primes' periodicity readable while taming large-prime lines at big widths. Rejected for now because Prompt 19 asked for a manual toggle, not automatic behavior.
6. **Per-row minimum (any row step):** allow connecting multiples more than one row apart when that gives a shallower line (stride $> 2W$). This mostly matters for $p > W$ (§12.5), which already needs its own design pass.

### 13.7 Housekeeping
* The uncommitted slider-range increase (N to 100,000, W and Max Strikeout to 300, zoom min 3) was an experiment before 13.3. With DOM cells it is too slow at large N. Keep it, but only rely on those ranges once 13.3 is done.

## 14. v4.5 as built (Prompts 22–27)

* **13.1 Click-to-edit:** implemented. Click a slider's number to type a value. Enter/blur commits (clamped to the slider range), Escape cancels. Typing a Max Strikeout value unlocks it.
* **13.2 Guide numbers:** implemented, stacked one per line in a collapsible "Guide Numbers" panel:
  1. Width W with its factorization (e.g. `360 = 2³·3²·5`), and the **next primorial width**: the smallest primorial greater than W.
  2. Primorial of the largest prime in the strikeout set.
  3. Primorial of the next prime above the strikeout set.
  4. Next-prime square (clickable; unchanged).

  Figures 2–3 now track **Max Strikeout**, not W (this changes §11, where they were deliberately W-based; they coincide when locked). Primorials are exact `BigInt` values (see §15; the brief "∞" version is superseded).
* **Strikeout-prime circles with lines off:** a new checkbox (default on). With lines off, every prime in the strikeout set keeps its colored circle: all in row 0 when locked, wherever they fall when unlocked.
* **Layout:** two collapsible `<details>` panels ("Guide Numbers", "Controls"), each with its own triangle on the left. Controls are one row of sliders, with the Lock checkbox under the Max Strikeout slider, then one row of checkboxes. Checkbox labels were shortened to fit on one row, and each has a `title` tooltip with the full description.

## 15. v4.6 (Prompt 28)

* **More guide numbers:** Next-prime cube $q^3$ (first missed $\Omega=3$ composite) and Next-prime 4th power $q^4$ (first missed $\Omega=4$ composite), where $q$ is the next prime above the strikeout set. Every unstruck composite has all prime factors $\ge q$, so these are exactly the first red and first purple cells when grading is on. Both are clickable, scrolling to the cell like the square does.
* **Exact primorials:** computed as `BigInt` and shown in full with a digit count (2160# ≈ 916 digits, formatted in well under a millisecond). Only abbreviated (first/last 12 digits) above 20,000 digits, which the current slider limits can't reach. Checked against OEIS A002110 (23# = 223,092,870; 29# = 6,469,693,230; 53# = 32,589,158,477,190,044,730). A link to that table is in the guide panel.
* **Lock to Grid Width** sits on the same line as the Max Strikeout label.
* **Sieve Length up to 1,000,000.** Measured cost of the current DOM renderer (W = 7): 100k ≈ 0.5 s, 300k ≈ 1.5 s, 1M ≈ 5.4 s per redraw. So 1M works but is over the 2–3 s comfort limit; §13.3's renderer rewrite is the fix if that matters.
* **Render warning bar:** a red bar under the controls appears (a) when the grid exceeds the browser's canvas limit (measured in Chromium: 65,535 px per side, 16384² px area; Safari/Firefox may be lower). The canvas is then hidden rather than covering the grid with a white box, and lines/circles are not drawn. It also appears (b) when a redraw takes over 2 s. Example: W = 7, N = 100,000 at zoom 45 is 317 × 642,872 px, so no lines; zooming out or widening brings them back.

### 15.1 Deprecated: composite (non-prime) strikeouts and per-composite colors
Per user: "The Non-prime strikeouts option is not helping." Both checkboxes are hidden (`hidden` attribute on their labels in `index.html`); the code behind them is kept, so they stay unchecked and have no effect.

What the features did, for reference if they come back:
* **Non-Prime Strikeouts (Multi-Factor Stacking)** (`#non-prime-toggle`): drew a strikeout line for every composite period $4 \le k \le$ Max Strikeout using the same independent $\lfloor W/k \rfloor$ geometry as primes, with thickness scaled by $\Omega(k)$ (`0.35 + 0.25·Ω` × base). The intent was to show "degree of non-primeness" by stacking lines on multi-factor nodes. Its geometry was never reconciled with the host-prime piggyback model (§10), and Ω-graded cell shading (§13.4) now shows the same information more directly.
* **Own Color per Composite** (`#individual-color-toggle`): composite lines (and the emphasized multiples-of-W line when W is composite) used a per-value color instead of inheriting their smallest prime factor's color.

**To restore:** remove `hidden` from the two labels. §10 (piggyback model) and the §13.5 composite rule (never more oblique than the smallest prime factor) are the design notes to pick up from.

## 16. Logged, not started (Prompt 29): number-visibility options, to build with the slope control (§13.5)

Goal: when zoomed far out, give different ways to see how prime density changes across large scales.

* **Hide all numbers:** no numbers or cell highlighting, only the interference pattern of the strikeout lines.
* **Hide only the highlighted numbers:** exact meaning to confirm before building. Either (a) keep the plain numbers but drop the highlighting (cyan primes, amber/red/purple unstruck composites), or (b) blank out the highlighted cells, leaving gaps where the primes and unstruck composites are.
* Probably a 3-way "Numbers: All | Hide highlighted | None" control. It works with the existing "Strikeout Lines" and "Grade by Ω" checkboxes.
* Performance note: "None" could skip building DOM cells (or their text) altogether, which is most of the redraw cost at large N (§15). That would make this mode noticeably faster at 100k–1M.

### 16.1 Refinement (Prompt 30): clickable color legend
Instead of a separate "Numbers: All | Hide highlighted | None" control, add a **color legend** whose entries toggle each group's numbers on or off. This settles the §16 ambiguity: each group can be hidden independently, so both readings are possible.
* Legend entries (each clickable, visibly dimmed when off): **Primes** (cyan) · **Struck composites** (plain grey-blue) · **Unstruck Ω=2** (amber) · **Unstruck Ω=3** (red) · **Unstruck Ω≥4** (purple). While grading is off, the three unstruck entries collapse into one amber entry.
* "Hide all numbers" = every entry off, leaving only the line interference. "Hide highlighted" = everything off except struck composites (or the reverse).
* Open question for build time: does turning a group off blank the cell entirely, or keep a faint cell outline so the grid structure stays visible when zoomed out? Also: should the strikeout lines get their own legend entries (per prime, using the persistent colors)?
* There's no legend today, so this adds one (natural home: the Controls panel, or just above the grid).

## 17. Toward v1.0 (Prompt 33): repo and branch cleanup

The app is close to a useful v1.0 product. (Versioning note: internal "v4.x" labels have seen many breaking changes; the repository-level release would be **v1.0**, the first version meant for use rather than exploration.)

### 17.1 Pre-release checklist (from Prompt 32)
1. Commit `prompt.md`. It's still untracked, but the spec cites it by prompt number throughout.
2. Tests commit: fix `tests/visual_check.js` (target `index.html`, select checkboxes by ID, replace the non-prime cases), add a root `.gitignore` (`.DS_Store`, `node_modules/`, `*.bak`).
3. README: the user's additions, plus the `README_v4.md` motivation merged in, a guide to which page is which (v1–v4), the docs, and how to run the checks.
4. Delete the untracked leftovers: `ClaudeThinksThisway.md`, `sieve_v4_spec.bak.md`, `sieves_v4.html.bak`.
5. Optionally fix stale docs: `sieve_detail_spec.md` (describes `sieves_v3.html`, absolute local links), and `sieves_v2` (no `.html` extension).
6. Tag the release (`v1.0`) once the above is merged to `main`.

### 17.2 Branch cleanup
Per user: nothing on the other branches is of deep value that couldn't be recovered from git history. State as of this writing:

| Branch | Status | Action |
|---|---|---|
| `v4_sieve_and_detail` (current) | Holds all v4 work; `origin` copy is 1 commit behind | Push, open a PR into `main`, merge. Then delete locally and on `origin`. |
| `main` | Already merged into the current branch | Keep; it becomes the v1.0 line. |
| `sieve_v4` | Fully merged (its tip 6fe785f is already on `main`) | Delete locally. Nothing is lost. |
| `start_at_1` | 1 unmerged commit (84fa92d: `interface_v1.py` starts display at 1; that file is no longer in the tree) | Delete locally and on `origin`. The commit is also on `origin/start_at_1`, so delete the remote last, or tag it first if you want it kept. |
| `start_at_1_html` | 1 unmerged commit (5a178cd: `sieve.html` starts at 1), **local only, never pushed** | Caution: this one is *not* recoverable from shared history once deleted. It lingers in the local reflog for about 90 days, then is gone. Either accept that, or first tag it (`git tag archive/start_at_1_html 5a178cd`) and push the tag. |

`upstream` (brimelbyu) is a separate remote. Nothing to clean up there; a PR upstream is its own decision.
