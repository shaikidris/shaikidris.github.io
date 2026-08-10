# Content source of truth — Quantitative Collatz Descent site

This site is synchronized to two public records only:

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
