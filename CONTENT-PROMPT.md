# Content source of truth

The site hosts **two independent papers**. Each page is synchronized to its own
published records, and the two must never be blended: they prove different
theorems by different architectures, with different numbering.

---

# Part A — Root (`/`): Polylogarithmic Descent, v3.2.3

Synchronized to three public records only:

1. **Primary preprint page:** SSRN
   [Paper 7290240](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=7290240),
   DOI [10.2139/ssrn.7290240](https://doi.org/10.2139/ssrn.7290240),
   *Polylogarithmic Descent for Almost All Collatz Orbits in Natural Density*.
2. **Versioned article archive:** Zenodo record
   [10.5281/zenodo.21984038](https://doi.org/10.5281/zenodo.21984038),
   version 3.2.3, *Polylogarithmic Descent for Almost All Collatz Orbits in
   Natural Density*.
3. **Formal artifact:** public
   [FirstPassageLinearTransport tag `lean-v3.2.0`](https://github.com/shaikidris/FirstPassageLinearTransport/tree/lean-v3.2.0),
   commit `ef3410843bf58d69f771f5ba2c0571d54b54da59`, archived as
   [10.5281/zenodo.21930432](https://doi.org/10.5281/zenodo.21930432).

SSRN is the primary reader-facing discovery and citation page. Zenodo remains
the immutable versioned archive and source of the exact public PDF. Neither
record changes the theorem statement or formalization boundary below.

## Frozen public theorem surface

Put \(\kappa_*=1-H_2(\log_3 2)\), \(A_{\rm FP}=1/(2\kappa_*)=9.9911133419\ldots\),
and \(c_*=2/\log(4/3)=6.9521189935\ldots\). For every fixed \(A>A_{\rm FP}\),
\(c>c_*\), \(\beta>0\), and \(0<\gamma<\kappa_*(A-A_{\rm FP})\), all but
\(O(X/(\log X)^\gamma)\) integers \(n\le X\) admit \(k<c\log n\) with
\(T^k(n)\le C_{\rm tar}(\log n)^A\) and \(\max_{j\le k}T^j(n)\le n^{1+\beta}\).

Not asserted, and never to be implied: the pure target
\(C(\log n)^{A_{\rm FP}}\), a bounded final multiplier at the critical
secondary scale, and the endpoint \(\delta=1\) in the stretched-logarithmic
companion.

## Formalization boundary

`Main.lean` exports exactly **eleven** public theorems in namespace
`FirstPassageLinearTransport.QuantitativeCollatzMain`. The canonical library
builds with no `sorry`, `admit`, project axiom, or missing module, and the
public-root axiom reports contain only `propext`, `Classical.choice`, and
`Quot.sound`.

The `/code/` page must keep stating the **declaration-level coverage
boundary**: some combined quantitative statements in the manuscript are
assembled from separately checked components rather than exported as single
wrapper theorems. That is a coverage boundary, not an admitted obligation.
Never compress this to an unqualified "no gaps."

## Figure and widget boundary

- The one-orbit dashed line is the mean-drift reference of slope \(a_0-1\),
  not a deterministic pointwise envelope.
- The target-growth comparison uses the admissible fixed exponent \(A=14\),
  not the unasserted pure target at \(A_{\rm FP}\).
- Finite orbit illustrations use the stretched-logarithmic companion target.
  The line \(c_*\log n\) is shown only as a drift reference; the theorem
  requires every fixed \(c>c_*\), so crossings are not labelled as its
  exceptional set.
- The scale calculator omits the unknown multiplicative constant
  \(C_{\rm tar}\) and must label its digit count accordingly.
- Generated values and interactive runs are illustrations, never premises of
  a theorem or evidence for the asymptotic density claim.

---

# Part B — `/cet/`: Quantitative Collatz Descent, v2.0.2

This page is synchronized to two public records only:

1. **Article:** Zenodo record
   [10.5281/zenodo.21851173](https://doi.org/10.5281/zenodo.21851173),
   version 2.0.2, *Quantitative Collatz Descent to Stretched-Logarithmic
   Scale in Natural Density, with a Lean 4 Formalization*.
2. **Formal artifact:** public
   [shaikidris/CET tag v2.0.1](https://github.com/shaikidris/CET/tree/v2.0.1),
   archived as
   [10.5281/zenodo.21797535](https://doi.org/10.5281/zenodo.21797535).

No unpublished or internal draft is a source for this site.

## Frozen public theorem surface

Put
\[
a_0=\frac{\log_2 3}{2},
\qquad
\delta_0=\frac{\log(1/a_0)}{\log(2/a_0)}
=0.251245530155874\ldots.
\]
For every fixed \(0<\delta<\delta_0\), Theorem 1.1 states natural-density-one
descent below
\[
\exp((\log n)^{1-\delta}).
\]
For every \(0<\sigma<1-\delta/\delta_0\), it also gives the displayed
stretched-exponential exceptional-count estimate, and it supplies a descent
witness before \(6.953\log n\) shortcut-map iterations on a density-one set.
The endpoint \(\delta=\delta_0\) is not claimed.

## Public proof outline

The landing page follows the six steps in §1.2 of article v2.0.2:

1. one block in parity coordinates;
2. condition on the odd count;
3. control endpoint multiplicities;
4. pull back a dense target;
5. iterate endpoints only;
6. choose the number of blocks.

The proof uses a central fixed-total Rényi estimate and endpoint-only
logarithmic-block iteration.

## Teaching order

The main page is organized for a mathematically mature reader who is new to
this proof:

1. state the public theorem and its limitations;
2. introduce the four elementary objects: orbit minimum and witness, parity
   words on dyadic blocks, natural density, and the stretched-logarithmic
   scale;
3. place the public result on the ordinary-natural-density literature line:
   Terras's density-one first descent and parity framework, Korec's
   \(n^\theta\) bound for \(\theta>\log_4 3\), Inselmann's bound for every
   fixed \(\theta>0\), and the article's moving exponent
   \((\log n)^{-\delta}\to0\); keep logarithmic-density and differently
   quantified results on separate comparison axes;
4. display the six-stage dependency spine;
5. let the reader inspect those six producer-to-consumer interfaces in the
   guided architecture lab;
6. only then introduce the quantifier and scale controls;
7. keep orbit, clock, ensemble, and exceptional-rate plots in a later
   illustration layer;
8. finish with the formalization boundary and public artifacts.

Do not move interactive parameters ahead of the definitions they manipulate.
Finite computations remain illustrations even when the page makes them
interactive.

## Formalization boundary

The public article names three referee-facing declarations:

- **collatz_central_renyi_endpoint_natural_density_descent**;
- **collatz_central_renyi_endpoint_exceptional_count_at_exponent**;
- **collatz_central_renyi_endpoint_natural_density_descent_timed**.

They formalize the principal theorem chain. The formal one-block seed uses a
stronger all-prefix estimate than the terminal consequence used by the written
proof. The Lean development is a supplementary kernel check, not a
line-by-line certification of the article's English exposition or literature
discussion.

## Figure boundary

- Orbit, witness, ensemble, and table values are computed directly by
  **scripts/make_figure_data.py** and are finite illustrations, never proof
  inputs.
- The one-orbit dashed line is a heuristic trend from the public article's
  logarithmic-block motivation, not a pointwise envelope.
- The comparison figure uses only strict public-range values of \(\delta\).
- The exceptional-rate figure uses an admissible exponent pair and sets
  \(c=1\) solely to normalize the curve; it does not estimate the article's
  proof constant or onset.
- The theorem lab must enforce \(0<\delta<\delta_0\) and visibly distinguish
  admissible from inadmissible choices of \(\sigma\). It may evaluate the
  public closed-form scale and clock, but must not estimate
  \(c_{\delta,\sigma}\) or the unspecified sufficiently-large onset.
- User-selected orbit runs are evaluated locally under the shortcut map. They
  remain finite illustrations and never change or validate the asymptotic
  theorem.

## Update gate

Before changing public prose or derived assets:

1. verify the latest Zenodo record version and file checksum;
2. compare every theorem range, exception exponent, clock, and theorem label
   against that public article;
3. compare formalization claims against the public CET tag and software DOI;
4. regenerate **paper/index.html**, **assets/figure-data.json**, and
   **assets/og-card.png**;
5. run HTML, JSON, JavaScript, internal-link, and unpublished-draft leakage
   checks;
6. do not push or deploy without separate explicit authorization.
