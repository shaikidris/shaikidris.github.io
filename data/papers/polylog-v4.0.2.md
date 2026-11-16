# Polylogarithmic Descent for Almost All Collatz Orbits in Natural Density

**Idris Ali Shaik**

Independent researcher, Dubai, United Arab Emirates

**Email:** shaikidris@apache.org

**ORCID:** [0009-0009-9699-9712](https://orcid.org/0009-0009-9699-9712)

**Date:** 4 October 2026

**Version:** 4.0.2

**Preprint DOI:** [10.5281/zenodo.23132901](https://doi.org/10.5281/zenodo.23132901)

**2020 Mathematics Subject Classification:** Primary 11B83; Secondary 37P99,
60G40

**Keywords:** Collatz map, almost all Collatz orbits, natural density,
first passage, stopping time, parity vectors, polylogarithmic descent

## Abstract

Korec proved that, for each fixed \(\theta>\log 3/\log 4\), almost every
positive integer \(n\) has a Collatz iterate below \(n^\theta\) in natural
density.  Tao proved descent below every prescribed diverging threshold in
logarithmic density.  We obtain polylogarithmic descent in ordinary natural
density within logarithmically many steps, with bounds on the preceding
orbit values.

The shortcut map \(T\) sends even \(n\) to \(n/2\) and odd \(n\) to
\((3n+1)/2\).  The unaccelerated map \(\operatorname{Col}\) sends even \(n\)
to \(n/2\) and odd \(n\) to \(3n+1\).  For any prescribed positive function
\(f(n)\to\infty\), however slowly, we prove that almost every positive
integer \(n\), in natural density, has nonnegative integers \(k=k(n)\) and
\(\ell=\ell(n)\) satisfying
\[
T^k(n)=\operatorname{Col}^{\ell}(n)
<(\log n)^{A_{\rm FP}}f(n),
\]
where \(A_{\rm FP}\approx9.9911\) is an explicit exponent.  The shortcut
time is \(k=c_*\log n+O_f(\sqrt{\log n\,\log\log n})\), where
\(c_*=2/\log(4/3)\).  The leading time \(c_*\log n\) is predicted by the
average logarithmic contraction of the equally weighted multipliers \(1/2\)
and \(3/2\).  The unaccelerated time is
\(\ell=\tfrac32c_*\log n+O_f(\sqrt{\log n\,\log\log n})\).
Both orbits are bounded by \(nf(n)\) up to their respective times.

For each fixed \(A>A_{\rm FP}\), put \(q=A/(2A_{\rm FP})-\tfrac12\).
For sufficiently large \(X\), all but at most \(C_A X/(\log X)^q\)
integers \(n\le X\) satisfy the same conclusions with target \((\log n)^A\)
and bound \(n(\log n)^q\) on both orbits.  The constant \(C_A\) and the
time-error constants depend only on \(A\).

The proof counts finite parity sequences exactly and follows first passages
through decreasing thresholds.  We count later failures among the original
starting values, without assuming that values reached after a descent are
uniformly distributed.  For starting values \(2^M\le n<2^{M+1}\), only
\(O(\sqrt{M\log M})\) cumulative passage times need to be counted at each
threshold.  A finite random-walk survival estimate supplies the additional
saving needed at the critical exponent.

Density-one descent below a fixed multiple of \((\log n)^{A_{\rm FP}}\) is
not established, and the pointwise Collatz conjecture remains open.  The
theorem for arbitrary \(f\) is formalized in Lean 4 with Mathlib and
registered as PALOMAR-2026-08-26-000005, version 4.

## 1. Introduction and main results

We study how far a Collatz orbit descends for almost every starting value,
how long this takes, and how large the preceding orbit values can be. The
main result reaches a polylogarithmic value in ordinary natural density.
It gives two-sided time estimates for both Collatz maps and a prescribed
bound on all orbit values up to those times.

The shortcut map \(T\) sends even \(n\) to \(n/2\) and odd \(n\) to
\((3n+1)/2\). The unaccelerated map \(\operatorname{Col}\) sends even
\(n\) to \(n/2\) and odd \(n\) to \(3n+1\). We use
\(\mathbb N=\{1,2,\ldots\}\), write \(\log\) for the natural logarithm
and \(\log_2\) for the base-two logarithm, and put
\(T_{\min}(n)=\min_{j\ge0}T^j(n)\). A set \(S\subseteq\mathbb N\)
has natural density one if \(\#(S\cap[1,X])/X\to1\).

Let \(H_2(p)=-p\log_2p-(1-p)\log_2(1-p)\) be binary entropy and put
\[
p_*=\log_3 2,\qquad
\kappa_*=1-H_2(p_*),\qquad
A_{\rm FP}=\frac1{2\kappa_*}\approx9.9911,\qquad
c_*=\frac2{\log(4/3)}\approx6.9521.
\tag{1.1}\label{eq:1-2}
\]

::: {.theorem-block}

### Theorem 1.1 (polylogarithmic descent) {#thm-main-descent}

Let \(U,R:\mathbb N\to(0,\infty)\) be prescribed functions tending to
infinity. There are a set \(S\) of natural density one and constants
\(K,n_0>0\), depending only on \(U\) and \(R\), such that for every
\(n\in S\) with \(n\ge n_0\), there are nonnegative integers
\(k=k(n)\) and \(\ell=\ell(n)\) satisfying
\[
T^k(n)=\operatorname{Col}^{\ell}(n)<(\log n)^{A_{\rm FP}}U(n),
\]
\[
|k-c_*\log n|+
\left|\ell-\tfrac32c_*\log n\right|
\le K\sqrt{\log n\,\log\log n},
\]
and
\[
\max_{0\le j\le k}T^j(n)\le nR(n),\qquad
\max_{0\le i\le\ell}\operatorname{Col}^i(n)\le nR(n).
\]
Neither function is required to be monotone.

:::

The abstract uses one function \(f\), with \(U=R=f\). Conversely, the
choice \(f(n)=\min\{U(n),R(n)\}\) gives the independent bounds above.
The proof constructs a value below \(n\) for sufficiently large \(n\),
even when the prescribed target is larger than \(n\). A fixed multiple of
\((\log n)^{A_{\rm FP}}\) is not covered by this theorem.

The fixed-exponent case has an explicit bound on the number of exceptions.

::: {.theorem-block}

### Corollary 1.2 (quantitative fixed-exponent descent) {#cor-main-exceptional-rate}

For every fixed \(A>A_{\rm FP}\), put
\(q=\kappa_*A-1/2>0\). There are constants \(C_A,K_A,n_A>0\)
such that, for every sufficiently large \(X\), all but at most
\(C_A X/(\log X)^q\) integers \(1\le n\le X\) have \(n\ge n_A\)
and nonnegative integers \(k,\ell\) satisfying
\[
T^k(n)=\operatorname{Col}^{\ell}(n)<(\log n)^A,
\]
\[
|k-c_*\log n|+
\left|\ell-\tfrac32c_*\log n\right|
\le K_A\sqrt{\log n\,\log\log n},
\]
\[
\max_{0\le j\le k}T^j(n)\le n(\log n)^q,\qquad
\max_{0\le i\le\ell}\operatorname{Col}^i(n)\le n(\log n)^q.
\]
The constants depend only on \(A\).

:::

The count concerns failure to satisfy these conditions together. Its order
is sharp for this joint conclusion: the height bound itself forces at least
a constant times \(X/(\log X)^q\) exceptions, as shown in
[Proposition 7.1](#cor-joint-rate-sharpness). This is not a lower bound for
failure to descend when no height bound is imposed.

The two results follow directly from the shell estimate in
[Proposition 6.4](#prop-rank-buffer). Their proofs are given at the
end of Section 6.

### Relation to earlier results

Terras [[11]](#ref-terras), [[12]](#ref-terras-density) and Everett
[[2]](#ref-everett) proved that almost every starting value eventually
falls below its initial value. Korec
[[5]](#ref-korec) obtained descent below \(n^\theta\) in natural density
for every fixed \(\theta>\log 3/\log 4\). Inselmann [[3]](#ref-inselmann)
obtains every fixed power \(n^\varepsilon\), with shortcut time
\(\lfloor c_*\log n\rfloor\). His Theorems 1.1 and 1.9 also bound the
shortcut and unaccelerated orbits throughout the stated time interval.
For each fixed \(\varepsilon>0\), his Theorem 2.18 supplies a
power-saving exceptional count \(O_\varepsilon(X^{1-d_\varepsilon})\)
for some \(d_\varepsilon>0\).

Tao [[10]](#ref-tao) proves descent below every prescribed diverging threshold
in logarithmic density. The preprints of Allikvere [[14]](#ref-allikvere)
and Mazur [[15]](#ref-mazur) state descent below every such threshold in
natural density. Their stated unaccelerated times are eventually less than
\(12\log n\) and \(436\log n\), respectively.

We give a proof using finite parity words and first passages. For
polylogarithmic targets, it gives explicit exceptional counts and two-sided
estimates of both times. The bound on the preceding orbits can be prescribed
independently. We do not claim descent below an
arbitrary diverging absolute threshold.

Their quantitative fixed-target statements concern a different event. For
a threshold \(N_0\ge2\), Allikvere's Theorem 1.3 bounds the proportion of
odd inputs up to \(X\) that fail to reach \(N_0\) within the stated
Syracuse time by
\(O((\log N_0)^{-1/29}+X^{-1/2000})\). Mazur's Theorem 1.2 gives
\(O_d((\log N_0)^{-d})\) for each \(0<d<5/143\).
A Syracuse step sends odd \(n\) to
\((3n+1)/2^{\nu_2(3n+1)}\), where \(\nu_2(m)\) is the exponent of
\(2\) dividing \(m\). These statements do not assert the two-sided
times and prescribed height bounds of Theorem 1.1.

The earlier endpoint-transport result [[9]](#ref-endpoint-v1) concerns
a stretched-logarithmic target; the proof here is independent of it.
For surveys and complementary approaches, see [[1]](#ref-crandall),
[[6]](#ref-krasikov-lagarias), [[7]](#ref-lagarias), and
[[13]](#ref-wirsching).

### The main estimate and its proof

The constant \(c_*\) is the reciprocal of the mean logarithmic decrease
of the equally weighted multipliers \(1/2\) and \(3/2\). Put
\[
a_0=\frac{\log_2 3}{2},
\qquad c_*^{-1}=(1-a_0)\log2=\tfrac12\log(4/3).
\tag{1.2}\label{eq:1-1}
\]
For the drift heuristics, see [[4]](#ref-kontorovich-lagarias) and
[[8]](#ref-lagarias-weiss).

The obstacle is repeating a descent estimate. Values reached after one
descent need not be uniformly distributed. We count the starting values
whose orbits first enter a specified set, then repeat this argument along
decreasing thresholds. Every later passage is still a first passage of the
original orbit. This also keeps track of the additive terms in the Collatz map.

Let \(I_M=[2^M,2^{M+1})\cap\mathbb N\) be the \(M\)-th dyadic shell.
For a final threshold \(2^L\), with \(L\asymp\log M\), and an orbit
bound \(nR_M\), where \(R_M\ge4\), the principal estimate in
[Proposition 6.4](#prop-rank-buffer) bounds the exceptional proportion by
\[
C\left(
\sqrt{\frac{(M+2)\log(M+2)}{L+1}}\,2^{-\kappa_*L}
+(M+2)^{-N}+R_M^{-1}
\right).
\]
Here \(N>0\) is fixed. The constant depends on \(N\) and the fixed
upper and lower bounds for \(L/\log(M+2)\). It is uniform in
\(L\) and \(R_M\) subject to those bounds.

Three estimates produce the first term. Prefix bounds leave only
\(O(\sqrt{M\log M})\) possible cumulative passage times to each
threshold. Reversing a passage contributes a factor of order \(L\).
A finite random-walk survival estimate contributes
\(O(L^{-3/2}2^{-\kappa_*L})\). When \(L\sim A\log_2M\), their
product has order \(M^{-(\kappa_*A-1/2)}\). This explains both
\(A_{\rm FP}=1/(2\kappa_*)\) and the exponent \(q\) in
Corollary 1.2. At the critical exponent, every divergent factor is allowed,
but a fixed factor is not established.

Sections 2--3 establish the parity identities and bounds on one orbit
block. Sections 4--5 count first passages through decreasing thresholds.
Section 6 combines these estimates with the finite survival estimate
in Appendix A and proves Theorem 1.1 and Corollary 1.2. Section 7 proves
the matching lower bound forced by the orbit bound.

Theorem 1.1 is formalized in Lean 4 with Mathlib and registered as
PALOMAR-2026-08-26-000005, version 4 [[17]](#ref-palomar-v4).
[Section 8](#lean-formalization) specifies the formalization scope. The use of AI assistance is described in the
[research disclosure](#research-and-software-disclosure).

## 2. Density, parity, and affine iterates

The argument uses three common tools: a shell-to-prefix summation rule, exact
parity coding on each dyadic shell, and an affine formula for the iterate.
This section establishes all three before they are used.  Lemma 2.1 converts
shell exceptional estimates into global natural-density bounds.
Proposition 2.2 makes parity words exactly uniform on a complete shell,
supplying the counting law used in Sections 3 and 6.  Proposition 2.3
separates each iterate into its multiplicative term and affine correction,
which is used to bound every iterate in Section 3.

A dyadic threshold is a value \(2^q\). A first passage is the first
time the orbit is at or below that value. A block is the orbit segment up to
such a crossing; successive blocks start at the values reached by the
preceding crossings. The shell rank of \(n\) is \(\lfloor\log_2n\rfloor\).
The times \(k\) and \(\ell\) count shortcut and unaccelerated steps,
respectively. If \(s_h\) is the number of odd states in the first
\(h\) shortcut steps, the same value is reached after \(h+s_h\)
unaccelerated steps.

For an exceptional set \(E\subseteq\mathbb N\), shell estimates imply
the following bounds for the whole initial interval.

### Lemma 2.1 (dyadic summation) {#lem-dyadic-sum}

Suppose that \(e_M\ge0\) and
\[
\#(E\cap I_M)\le e_M2^M
\tag{2.1}\label{eq:2-shell-count}
\]
for all sufficiently large \(M\). If \(e_M\to0\), then \(E\) has natural
density zero. If, for some fixed \(q>0\), one has
\(e_M=O(M^{-q})\), then
\[
\#(E\cap[1,X])=O\!\left(\frac{X}{(\log X)^q}\right).
\tag{2.2}\label{eq:2-prefix-count}
\]

#### Proof

Fix \(\epsilon>0\) and choose \(M_0\) so that \(e_M\le\epsilon\)
for \(M\ge M_0\). If \(2^J\le X<2^{J+1}\), these shells contribute
at most \(\epsilon\sum_{M=M_0}^J2^M\le2\epsilon X\). The earlier shells
contain a fixed finite number of integers. Divide by \(X\), then let
\(\epsilon\downarrow0\), to obtain the qualitative assertion.

For the quantitative assertion, the shells with \(M<\lfloor J/2\rfloor\)
contain fewer than \(2^{J/2}\le\sqrt X\) integers. On every remaining
shell, \(e_M\ll J^{-q}\), so their total contribution is
\(O(XJ^{-q})\). Since \(J\asymp\log X\) and
\(\sqrt X=o(X/(\log X)^q)\), this proves \eqref{eq:2-prefix-count}.
\(\square\)

For \(n\geq1\), define
\[
p_i(n)=\mathbf1_{\{T^i(n)\ \mathrm{odd}\}},
\qquad
s_k(n)=\sum_{i=0}^{k-1}p_i(n).
\tag{2.3}\label{eq:2-4}
\]

The exact parity coding below is classical in the stopping-time literature;
see, for example, Terras [[11]](#ref-terras).  Its short proof is included
because no external
result is needed by the argument.

### Proposition 2.2 (parity-vector bijection) {#prop-parity-code}

For every \(M\geq0\),
\[
n\bmod2^M
\longmapsto
(p_0(n),\ldots,p_{M-1}(n))
\tag{2.4}\label{eq:2-5}
\]
is a bijection from \(\mathbb Z/2^M\mathbb Z\) to \(\{0,1\}^M\).

#### Proof

The relation
\[
n\equiv n'\pmod{2^{k+1}}
\quad\Longrightarrow\quad
T(n)\equiv T(n')\pmod{2^k}
\]
shows inductively that the first \(M\) parity bits depend only on
\(n\bmod2^M\).  For the converse, induct on the word length.  Suppose the
first bit is \(e\), and use the induction hypothesis to recover the residue
\(m=T(n)\bmod2^k\) from the remaining \(k\) bits.  If \(e=0\), the unique
compatible residue is
\[
n\equiv2m\pmod{2^{k+1}}.
\]
If \(e=1\), it is
\[
n\equiv(2m-1)3^{-1}\pmod{2^{k+1}},
\]
where \(3\) is a unit modulo \(2^{k+1}\).  The first residue is even, the
second is odd, and in either case applying \(T\) recovers \(m\bmod2^k\).
Thus every word has exactly one preimage residue. \(\square\)

Consequently, as \(n\) ranges over the complete shell \(I_M\), its length-
\(M\) parity word is exactly uniform on \(\{0,1\}^M\).

### Proposition 2.3 (exact affine iterate) {#prop-affine-iterate}

For every \(n\geq1\) and \(k\geq0\),
\[
T^k(n)
=
\frac{3^{s_k(n)}}{2^k}n
+
\sum_{i=0}^{k-1}
\frac{p_i(n)3^{s_k(n)-s_{i+1}(n)}}{2^{k-i}}.
\tag{2.5}\label{eq:2-6}
\]

#### Proof

The assertion is trivial at \(k=0\).  Passing from \(k\) to \(k+1\), an
even letter divides every existing term by two.  An odd letter multiplies
every existing term by \(3/2\) and adds \(1/2\).  This is exactly the
displayed update. \(\square\)

## 3. Parity-prefix bounds on an orbit block

The parity bijection identifies a complete dyadic shell with the Boolean
cube.  We now discard the sparse words whose prefixes deviate too far from
their mean. The resulting bounds hold at every step of the block and
will guarantee the first passages used later.

For a parity word of length \(M\), put
\[
Y_k=2s_k-k,
\qquad
H_M=\max_{0\leq k\leq M}\left|s_k-\frac k2\right|
=\frac12\max_{0\leq k\leq M}|Y_k|.
\tag{3.1}\label{eq:3-1}
\]

For \(0<p,q<1\), write
\[
D(p\|q)=p\log\frac pq+(1-p)\log\frac{1-p}{1-q}
\]
for binary relative entropy.  For \(0\le t<1/2\), put
\[
\mathcal I(t)
=D\!\left(\frac12+t\,\middle\|\,\frac12\right)
=\left(\frac12+t\right)\log(1+2t)
+\left(\frac12-t\right)\log(1-2t).
\tag{3.2}\label{eq:3-2}
\]

### Lemma 3.1 (maximal deviation of parity prefixes) {#lem-entropy-barrier}

If \(M\ge1\) and \(0\le h<M/2\), then
\[
2^{-M}\#\{w\in\{0,1\}^M:H_M(w)>h\}
\leq2\exp\!\left(-M\mathcal I(h/M)\right).
\tag{3.3}\label{eq:3-3}
\]
In particular, the right side is at most
\(2\exp(-2h^2/M)\).

#### Proof

Fix \(\theta>0\) and stop the Boolean tree at the first prefix \(u\) with
\(|Y(u)|>2h\).  For a frontier node of depth \(k\), set
\[
\Phi_\theta(u)
=2^{-k}\cosh(\theta Y(u))(\cosh\theta)^{M-k}.
\]
The identity
\[
\cosh(\theta(y-1))+\cosh(\theta(y+1))
=2\cosh(\theta y)\cosh\theta
\]
shows that replacing an unexpanded node by its two children preserves the
total potential.  The frontier formed by first-crossing prefixes and
noncrossing depth-\(M\) words therefore has total
\((\cosh\theta)^M\).  Each crossing prefix contributes at least
\(2^{-|u|}\cosh(2\theta h)\), whence
\[
\Pr(H_M>h)
\le2\exp(M\log\cosh\theta-2\theta h).
\tag{3.4}\label{eq:3-4}
\]
Take \(u=2h/M\) and \(\theta=\operatorname{arctanh}u\).  The elementary
Legendre identity
\[
u\theta-\log\cosh\theta
=D\!\left(\frac{1+u}{2}\,\middle\|\,\frac12\right)
=\mathcal I(h/M)
\]
proves \eqref{eq:3-3}.  Pinsker's inequality in this binary case, or the direct
convexity estimate \(\mathcal I(t)\ge2t^2\), gives the quadratic assertion.

\(\square\)

Set
\[
\rho:=\frac{\sqrt3}{2}=2^{a_0-1}.
\]
Define
\[
r_k(n)=
\sum_{i=0}^{k-1}
\frac{p_i(n)}{3^{s_{i+1}(n)}2^{k-i}},
\qquad
d_k=s_k-\frac k2.
\tag{3.5}\label{eq:3-5}
\]
By [Proposition 2.3](#prop-affine-iterate),
\[
T^k(n)
=\rho^k n3^{d_k}
+(r_k(n)3^{k/2})3^{d_k}.
\tag{3.6}\label{eq:3-6}
\]

### Lemma 3.2 (uniform affine correction) {#lem-affine-correction}

If \(H_M\leq h\), then for every \(1\leq k\leq M\),
\[
r_k(n)3^{k/2}
\leq
(2+\sqrt3)\left(1-\rho^k\right)3^h
<(2+\sqrt3)3^h.
\tag{3.7}\label{eq:3-7}
\]

#### Proof

For \(0\leq i<k\), the barrier gives
\(s_{i+1}\geq(i+1)/2-h\).  Hence
\[
r_k3^{k/2}
\leq
3^h\sum_{i=0}^{k-1}\frac{3^{(k-i-1)/2}}{2^{k-i}}
=\frac{3^h}{2}\sum_{j=0}^{k-1}\rho^j,
\]
which is \eqref{eq:3-7}. \(\square\)

For \(0<\eta\leq1\), let \(W_\eta\) be the set of integers \(n\) such
that
\[
\rho^k n^{1-\eta}
\leq T^k(n)\leq
\rho^k n^{1+\eta}
\qquad
(0\leq k\leq\lfloor\log_2n\rfloor).
\tag{3.8}\label{eq:3-8}
\]

Put
\[
c_0=\frac1{2(\log_2 3)^2},
\qquad
C_0=2e^{4c_0}.
\]
The following estimate is uniform in the tolerance:
\[
\frac{\#(I_m\setminus W_t)}{2^m}
\le C_0e^{-c_0t^2m}
\qquad(0<t\le1).
\tag{3.9}\label{eq:6-8d}
\]

#### Proof

When \(m\ge4\) and \(tm\ge2\), apply [Lemma 3.1](#lem-entropy-barrier) at
height
\[
h=\frac{tm}{2\log_2 3},
\qquad 3^h=2^{tm/2}.
\]
Here \(h<m/2\), since \(t\le1<\log_2 3\), so the height is in the range of
[Lemma 3.1](#lem-entropy-barrier).
If \(H_m\le h\), then \(|d_k|\le h\) for every \(k\le m\).  Since
\(n\ge2^m\),
\[
3^{-h}=2^{-tm/2}\ge n^{-t},
\qquad
3^h=2^{tm/2}\le2^{-tm/2}n^t.
\]
Thus the multiplicative term in \eqref{eq:3-6} lies above
\(\rho^kn^{1-t}\) and below
\(2^{-tm/2}\rho^kn^{1+t}\).  The unused difference from the upper bound is at least
\[
\left(1-2^{-tm/2}\right)\rho^m2^{(1+t)m}
\ge\frac12\,2^{(a_0+t)m}.
\]
Meanwhile [Lemma 3.2](#lem-affine-correction) and \(d_k\le h\) bound the
additive term in \eqref{eq:3-6} by
\[
(2+\sqrt3)3^{2h}=(2+\sqrt3)2^{tm}.
\]
For \(m\ge4\), this is at most the displayed slack because
\(2^{a_0m}/2\ge2^{4a_0}/2=9/2>2+\sqrt3\).  Hence
for \(n\in I_m\), \(H_m(n)\le h\) implies \(n\in W_t\), or equivalently
\(I_m\setminus W_t\subseteq\{x\in I_m:H_m(x)>h\}\).  By
[Proposition 2.2](#prop-parity-code), [Lemma 3.1](#lem-entropy-barrier), and
\(\mathcal I(u)\ge2u^2\), the complementary proportion is at most
\[
2\exp\!\left(-\frac{t^2m}{2(\log_2 3)^2}\right)
=2e^{-c_0t^2m}.
\]
When \(m<4\) or \(tm<2\), \(t^2m\le4\), so the trivial shell bound is
absorbed by \(C_0=2e^{4c_0}\).  Thus \eqref{eq:6-8d} is uniform in \(t\).
\(\square\)

## 4. Counting first-passage preimages

The barrier identifies a sparse set of bad orbit values.  To count the
starting values whose orbits reach such values, we reverse their first
passage to a lower threshold. The estimate below bounds the number reaching
any specified subset of the crossing interval.

For real \(Y>1\), define
\[
\tau_Y(n)=\min\{h\geq0:T^h(n)\leq Y\}
\tag{4.1}\label{eq:4-1}
\]
when the set is nonempty.

### Lemma 4.1 (first-passage band and reverse product) {#lem-first-passage}

Let \(1<Y<2^M\), let \(n\in I_M\), and suppose
\(\tau_Y(n)=h\geq1\).  Write \(x_j=T^j(n)\), \(y=x_h\), and let \(s\)
be the number of odd values among \(x_0,\ldots,x_{h-1}\).  Then
\[
\frac Y2<y\leq Y
\tag{4.2}\label{eq:4-2}
\]
and
\[
n=
\frac{2^hy}{3^s}
\prod_{\substack{0\leq j<h\\x_j\ \mathrm{odd}}}
\left(1-\frac1{2x_{j+1}}\right).
\tag{4.3}\label{eq:4-3}
\]
Consequently, whenever \(h<2Y\),
\[
\left(1-\frac h{2Y}\right)\frac{2^hy}{3^s}
\leq n\leq\frac{2^hy}{3^s}.
\tag{4.4}\label{eq:4-4}
\]

#### Proof

The final crossing cannot be odd: otherwise
\(x_h=(3x_{h-1}+1)/2>x_{h-1}>Y\).  Hence \(x_{h-1}=2y\), proving
\eqref{eq:4-2}.  Reversing an even step gives \(x_j=2x_{j+1}\), while reversing an
odd step gives
\[
x_j=\frac{2x_{j+1}-1}{3}
=\frac23x_{j+1}\left(1-\frac1{2x_{j+1}}\right).
\]
Multiplication proves \eqref{eq:4-3}.  Every odd factor occurs before the final
crossing, so its following state is greater than \(Y\).  Therefore
\(\prod_i(1-u_i)\geq1-\sum_i u_i\) gives a lower product bound
\(1-s/(2Y)\geq1-h/(2Y)\); the upper bound is one. \(\square\)

Write the reverse product in \eqref{eq:4-3} as
\(\prod_{j<h}(1-u_j)\), where
\[
u_j(n)=
\begin{cases}
\dfrac1{2T^{j+1}(n)},&T^j(n)\text{ odd},\\[2mm]
0,&T^j(n)\text{ even},
\end{cases}
\qquad
E_Y(n)=Y\sum_{j=0}^{h-1}u_j(n).
\tag{4.5}\label{eq:4-5}
\]
The factor \(Y\) records the additive reverse loss at the target scale:
\(E_Y/Y\) is an additive upper bound for the defect of the reverse product.
It also makes concatenation compatible with changing thresholds.  If a
segment is measured locally at \(Y'\geq Y\), then its contribution after
rescaling to the final threshold \(Y\) is exactly \(Y/Y'\) times its local
contribution to \(E_{Y'}\).  Thus segment losses add after rescaling, which is
the coordinate used below to bound the total loss along a decreasing
threshold chain.
The elementary product inequality gives
\[
1-\frac{E_Y(n)}Y
\le\prod_{j=0}^{h-1}(1-u_j(n))\le1.
\tag{4.6}\label{eq:4-6}
\]

### Lemma 4.2 (starting values reaching one value at a fixed time) {#lem-loss-filtered-fibers}

Let \(D\ge0\), and suppose
\[
\frac DY\le\frac13.
\tag{4.7}\label{eq:4-7}
\]
For a fixed pair \((h,y)\), the number of starting values \(n\in I_M\) satisfying
\[
\tau_Y(n)=h,
\qquad
T^h(n)=y,
\qquad
E_Y(n)\le D
\]
is at most
\[
1+3D\frac{2^M}{Y}.
\tag{4.8}\label{eq:4-8}
\]

#### Proof

Put \(P(n)=\prod_{j<h}(1-u_j(n))\).  By [Lemma 4.1](#lem-first-passage),
if two such starting values had odd
counts \(s_1<s_2\), put \(A_i=2^hy/3^{s_i}\).  Then
\(A_1\ge3A_2\), while \eqref{eq:4-3} and \eqref{eq:4-6} give
\[
n_1=A_1P(n_1)
\ge3A_2\left(1-\frac DY\right)
\ge2A_2\ge2n_2.
\]
This is impossible in the half-open shell \(I_M\).  The argument uses
only positive products and introduces no division by a reverse product.
Fix the common odd count and put
\(A=2^hy/3^s\).  All such starting values lie in
\([(1-D/Y)A,A]\).  Nonemptiness, \eqref{eq:4-7}, and \(n<2^{M+1}\) imply
\(A<(3/2)2^{M+1}\), so this interval has length at most
\[
3D\frac{2^M}{Y}.
\]
Any additional congruence or residue restriction can only reduce the number
of starting values in this interval.
This proves \eqref{eq:4-8}. \(\square\)

### Proposition 4.3 (starting values reaching a specified set) {#prop-loss-transport}

Put \(J_Y=(Y/2,Y]\cap\mathbb N\). Let \(1<Y<2^M\) and
\(H\in\mathbb Z_{\ge0}\). Under
\eqref{eq:4-7}, every \(B\subseteq J_Y\) satisfies the
exact bound
\[
\#\left\{n\in I_M:
\begin{array}{l}
\tau_Y(n)\le H,\quad
T^{\tau_Y(n)}(n)\in B,\\
E_Y(n)\le D
\end{array}
\right\}
\le
H\left(1+3D\frac{2^M}{Y}\right)|B|.
\tag{4.9}\label{eq:4-9}
\]
Consequently,
\[
\#\left\{n\in I_M:
\begin{array}{l}
\tau_Y(n)\le H,\quad
T^{\tau_Y(n)}(n)\in B,\\
E_Y(n)\le D
\end{array}
\right\}
\le
H(1+3D)\frac{2^M}{Y}|B|.
\tag{4.10}\label{eq:4-10}
\]
The estimate remains valid when the starting values are restricted to any subset.

#### Proof

Since \(Y<2^M\), every passage time is positive.  Sum
[Lemma 4.2](#lem-loss-filtered-fibers) over the at most \(H|B|\) pairs to
obtain \eqref{eq:4-9}.  The contribution \(H|B|\) is at most
\(H(2^M/Y)|B|\), which gives \eqref{eq:4-10}. \(\square\)

## 5. Decreasing thresholds and accumulated reverse loss

To apply Section 4 repeatedly, we need to identify each successive crossing
as a first passage of the original orbit. We also need a bound on its reverse
product that depends on the final threshold, rather than on the full elapsed
time. The following two lemmas provide these facts.

Consider a finite sequence of thresholds with strictly decreasing integer
exponents \(q_0>\cdots>q_i\ge1\). Set \(n_0=n\), \(t_0=0\), and
suppose that \(n_j>2^{q_j}\) and the first-passage time
\(h_j=\tau_{2^{q_j}}(n_j)\) exists. Define
\[
n_{j+1}=T^{h_j}(n_j),\qquad t_{j+1}=t_j+h_j.
\tag{5.1}\label{eq:5-chain}
\]

### Lemma 5.1 (successive crossings are direct first passages) {#lem-nested-passage}

For every block in this sequence,
\[
t_{j+1}=\tau_{2^{q_j}}(n),\qquad
n_{j+1}=T^{\tau_{2^{q_j}}(n)}(n).
\tag{5.2}\label{eq:5-direct}
\]

#### Proof

The assertion is the definition for \(j=0\). Inductively, every state
before \(t_j\) exceeds the preceding threshold and therefore also the
smaller threshold \(2^{q_j}\). The orbit from \(n_j\) stays above
\(2^{q_j}\) until its local first-passage time \(h_j\). Thus
\(t_j+h_j\) is the original orbit's first crossing of that threshold.
\(\square\)

### Lemma 5.2 (reverse loss along decreasing thresholds) {#lem-rank-loss}

Suppose that, for a fixed \(r_*>0\), every block has duration
\(h_j\le m_j\), where \(m_j=\lfloor\log_2 n_j\rfloor\), and
\(q_j+1>r_*m_j\). Then the direct first passage to the final threshold
satisfies
\[
E_{2^{q_i}}(n)<\frac{q_i+2}{r_*}.
\tag{5.3}\label{eq:5-loss}
\]

#### Proof

The final step of each block is even. Every state following an odd step
in block \(j\) therefore exceeds \(2^{q_j}\), and each corresponding
reverse-product decrement is less than \(2^{-q_j-1}\). Expressing all
decrements at the final scale \(2^{q_i}\) gives
\[
E_{2^{q_i}}(n)
<\frac12\sum_{j\le i}m_j2^{q_i-q_j}
<\frac1{2r_*}\sum_{j\le i}(q_j+1)2^{q_i-q_j}.
\]
The exponents \(q_j\) are distinct and at least \(q_i\). Hence this
last sum is at most
\[
\frac1{2r_*}\sum_{d\ge0}(q_i+d+1)2^{-d}
=\frac{q_i+2}{r_*},
\]
using \(\sum_{d\ge0}2^{-d}=\sum_{d\ge0}d2^{-d}=2\).
\(\square\)

In Section 6, a block starting at a value in \(I_m\) lasts at most \(m\) steps.
Their threshold exponents satisfy the hypotheses of Lemma 5.2 with one
fixed \(r_*\). No condition on the value reached at the final crossing
is needed to bound the reverse loss accumulated before it.

## 6. Shrinking prefix bounds and compressed passage times

Section 4 bounds the number of starting values whose first passage
reaches a specified set. Section 5 bounds the accumulated reverse loss.
To obtain a polylogarithmic target, we now bound the number of possible
passage times and the proportion that fail to cross the next threshold.
At large ranks, each descent reduces the rank by a fixed ratio. Shrinking
prefix tolerances then keep the sum of the time errors small. Near the
final rank, these tolerances no longer give the required exceptional-count
bound. We instead decrease the rank by a bounded amount at each passage
and use a finite survival estimate to count failures to cross. The change
occurs at a rank of order \(\log M\). Proposition 6.4 combines the two estimates.

For each shell \(I_M\), prescribe an integer final threshold exponent
\(L_M\asymp\log M\). The choices yielding Theorem 1.1 and Corollary 1.2
are made after Proposition 6.4. The switch exponent \(S_M\) defined below
will be chosen so that \(L_M<S_M\) for all sufficiently large \(M\).

### First passages at large shell ranks

Fix parameters
\[
a_0<r_{\rm hi}<1,
\qquad
0<\tau<r_{\rm hi}-a_0,
\tag{6.1}\label{eq:6-1}
\]
and constants \(D_{\rm hi},C_{\rm sw}>0\). Put
\[
S_M=\left\lceil C_{\rm sw}\log(M+2)\right\rceil,
\tag{6.2}\label{eq:6-2}
\]
and, for a block starting in \(I_m\) with \(m\ge S_M\), use the tolerance
\[
\eta_{M,m}
=\min\left\{\tau,
D_{\rm hi}\sqrt{\frac{\log(M+2)}m}\right\}.
\tag{6.3}\label{eq:6-3}
\]
Since \(\eta_{M,m}\le\tau<r_{\rm hi}-a_0\), membership in
\(W_{\eta_{M,m}}\) guarantees a crossing of \(2^{\lfloor r_{\rm hi}m\rfloor}\)
within \(m\) steps for all sufficiently large \(m\). Indeed,
\[
T^m(x)\le\rho^m x^{1+\eta_{M,m}}
<2^{(a_0+\tau)m+1+\tau}
\le2^{\lfloor r_{\rm hi}m\rfloor}.
\]
Proposition 6.2 will estimate how many values fail this condition.

Fix \(M\), write \(S=S_M\), and define the initial exceptional set
\(\mathcal F^{\rm ini}_M=I_M\setminus W_{\eta_{M,M}}\).
For \(n\in I_M\setminus\mathcal F^{\rm ini}_M\), let \(n_0=n\),
\(m_0=M\), and \(H_0=0\). Define a finite sequence recursively.
At each \(n_i\in I_{m_i}\) with \(m_i\ge S\) and
\(n_i\in W_{\eta_{M,m_i}}\), put
\[
q_i=\lfloor r_{\rm hi}m_i\rfloor,\qquad
h_i=\tau_{2^{q_i}}(n_i),\qquad
n_{i+1}=T^{h_i}(n_i),\qquad
H_{i+1}=H_i+h_i.
\tag{6.4}\label{eq:6-4}
\]
The value \(n_{i+1}\) at the crossing is called the *landing*.
An upper endpoint \(n_{i+1}=2^{q_i}\) ends this sequence. When \(q_i\le S\),
repeated halving reaches a shell below \(L_M\) in at most \(S\) further
steps. Every nonendpoint landing belongs to \(I_{q_i-1}\).
If \(q_i-1<S\), it is the initial value of the small-rank sequence defined
below. If \(q_i-1\ge S\), the recursion continues precisely when
\(n_{i+1}\in W_{\eta_{M,q_i-1}}\), with \(m_{i+1}=q_i-1\).

Let \(\mathcal F^{\rm hi}_M\) consist of those starting values in
\(I_M\setminus\mathcal F^{\rm ini}_M\) whose sequence ends at either an
upper endpoint with \(q_i>S\), or a nonendpoint landing outside
\(W_{\eta_{M,q_i-1}}\) with \(q_i-1\ge S\). Every
earlier large-rank value satisfies its prefix condition. Thus this set counts
the first failure along the sequence.

### Lemma 6.1 (possible passage times at large ranks) {#lem-time-support}

There is a constant \(K>0\), depending only on the fixed parameters, such
that, for every shell \(I_M\) and every threshold rank \(q\) reached by
the sequence defined by \eqref{eq:6-4}, all cumulative first-passage times to
its landing band \(J_{2^q}=(2^{q-1},2^q]\cap\mathbb N\)
belong to a finite set \(\mathcal H^{\rm hi}_{M,q}\) satisfying
\[
\#\mathcal H^{\rm hi}_{M,q}
\le K\sqrt{(M+2)\log(M+2)}.
\tag{6.5}\label{eq:6-5}
\]

#### Proof

Write \(g=1-a_0\). We bound each block's duration, then sum the errors
over the decreasing shell ranks.

Consider one high block satisfying this condition from the shell
\(I_m\) to threshold \(2^q\), and let \(h\) be its duration and
\(t=\eta_{M,m}\).  The two bounds in \eqref{eq:3-8} and the
first-passage band give
\[
(1-t)m-q
\le gh
<(1+t)(m+1)-q+1.
\tag{6.6}\label{eq:6-6}
\]
Thus
\[
\left|gh-(m-q)\right|\le tm+t+2.
\tag{6.7}\label{eq:6-6a}
\]

The next computation makes this telescoping explicit.

Suppose high blocks \(0,\ldots,j\) have been executed.  Every landing before
the last starts another block and lies in \((2^{q_i-1},2^{q_i}]\). By the
endpoint convention above, a landing equal to \(2^{q_i}\) terminates the
chain: it is followed by deterministic halving when \(q_i\le S\), and is a
value contributing to \(\mathcal F^{\rm hi}_M\) when \(q_i>S\).
Thus no continuing block starts at an
upper endpoint.  Each lies in the unique shell \(I_{q_i-1}\), and therefore
\[
m_{i+1}=q_i-1\qquad(0\le i<j).
\tag{6.8}\label{eq:6-6b}
\]
This removes the apparent rank branching.  In particular,
\[
\sum_{i=0}^{j}(m_i-q_i)=M-q_j-j.
\tag{6.9}\label{eq:6-6c}
\]
Summing \eqref{eq:6-6a}, using \eqref{eq:6-6c}, and paying one additional
unit per block to change the center from \(M-q_j-j\) to \(M+1-q_j\), gives
the following bound on cumulative time
\[
\left|gH_{j+1}-\bigl((M+1)-q_j\bigr)\right|
\le
\sum_{i=0}^{j}(t_i m_i+t_i+3).
\tag{6.10}\label{eq:6-6d}
\]

For every block,
\[
t_i m_i\le D_{\rm hi}\sqrt{m_i\log(M+2)},\qquad t_i\le\tau,
\]
and \eqref{eq:6-6b} gives
\(m_{i+1}\le r_{\rm hi}m_i\).  The resulting geometric square-root sum is
\(O(\sqrt{M\log(M+2)})\), so the right side of \eqref{eq:6-6d} has the
same order.

For fixed \(M\) and \(q_j=q\), the center in \eqref{eq:6-6d} is fixed.
Consequently every feasible integer \(H_{j+1}\) lies in one interval of
length \(O(\sqrt{M\log(M+2)})\); counting its integer points proves
\eqref{eq:6-5}.  No union over intermediate high-rank histories remains.
\(\square\)

The fixed-time, fixed-landing count also has the following restricted-time
form.  If \(\mathcal H\) is any finite set of positive times,
\(B\subseteq J_Y\), and \(D_q\ge0\) satisfies \(D_q/Y\le1/3\), then
\[
\#\left\{n\in I_M:
\begin{array}{l}
\text{the first passage at or below }Y\text{ occurs at some }h\in\mathcal H,\\
T^h(n)\in B,\ E_Y(n)\le D_q
\end{array}\right\}
\le
\#\mathcal H\left(1+3D_q\frac{2^M}{Y}\right)\#B.
\tag{6.11}\label{eq:restricted-passage-count}
\]
This is [Proposition 4.3](#prop-loss-transport) summed only over the declared
times.  No interval structure or density hypothesis on \(\mathcal H\)
is used.

### Proposition 6.2 (density of large-rank failures) {#prop-shrinking-high-density}

Assume
\[
\frac{D_{\rm hi}}{\sqrt{C_{\rm sw}}}\le\tau
\qquad\text{and}\qquad
1\le S_M\le M.
\]
For a high threshold rank \(q\), define the complete landing-band target
\[
B^{\rm sh}_{M,S_M,q}
=\{2^q\}\cup
\left[
\bigl(I_{q-1}\cap J_{2^q}\bigr)
\setminus W_{\eta_{M,q-1}}
\right].
\]
Then the cap in \eqref{eq:6-3} is inactive at every \(m\ge S_M\), and
\[
\eta_{M,m}^2m=D_{\rm hi}^2\log(M+2).
\tag{6.12}\label{eq:6-8a}
\]
Moreover,
\[
\frac{\#(I_M\setminus W_{\eta_{M,M}})}{2^M}
\le C_0(M+2)^{-c_0D_{\rm hi}^2},
\tag{6.13}\label{eq:6-8b}
\]
and, for every \(q\) with \(S_M\le q-1\),
\[
\frac{|B^{\rm sh}_{M,S_M,q}|}{2^q}
\le 2^{-q}+\frac{C_0}{2}(M+2)^{-c_0D_{\rm hi}^2}.
\tag{6.14}\label{eq:6-8c}
\]

#### Proof

From \(m\ge S_M\ge C_{\rm sw}\log(M+2)\),
\[
D_{\rm hi}\sqrt{\frac{\log(M+2)}m}
\le\frac{D_{\rm hi}}{\sqrt{C_{\rm sw}}}\le\tau.
\]
This proves that the cap is inactive and gives \eqref{eq:6-8a}.

Apply \eqref{eq:6-8d} with \(t=\eta_{M,M}\) and use \eqref{eq:6-8a}
to obtain \eqref{eq:6-8b}.

For \(q\ge1\), the landing band \(J_{2^q}\) lies in \(I_{q-1}\) apart from its single
upper endpoint \(2^q\).  Apply \eqref{eq:6-8d} in \(I_{q-1}\), divide by
\(2^q\), and use \eqref{eq:6-8a} at \(m=q-1\).  This gives
\eqref{eq:6-8c}. \(\square\)

Consequently the initial exceptional set and every large-rank landing target
have a common density bound
\[
d_{\rm hi}(M)
\ll (M+2)^{-p_{\rm hi}},
\qquad
p_{\rm hi}
=\min\{C_{\rm sw}\log2,c_0D_{\rm hi}^2\},
\tag{6.15}\label{eq:6-9}
\]
where \(c_0>0\) is the fixed constant in the quadratic prefix-deviation
bound.  The first
term in the minimum pays for the dyadic endpoint boundary at the switch.

### Critical timeout estimate at small shell ranks

For a nonendpoint landing in a shell below \(S_M\), the construction
continues at smaller ranks. There the proof no longer imposes the large-rank
prefix condition. A failure to cross still gives information about the orbit:
every prefix of the actual parity word has kept the orbit above the next
threshold.  The exact multiplicative recurrence converts this into survival
above a fixed logarithmic barrier.  The finite ballot estimate proved in
[Appendix A](#app-finite-ballot) then gains a factor \(m^{-1}\) over the
terminal-only binomial bound.

For a block starting in \(I_m\), success means that its
first passage to the next threshold occurs within \(m\) steps.

Let \(L=L_M\asymp\log M\), fix \(K_0>0\), and put
\[
r_L=1-\frac{K_0}{2L},
\qquad
q_L(m)=\lfloor r_Lm\rfloor.
\tag{6.16}\label{eq:6-10}
\]
For sufficiently large \(L\), one has \(0<r_L<1\) and
\(q_L(m)<m\) whenever \(m\ge L\).  For \(x\in I_m\), define the low timeout
event by
\[
\operatorname{To}_{L,m}(x)
\iff
T^j(x)>2^{q_L(m)}
\quad\text{for every }0\le j\le m.
\tag{6.17}\label{eq:6-11}
\]
If this event fails, the least \(0\le h\le m\) with
\(T^h(x)\le2^{q_L(m)}\) is an actual successful first-passage block.

Let \(x_0\) be the first nonendpoint landing in a shell below \(S=S_M\).
No additional prefix condition is imposed on \(x_0\). Define the small-rank
sequence recursively, writing \(x_i\in I_{m_i}\).
A rank \(m_i<L\) ends the sequence with the required target value.
For \(m_i\ge L\), the sequence ends if
\(\operatorname{To}_{L,m_i}(x_i)\) holds. Otherwise, put
\(h_i=\tau_{2^{q_L(m_i)}}(x_i)\) and \(x_{i+1}=T^{h_i}(x_i)\).
Each such passage has duration at most \(m_i\), and the next shell rank is
at most \(q_L(m_i)<m_i\). Thus the sequence ends after at most \(S+1\) blocks.

Let \(\mathcal F^{\rm low}_{M,L}\) be the set of starting values \(n\in I_M\) whose
small-rank sequence ends at a timeout, all its preceding blocks having
crossed their thresholds. Define
\(\operatorname{Fail}^{\rm to}_{M,L}
=\mathcal F^{\rm ini}_M\cup\mathcal F^{\rm hi}_M
\cup\mathcal F^{\rm low}_{M,L}\).

### Lemma 6.3 (timeout targets and feasible times) {#lem-timeout-low-phase}

Fix \(C>1\).  Uniformly for \(L\le m\le CL\), for all sufficiently large \(L\),
\[
\boxed{
\frac{\#\{x\in I_m:\operatorname{To}_{L,m}(x)\}}{2^m}
\ll_{C,K_0}m^{-3/2}2^{-\kappa_*m}.}
\tag{6.18}\label{eq:6-12}
\]
Moreover, for every sufficiently large shell rank \(M\) and every possible
first-timeout landing band \(J_{2^p}\), the cumulative times at which that band is
reached lie in a finite set \(\mathcal H^{\rm to}_{M,p}\) satisfying
\[
\#\mathcal H^{\rm to}_{M,p}
\ll\sqrt{(M+2)\log(M+2)}.
\tag{6.19}\label{eq:6-13}
\]

#### Proof

Write \(x_j=T^j(x)\), let \(b_i\) be the parity of \(x_i\), and put
\[
s_j=\sum_{i<j}b_i,
\qquad
Z_j=s_j\log3-j\log2.
\]
Iteration of the shortcut recurrence gives the exact product
\[
x_j=x\,e^{Z_j}
\prod_{\substack{0\le i<j\\x_i\ {\rm odd}}}
\left(1+\frac1{3x_i}\right).
\tag{6.20}\label{eq:6-14}
\]
On a timeout every \(x_i>Y:=2^{q_L(m)}\).  The logarithm of the product in
\eqref{eq:6-14} is therefore between zero and \(m/(3Y)\).  Since
\(x<2^{m+1}\) and \(x_j>2^{q_L(m)}\), every prefix satisfies
\[
Z_j>-(m+1-q_L(m))\log2-\frac{m}{3Y}.
\tag{6.21}\label{eq:6-14a}
\]
Integer rounding gives
\[
m-q_L(m)
=\left\lceil\frac{K_0m}{2L}\right\rceil
\le\frac{CK_0}{2}+1.
\]
Also \(q_L(m)\ge m-CK_0/2-1\), so \(m/(3Y)\le1\) uniformly for sufficiently large \(L\).  Thus every timeout word satisfies \(Z_j>-B\) for every
\(0\le j\le m\), with the fixed choice
\[
B=\left(\frac{CK_0}{2}+2\right)\log2+1.
\]
[Lemma A.3](#lem-fair-word-barrier), followed by the exact parity-word
bijection of [Proposition 2.2](#prop-parity-code), now proves
\eqref{eq:6-12}.

It remains to identify the target set and its possible passage times.
Suppose the first timeout occurs at a low starting value \(x_i\). Let
\(H_i\) denote the total shortcut time from \(n\) to \(x_i\), including
the preceding large-rank blocks. The value \(x_i\) is the landing of the
preceding successful block; let \(p\) be that block's
threshold rank.  The identity in
[Lemma 5.1](#lem-nested-passage) collapses the preceding threshold chain,
making
\(H_i\) the direct first-passage time of the starting value \(n\) at or below \(2^p\), with
\[
x_i\in(2^{p-1},2^p].
\]
The upper endpoint cannot time out, since a power of two crosses every lower
dyadic threshold by repeated halving.  Hence \(x_i\in I_{p-1}\).  Since the
sequence has no further blocks below rank \(L\), and timeouts occur only below
the switch,
\[
L+1\le p\le S.
\]
Thus the first-timeout target in the landing band \(J_{2^p}\) is
\[
\mathcal C^{\rm to}_{L,p}
=\{y\in(2^{p-1},2^p)\cap\mathbb N:
      \operatorname{To}_{L,p-1}(y)\},
\qquad
\frac{|\mathcal C^{\rm to}_{L,p}|}{2^p}
\ll p^{-3/2}2^{-\kappa_*p}.
\tag{6.22}\label{eq:6-15}
\]
The last estimate is \eqref{eq:6-12} with \(m=p-1\), after changing only its
fixed constant and absorbing the harmless factor between \(2^{p-1}\) and
\(2^p\).

For a fixed high entry threshold, [Lemma 6.1](#lem-time-support) places the
cumulative high entry times in an interval of length
\(O(\sqrt{M\log(M+2)})\).  The possible entry thresholds vary over only
\(O(S)\) ranks, shifting the common center by \(O(S)\).  Low ranks decrease
strictly, there are at most \(S+1\) successful low stages, and each duration
is at most \(S\); hence
\[
\sum_{\text{successful low stages}}h_i\le S(S+1).
\tag{6.23}\label{eq:6-16}
\]
Taking the Minkowski sum enlarges the high interval by \(O(S^2)\).  Since
\(S=O(\log(M+2))\), this is
\(o(\sqrt{M\log M})\), proving \eqref{eq:6-13}. \(\square\)

### Assembly of the shell estimate

The times \(k,\ell\) below are constructed witnessing times. They need
not be the first times below a prescribed target.

### Proposition 6.4 (critical shell estimate with time and relative-height bounds) {#prop-rank-buffer}

Fix constants \(0<c_-\le c_+<\infty\), \(K_0>0\), and \(N>0\).  Let
\(L_M\) be an integer terminal-rank sequence satisfying, eventually,
\[
c_-\log(M+2)\le L_M\le c_+\log(M+2),
\]
and let \(R_M\ge4\) be any prescribed real sequence.  The high parameters
and switch constant may be chosen so that there are fixed constants \(C,K\)
such that, for all sufficiently large \(M\),
\[
\boxed{
\frac{\#\operatorname{Fail}^{\rm str}_{M,L_M,R_M}}{2^M}
\le C\left[
\sqrt{\frac{(M+2)\log(M+2)}{L_M+1}}\,2^{-\kappa_*L_M}
+(M+2)^{-N}+R_M^{-1}
\right].}
\tag{6.24}\label{eq:6-17}
\]
Outside this failure set, every \(n\in I_M\) has corresponding shortcut and
unaccelerated times \(k,\ell\) and one common value \(y\) such that
\[
T^k(n)=\operatorname{Col}^{\ell}(n)=y<2^{L_M},
\tag{6.25}\label{eq:6-17a}
\]
\[
|k-c_*\log n|+
\left|\ell-\frac32c_*\log n\right|
\le K\sqrt{\log n\,\log\log n},
\tag{6.26}\label{eq:6-17b}
\]
and
\[
\max_{j\le k}T^j(n)\le nR_M,
\qquad
\max_{i\le\ell}\operatorname{Col}^i(n)\le nR_M.
\tag{6.27}\label{eq:6-17c}
\]
The constants \(C,K\) depend only on the fixed data and not on the detailed
sequences \(L_M,R_M\); the lower bound on \(M\) also includes the point from which the
displayed bounds on \(L_M\) hold.  The failure set
\(\operatorname{Fail}^{\rm str}\) is the union of
\(\operatorname{Fail}^{\rm to}_{M,L_M}\) with the initial
multiplicative-maximum exception used for \eqref{eq:6-17c}.

#### Proof

**Estimating \(\mathcal F^{\rm ini}_M\cup\mathcal F^{\rm hi}_M\).**

Choose a fixed \(r\in(a_0,1)\) and
\[
a_0<r<1,
\qquad
0<\tau<\min\{r-a_0,(1-r)/r,a_0,1\}.
\tag{6.28}\label{eq:6-18}
\]
Thus \(r(1+\tau)<1\).  Use \(r_{\rm hi}=r\), choose \(D_{\rm hi}\) so that
\(c_0D_{\rm hi}^2>N+5\), and then choose \(C_{\rm sw}\) large enough that
\[
C_{\rm sw}\log2>N+5,
\qquad
C_{\rm sw}\ge D_{\rm hi}^2/\tau^2,
\qquad
rC_{\rm sw}>2c_+.
\tag{6.29}\label{eq:6-18a}
\]
With \(S_M=\lceil C_{\rm sw}\log(M+2)\rceil\), one has
\(L_M<S_M<M\) eventually.  The final high threshold entering below the
switch is still at least \(L_M+1\), since its starting shell rank is at least \(S_M\)
and its threshold rank is at least \(rS_M-1\). The proportion of
\(\mathcal F^{\rm ini}_M\cup\mathcal F^{\rm hi}_M\) is then
\(O((M+2)^{-N})\).
Indeed, [Proposition 6.2](#prop-shrinking-high-density), the direct-passage
identity, \eqref{eq:6-5}, and \eqref{eq:restricted-passage-count} bound their total proportion by
\[
d_{\rm hi}(M)
+O\!\left(\sqrt{M\log M}\,M^2d_{\rm hi}(M)\right),
\]
where the transported contribution is estimated as follows.  For a high target
rank \(q\), let \(B_q\) be its bad landing target.  Every producing block has
duration at most its starting shell rank \(m\) and \(q+1>r_{\rm hi}m\), so the bound in
[Lemma 5.2](#lem-rank-loss) gives
\(E_{2^q}(n)<D_q:=(q+2)/r_{\rm hi}\).  Take \(M\) sufficiently large that
\(D_q/2^q=(q+2)/(r_{\rm hi}2^q)\le1/3\) for every high target rank.  Thus
\eqref{eq:restricted-passage-count} applies.  Since \(|B_q|\le2^qd_{\rm hi}(M)\), it gives, after
division by \(2^M\), a band proportion
\(\ll\sqrt{M\log M}(2^{q-M}+D_q)d_{\rm hi}(M)
\ll\sqrt{M\log M}\,M d_{\rm hi}(M)\).  Summing over at most \(M+1\)
possible ranks proves the displayed total.
The exponent in \(d_{\rm hi}(M)\) exceeds \(N+5\) by
\eqref{eq:6-18a}, so the polynomial transport factors are absorbed with
room to spare.

**Estimating \(\mathcal F^{\rm low}_{M,L_M}\).**

Fix \(r_*=1/2<r_{\rm hi}\), which is permitted because
\(r_{\rm hi}>a_0>1/2\).  Eventually
\(r_*<r_{L_M}\).
Every successful high or low block from starting shell rank \(m\) to threshold rank
\(q\) then has duration at most \(m\) and \(q+1>r_*m\).  The bound in
[Lemma 5.2](#lem-rank-loss) therefore gives, at
a first-timeout target rank \(p\),
\[
E_{2^p}(n)<\frac{p+2}{r_*}.
\]
Since \(L_M\asymp\log M\) and
\(S_M=C_{\rm sw}\log(M+2)+O(1)\), a fixed \(C>1\), depending only on the
fixed bounds \(c_-\) and \(C_{\rm sw}\), satisfies
\(p-1\le S_M-1\le CL_M\) eventually; for example, any
\[
C>\max\left\{1,\frac{2C_{\rm sw}}{c_-}\right\}
\]
works for all sufficiently large \(M\).  Thus
[Lemma 6.3](#lem-timeout-low-phase) applies uniformly to every timeout band
\(L_M+1\le p\le S_M\).
For all sufficiently large \(L_M\), this loss satisfies the smallness
condition \eqref{eq:4-7}.  Apply the restricted-time form
\eqref{eq:restricted-passage-count} with target \(\mathcal C^{\rm to}_{L_M,p}\) and time set
\(\mathcal H^{\rm to}_{M,p}\).  Equations \eqref{eq:6-13} and
\eqref{eq:6-15} give
\[
\frac{\#\{\text{first timeout in band }p\}}{2^M}
\ll
\sqrt{M\log M}\,(p+1)p^{-3/2}2^{-\kappa_*p}.
\]
The geometric tail satisfies
\[
\sum_{p=L_M+1}^{S_M}(p+1)p^{-3/2}2^{-\kappa_*p}
\ll L_M^{-1/2}2^{-\kappa_*L_M}.
\tag{6.30}\label{eq:6-19}
\]
This proves the first term of \eqref{eq:6-17}.
The contribution from \(\mathcal F^{\rm ini}_M\cup\mathcal F^{\rm hi}_M\)
supplies the second term.

**Shortcut and unaccelerated time estimates.** Write \(g=1-a_0\), and let
\(H\) be the cumulative time at the last high landing, whose threshold
rank \(q_{\rm ent}\) is \(O(S_M)\). Equation
\eqref{eq:6-6d} and the geometric decay of the high blocks' starting shell ranks give
\[
\left|gH-\bigl((M+1)-q_{\rm ent}\bigr)\right|
\ll\sqrt{M\log(M+2)}.
\]
The remaining low part costs at most \(S_M(S_M+1)\), and an endpoint-halving
tail costs at most \(S_M\).  Both are absorbed by the same error.  Since
\(\log n=M\log2+O(1)\), the resulting shortcut witness satisfies
\[
k=c_*\log n+O(\sqrt{\log n\,\log\log n}).
\tag{6.31}\label{eq:6-19a}
\]

Let \(q_f\) be the final threshold rank. The small-rank sequence and the endpoint-
halving alternative give
\[
L_M-K_0/2-1\le q_f\le L_M.
\tag{6.32}\label{eq:6-19b}
\]
Indeed, if the final block is low, its starting shell rank is at least \(L_M\), so
\(q_f=\lfloor r_{L_M}m\rfloor\ge L_M-K_0/2-1\).  A threshold rank above
\(L_M\) cannot be final, whereas a nonendpoint landing at threshold
rank \(L_M\) already has shell rank \(L_M-1\); in the endpoint-halving case,
\(q_f=L_M-1\).  This accounts for every successful terminal case.
Treating every endpoint-halving step as a one-step first passage, the complete
successful chain is the direct first passage of the starting value \(n\) to its
last threshold.  If \(s\) is the number of odd shortcut steps, the exact
reverse product of Section 4 gives
\[
n=\frac{2^k y}{3^s}P,
\qquad
1-\frac{q_f+2}{r_*2^{q_f}}\le P\le1.
\tag{6.33}\label{eq:6-19c}
\]
Hence \(\log P=O(L_M2^{-L_M})\), while \(0\le\log y\le L_M\log2\).
Taking logarithms and using \eqref{eq:6-19a} yields
\[
s-\frac{k}{2}
=\frac{gk\log2-\log n+\log y+\log P}{\log3}
=O(\sqrt{\log n\,\log\log n}).
\]
Since \(\operatorname{Col}^{k+s}(n)=T^k(n)=y\), this proves the two-sided
unaccelerated-time estimate in \eqref{eq:6-17b}.

**Relative height.**  It remains to establish the common relative-height
bound.  For the first
\(M\) parity prefixes of the starting value \(n\), put
\(F_j=3^{s_j}/2^j\).  [Lemma A.4](#lem-multiplier-maximum) and the exact shell
parity law show that, outside a set of proportion at most \(4/R_M\),
\[
\max_{0\le j\le M}F_j\le R_M/4.
\tag{6.34}\label{eq:6-19d}
\]
During the first high block, the multiplicative correction in
\eqref{eq:6-14} is at most
\(\exp(M/2^{\lfloor rM\rfloor+1})\le2\) for all sufficiently large \(M\).  Thus every
shortcut state there is at most \(nR_M/2\), and every intervening unaccelerated odd
state is at most twice the following shortcut state.  Every later high block
starts below \(2^{\lfloor rM\rfloor}\), so the bound \(T^j(x)\le x^{1+\tau}\) from \eqref{eq:3-8} and
\(r(1+\tau)<1\) keep its shortcut states below \(n\) and its unaccelerated states below
\(2n\).  Low blocks and endpoint halving remain below
\(2^{2S_M+2}=M^{O(1)}<n\) eventually.  Since \(R_M\ge4\), these estimates
prove \eqref{eq:6-17c}.  Adding the initial maximum exception contributes
  the final term \(R_M^{-1}\) in \eqref{eq:6-17}.  \(\square\)

### Deductions of the main results

#### Proof of Theorem 1.1

For each shell \(I_M\), take the minima
\[
u_M=\min_{n\in I_M}U(n),\qquad v_M=\min_{n\in I_M}R(n).
\]
Both sequences tend to infinity. Put
\[
w_M=\min\{u_M,\log(M+2)\},\qquad
L_M=\left\lfloor A_{\rm FP}\log_2(M\log2)+\log_2w_M\right\rfloor,
\qquad R_M=\min\{v_M,M+2\}.
\tag{6.35}\label{eq:6-arbitrary-schedule}
\]
For all sufficiently large \(M\), one has \(R_M\ge4\) and
\(L_M\asymp\log M\), with fixed upper and lower constants. Moreover,
for \(n\in I_M\),
\[
2^{L_M}\le (M\log2)^{A_{\rm FP}}w_M
\le(\log n)^{A_{\rm FP}}U(n),\qquad R_M\le R(n).
\]
Since \(\kappa_*A_{\rm FP}=1/2\), the first term of
\eqref{eq:6-17} satisfies
\[
\sqrt{\frac{(M+2)\log(M+2)}{L_M+1}}\,2^{-\kappa_*L_M}
\ll w_M^{-\kappa_*}=o(1).
\]
Apply Proposition 6.4 with \(N=1\). The other two terms in its exceptional
proportion also tend to zero. Lemma 2.1 therefore shows that the union of
these exceptional sets has natural density zero. On its complement, the
target, time estimates, and both orbit bounds are exactly those asserted in
Theorem 1.1. The finitely many earlier integers can be omitted from the
density-one set. \(\square\)

#### Proof of Corollary 1.2

Fix \(A>A_{\rm FP}\) and put \(q=\kappa_*A-1/2>0\). Choose
\[
L_M=\left\lfloor A\log_2(M\log2)\right\rfloor,\qquad
R_M=(M\log2)^q,
\tag{6.36}\label{eq:6-fixed-schedule}
\]
and fix \(N>q\). For sufficiently large \(M\), these sequences satisfy
the hypotheses of Proposition 6.4. For \(n\in I_M\), they give
\(2^{L_M}\le(\log n)^A\) and \(R_M\le(\log n)^q\). The first term
of \eqref{eq:6-17} is
\[
O_A(M^{1/2-\kappa_*A})=O_A(M^{-q}),
\]
and the other two terms have this order or smaller. Thus the exceptional
proportion on \(I_M\) is \(O_A(M^{-q})\). The quantitative assertion of
Lemma 2.1 gives \(O_A(X/(\log X)^q)\) exceptions in \([1,X]\).
The time-error constant in Proposition 6.4 depends only on the fixed data,
which here depend only on \(A\). Enlarging the exceptional-count constant
absorbs the finitely many integers below \(n_A\). \(\square\)

## 7. The cost of the orbit bound

The exceptional count in Corollary 1.2 has a matching lower bound. This
comes from the prescribed height of the orbit, not from the difficulty of
reaching the target alone.

### Proposition 7.1 (sharpness of the joint exceptional count) {#cor-joint-rate-sharpness}

Fix \(A>A_{\rm FP}\), put \(q=\kappa_*A-1/2\), and let \(E_A\)
be the set of integers for which the complete conclusion of Corollary 1.2
fails, with its constants \(K_A,n_A\). Then
\[
\#(E_A\cap[1,X])=\Theta_A\!\left(\frac{X}{(\log X)^q}\right).
\tag{7.1}\label{eq:7-joint-order}
\]

#### Proof

The upper bound is Corollary 1.2. For the lower bound, work on a large shell
\(I_M\) and put
\[
h=\lfloor M/2\rfloor,\qquad u_M=((M+1)\log2)^q.
\]
For all sufficiently large \(M\),
\[
((M+1)\log2)^A<2^{M-h},\qquad
\log u_M\le\varepsilon_0h\log3,
\]
where \(\varepsilon_0>0\) is defined in
[Lemma A.5](#lem-multiplier-reciprocal). Every shortcut step is at least
a halving, so, for \(n\in I_M\) and \(0\le j\le h\),
\[
T^j(n)\ge2^{-j}n\ge2^{M-h}>(\log n)^A.
\]
Thus no value below the target can be reached in the first \(h\) steps.

For the first \(h\) parity letters, set \(F_j=3^{s_j(n)}/2^j\).
If \(\max_{j\le h}F_j>u_M\), the positive affine correction in
Proposition 2.3 gives, at some \(j\le h\),
\[
T^j(n)\ge nF_j>nu_M\ge n(\log n)^q.
\]
Every later time reaching the target therefore violates the shortcut orbit
bound. Such an integer is in \(E_A\), regardless of the time or
unaccelerated-orbit requirements.

Since \(h\le M\), each length-\(h\) parity word occurs exactly
\(2^{M-h}\) times on \(I_M\), by Proposition 2.2. Lemma A.5 now yields
\[
\frac{\#(E_A\cap I_M)}{2^M}
\ge\frac{2}{3u_M}\left(1-\frac{K_{\max}}h\right)
\gg_A M^{-q}.
\]
For an arbitrary large \(X\), choose \(M\) with
\(2^{M+1}\le X<2^{M+2}\). The complete shell \(I_M\) lies in
\([1,X]\), has more than \(X/4\) integers, and satisfies
\(M\asymp\log X\). Retaining this shell gives the required lower
bound for every sufficiently large \(X\). \(\square\)

This argument proves sharpness only for the joint conclusion with its stated
orbit bound. It gives no lower bound for descent failures when that bound
is removed, and does not establish optimality of \(A_{\rm FP}\).

## 8. Formal verification {#lean-formalization}

Theorem 1.1, with the shared value, both time estimates, and both orbit
bounds, is formalized in Lean 4 with Mathlib and registered as
PALOMAR-2026-08-26-000005, version 4 [[17]](#ref-palomar-v4), using only
\(\mathtt{propext}\), \(\mathtt{Classical.choice}\), and
\(\mathtt{Quot.sound}\). The source is archived at
[doi:10.5281/zenodo.23043600](https://doi.org/10.5281/zenodo.23043600).
The related registered fixed-exponent upper bound permits a constant
\(C>0\) in the target \(C(\log n)^A\) and uses the orbit bound
\(n(\lfloor\log_2n\rfloor+2)^q\); the registered lower bound counts
failure of the shortcut target-and-height conditions with those
normalizations. These differ from the printed formulations of Corollary 1.2
and Proposition 7.1. The supplement `formalization-supplement.md` gives the exact
statements, proof locations, and mathematical definitions used in the code.

## Research and software disclosure {#research-and-software-disclosure}

OpenAI Codex assisted with mathematical exploration, Lean formalization,
and manuscript preparation. The author reviewed the AI-assisted material
and takes full responsibility for the manuscript.

## Appendix A. Finite ballot estimates {#app-finite-ballot}

This appendix proves the finite-word estimate used in
[Lemma 6.3](#lem-timeout-low-phase).  Probability notation below denotes an
exact finite product weighting of words.

### Lemma A.1 (centered finite survival) {#lem-centered-survival}

Let \(X_1,\ldots,X_n\) be independent copies of a random variable on a finite
weighted alphabet such that
\[
\mathbb EX_1=0,
\qquad |X_1|\le1,
\qquad \mathbb EX_1^2=v>0.
\]
Put \(S_0=0\) and \(S_j=\sum_{i=1}^jX_i\).  For every \(h\ge0\) and
integer \(n\ge1\),
\[
\begin{split}
\mathbb P\{S_j\ge-h\text{ for }0\le j\le n\}
&\le\frac{h+1}{\sqrt n+h+1}
+\frac{(h+1)(\sqrt n+1)}{vn}\\
&\le\left(1+\frac2v\right)\frac{h+1}{\sqrt n}.
\end{split}
\tag{A.1}\label{eq:b-1}
\]

#### Proof

Set \(H=\sqrt n\), and let \(\tau\) be the smaller of \(n\) and the first
index at which \(S_j<-h\) or \(S_j\ge H\).  If no such index occurs, put
\(\tau=n\).  The stopped value has the finite expansion
\[
Y=S_\tau=\sum_{j=1}^n\mathbf1_{\{\tau\ge j\}}X_j.
\]
The indicator in the \(j\)-th summand is determined by the first \(j-1\)
letters.  Independence and centering therefore give \(\mathbb EY=0\).
Conditioning on the letters before the later increment makes every cross term
in \(\mathbb EY^2\) vanish, while the diagonal terms give
\[
\mathbb EY^2
=v\sum_{j=1}^n\mathbb P(\tau\ge j)
=v\mathbb E\tau.
\tag{A.2}\label{eq:b-2}
\]
Bounded overshoot gives \(-h-1\le Y\le H+1\).  Hence
\[
0\le\mathbb E[(Y+h+1)(H+1-Y)]
=(h+1)(H+1)-v\mathbb E\tau,
\]
so \(\mathbb E\tau\le(h+1)(H+1)/v\).  If \(U=\{Y\ge H\}\), then
\(Y\ge-h-1\) off \(U\), and \(\mathbb EY=0\) gives
\[
\mathbb P(U)\le\frac{h+1}{H+h+1}.
\]
A path surviving above \(-h\) through time \(n\) either stops at the upper
boundary or has \(\tau=n\).  Markov's inequality for \(\tau\) therefore gives
\[
\mathbb P(\text{survival})
\le\mathbb P(U)+\mathbb P(\tau=n)
\le\frac{h+1}{H+h+1}+\frac{\mathbb E\tau}{n},
\]
which proves \eqref{eq:b-1}. \(\square\)

### Lemma A.2 (uniform binomial atom) {#lem-binomial-atom}

For fixed \(p\in(0,1)\), there is \(C_p<\infty\) such that, for every
integer \(n\ge1\),
\[
\sup_{k\in\mathbb Z}\binom nkp^k(1-p)^{n-k}\le C_pn^{-1/2},
\tag{A.3}\label{eq:b-3}
\]
where masses outside \(0\le k\le n\) are zero.

#### Proof

The ratio of consecutive positive masses is
\[
\frac{n-k}{k+1}\frac p{1-p}.
\]
Thus a mode may be chosen as \(k_0=\lfloor(n+1)p\rfloor\), with
\(|k_0-np|\le1\).  For all sufficiently large \(n\), \(u=k_0/n\) remains in
a fixed compact subinterval of \((0,1)\).  The elementary factorial Stirling
bounds give
\[
\binom n{k_0}p^{k_0}(1-p)^{n-k_0}
\le\frac{C}{\sqrt{nu(1-u)}}e^{-nD(u\Vert p)}
\le C_pn^{-1/2},
\]
because \(D(u\Vert p)\ge0\).  Enlarge \(C_p\) for the finitely many smaller
values of \(n\).  Every other atom is no larger than a mode. \(\square\)

### Lemma A.3 (fair-word mass above a fixed barrier) {#lem-fair-word-barrier}

For a binary word \(b_0,\ldots,b_{m-1}\), put
\[
s_j=\sum_{i<j}b_i,
\qquad
Z_j=s_j\log3-j\log2.
\]
For every fixed \(B>0\), there is \(C_B<\infty\) such that, for every
integer \(m\ge1\),
\[
2^{-m}\#\{b:Z_j>-B\text{ for every }0\le j\le m\}
\le C_Bm^{-3/2}2^{-\kappa_*m}.
\tag{A.4}\label{eq:b-4}
\]
The constant may be chosen uniformly for \(B\) in a bounded positive
interval.

#### Proof

Give a letter \(1\) weight \(p_*\) and a letter \(0\) weight \(1-p_*\), and
write \(\mathbb P_*\) for the resulting finite product law.  The increments
of \(Z\) then have mean zero, absolute value less than one, and variance
\[
v=p_*(1-p_*)(\log3)^2=\log2\log(3/2)>0.
\]
The negated increments have the same properties.  Put
\[
\lambda=\frac{\log(p_*/(1-p_*))}{\log3}>0.
\]
For every individual word, direct simplification gives
\[
\frac{2^{-m}}{p_*^{s_m}(1-p_*)^{m-s_m}}
=2^{-\kappa_*m}e^{-\lambda Z_m}.
\tag{A.5}\label{eq:b-5}
\]

For \(m\ge8\), split the word into a first block of length
\(a=\lfloor m/4\rfloor\), a middle block of length \(b=m-2a\), and a last
block of length \(a\).  Let \(W\) be the event on the left of
\eqref{eq:b-4}, and partition its terminal values into
\[
Z_m+B\in[q,q+1),
\qquad q=0,1,2,\ldots.
\]
On \(W\), the first block stays above \(-B\).  On \(W\) in bin \(q\), the
reversed, negated last block has partial sums
\[
Z_{m-j}-Z_m>-(q+1),
\qquad 0\le j\le a.
\]
These two necessary outer-block events depend on disjoint letters.  Applying
[Lemma A.1](#lem-centered-survival) to each bounds their product probability
by
\[
\frac{C(B+1)(q+2)}a.
\]
After the two outer blocks are fixed, the terminal-bin condition asks that
the middle-block sum lie in an interval of length one.  That sum is
\(K\log3-b\log2\), where \(K\) has the
\(\operatorname{Bin}(b,p_*)\) law.  Its lattice spacing is
\(\log3>1\), so the interval contains at most one atom.
[Lemma A.2](#lem-binomial-atom) bounds the conditional probability by
\(Cb^{-1/2}\), uniformly in the outer blocks.  Since \(a\ge m/8\) and
\(b\ge m/2\),
\[
\mathbb P_*(W,\ Z_m+B\in[q,q+1))
\le C(B+1)(q+2)m^{-3/2}.
\tag{A.6}\label{eq:b-6}
\]
The power \(m^{-3/2}\) has three square-root sources: survival of the first
outer block, survival of the reversed-negated last outer block, and the
single middle-block binomial atom.
Only the two disjoint outer-block events have been multiplied here; no
independence of the full survival and terminal events is asserted.

On bin \(q\),
\(e^{-\lambda Z_m}\le e^{\lambda B}e^{-\lambda q}\).  Summing
\eqref{eq:b-6} with the weights in \eqref{eq:b-5} yields
\[
2^{-m}\#W
\le C(B+1)e^{\lambda B}
\left(\sum_{q\ge0}(q+2)e^{-\lambda q}\right)
m^{-3/2}2^{-\kappa_*m}.
\]
The series converges, and the finitely many \(m<8\) are absorbed into the
constant.  The same expression is bounded uniformly when \(B\) ranges over
a bounded positive interval. \(\square\)

This is a ballot-type estimate.  General ballot estimates for finite-variance
walks are classical; see Addario-Berry and Reed
[[16]](#ref-addario-berry-reed).  Their theorem is not a premise here: the
finite argument above supplies the precise estimate used in Section 6.

### Lemma A.4 (finite multiplicative maximum) {#lem-multiplier-maximum}

For fair binary words of length \(M\), put
\(F_j=3^{s_j}/2^j\).  For every \(u>0\),
\[
2^{-M}\#\{b:\max_{0\le j\le M}F_j>u\}\le u^{-1}.
\tag{A.7}\label{eq:b-7}
\]

#### Proof

Given a prefix, the next multiplicative factor is \(1/2\) or \(3/2\), whose
fair average is one.  Stop at the first index for which \(F_j>u\), or at
\(M\) if there is none; if \(u<1\), stop at zero.  Repeatedly replacing each
pair of children by its parent in this finite word tree shows that the stopped
terminal value has mean one.  It is nonnegative everywhere and exceeds \(u\)
on the crossing event.  Hence
\(1\ge u\,\mathbb P(\text{crossing})\), proving \eqref{eq:b-7}. \(\square\)

### Lemma A.5 (reciprocal finite multiplicative maximum) {#lem-multiplier-reciprocal}

For an integer \(h\ge1\) and \(u\ge1\), let
\[
A_h(u)=\left\{\max_{0\le j\le h}F_j>u\right\},
\qquad
\varepsilon_0=\frac{3/4-p_*}{2}>0,
\qquad
K_{\max}=\frac{3}{16\varepsilon_0^2}.
\]
If \(\log u\le\varepsilon_0h\log3\), then
\[
\frac{2}{3u}\left(1-\frac{K_{\max}}h\right)
\le2^{-h}\#A_h(u)\le\frac1u.
\tag{A.8}\label{eq:b-8}
\]
For small \(h\), a negative lower bound is understood as vacuous.

#### Proof

Stop each fair word at its first crossing of \(u\), or at \(h\) if it
does not cross.  The finite-tree identity used in Lemma A.4 gives
\(\mathbb EF_\sigma=1\).  At a crossing, the previous value is at most
\(u\), and only an upward multiplier can cross, so
\(u<F_\sigma\le3u/2\).  Consequently
\[
1\le\frac32u\,\mathbb P_{1/2}(A_h(u))
+\mathbb E_{1/2}[F_h;A_h(u)^c].
\tag{A.9}\label{eq:b-9}
\]
For each individual word there is the exact change of finite word weights
\[
2^{-h}F_h
=\left(\frac34\right)^{s_h}
 \left(\frac14\right)^{h-s_h}.
\tag{A.10}\label{eq:b-10}
\]
Therefore the final term in \eqref{eq:b-9} equals
\(\mathbb P_{3/4}(A_h(u)^c)\), and is at most
\(\mathbb P_{3/4}(F_h\le u)\).

Under the latter finite product weighting, \(s_h\) has mean \(3h/4\) and
variance \(3h/16\).  The identity
\(\log F_h=s_h\log3-h\log2\), the definition
\(p_*=\log_3 2\), and the hypothesis on \(u\) imply
\[
F_h\le u
\quad\Longrightarrow\quad
s_h\le p_*h+\frac{\log u}{\log3}
\le\left(\frac34-\varepsilon_0\right)h.
\]
Chebyshev's inequality bounds this probability by \(K_{\max}/h\).
Substitution in \eqref{eq:b-9} proves the lower bound; Lemma A.4 gives the
upper bound. \(\square\)

## References

<span id="ref-crandall">[1]</span> R. E. Crandall, *On the "3x+1" problem*, Math.
Comp. **32** (1978), no. 144, 1281--1292,
[doi:10.1090/S0025-5718-1978-0480321-3](https://doi.org/10.1090/S0025-5718-1978-0480321-3).

<span id="ref-everett">[2]</span> C. J. Everett, *Iteration of the number-theoretic
function \(f(2n)=n\), \(f(2n+1)=3n+2\)*, Adv. Math. **25** (1977), no. 1,
42--45,
[doi:10.1016/0001-8708(77)90087-1](https://doi.org/10.1016/0001-8708(77)90087-1).

<span id="ref-inselmann">[3]</span> M. Inselmann, *An approximation of the Collatz
map and a lower bound for the average total stopping time*, arXiv:2402.03276v3
(2024),
[doi:10.48550/arXiv.2402.03276](https://doi.org/10.48550/arXiv.2402.03276).

<span id="ref-kontorovich-lagarias">[4]</span> A. V. Kontorovich and J. C.
Lagarias, *Stochastic models for the \(3x+1\) and \(5x+1\) problems and related
problems*, in *The Ultimate Challenge: The \(3x+1\) Problem* (J. C. Lagarias,
ed.), American Mathematical Society, Providence, RI, 2010, pp. 131--188.

<span id="ref-korec">[5]</span> I. Korec, *A density estimate for the \(3x+1\)
problem*, Math. Slovaca 44 (1994), no. 1, 85--89,
[DML-CZ record](https://dml.cz/handle/10338.dmlcz/133225).

<span id="ref-krasikov-lagarias">[6]</span> I. Krasikov and J. C. Lagarias,
*Bounds for the \(3x+1\) problem using difference inequalities*, Acta Arith.
**109** (2003), 237--258,
[doi:10.4064/aa109-3-4](https://doi.org/10.4064/aa109-3-4).

<span id="ref-lagarias">[7]</span> J. C. Lagarias, *The \(3x+1\) problem and its
generalizations*, Amer. Math. Monthly **92** (1985), no. 1, 3--23,
[doi:10.2307/2322189](https://doi.org/10.2307/2322189).

<span id="ref-lagarias-weiss">[8]</span> J. C. Lagarias and A. Weiss, *The
\(3x+1\) problem: two stochastic models*, Ann. Appl. Probab. **2** (1992),
no. 1, 229--261,
[doi:10.1214/aoap/1177005779](https://doi.org/10.1214/aoap/1177005779).

<span id="ref-endpoint-v1">[9]</span> I. A. Shaik, *Quantitative Collatz Descent to
Stretched-Logarithmic Scale in Natural Density, with a Lean 4 Formalization*,
version 2.0.2, preprint (2026),
[doi:10.5281/zenodo.21851173](https://doi.org/10.5281/zenodo.21851173).

<span id="ref-tao">[10]</span> T. Tao, *Almost all orbits of the Collatz map
attain almost bounded values*, Forum Math. Pi **10** (2022), e12,
[doi:10.1017/fmp.2022.8](https://doi.org/10.1017/fmp.2022.8).

<span id="ref-terras">[11]</span> R. Terras, *A stopping time problem on the
positive integers*, Acta Arith. **30** (1976), 241--252.

<span id="ref-terras-density">[12]</span> R. Terras, *On the existence of a
density*, Acta Arith. **35** (1979), 101--102,
[doi:10.4064/aa-35-1-101-102](https://doi.org/10.4064/aa-35-1-101-102).

<span id="ref-wirsching">[13]</span> G. J. Wirsching, *The Dynamical System
Generated by the \(3n+1\) Function*, Lecture Notes in Mathematics, vol. 1681,
Springer-Verlag, Berlin, 1998,
[doi:10.1007/BFb0095985](https://doi.org/10.1007/BFb0095985).

<span id="ref-allikvere">[14]</span> J. Allikvere, *Almost all Collatz orbits
attain almost bounded values in natural density*, version 2, preprint
(22 July 2026),
[doi:10.5281/zenodo.21499244](https://doi.org/10.5281/zenodo.21499244).

<span id="ref-mazur">[15]</span> L. Mazur, *Natural-density almost-bounded
Collatz orbits in logarithmic time*, version 2, preprint (21 July 2026),
[public manuscript](https://www.proofatlas.ai/papers/natural-density-log-time-collatz/Mazur_Natural_Density_Collatz_Orbits_in_Logarithmic_Time_v2.pdf).

<span id="ref-addario-berry-reed">[16]</span> L. Addario-Berry and B. A. Reed,
*Ballot theorems for random walks with finite variance*, arXiv:0802.2491v2
(2008),
[doi:10.48550/arXiv.0802.2491](https://doi.org/10.48550/arXiv.0802.2491).

<span id="ref-palomar-v4">[17]</span> I. A. Shaik, *Polylogarithmic Descent
for Almost All Collatz Orbits in Natural Density*, Lean 4 formalization,
Palomar Registry, PALOMAR-2026-08-26-000005, version 4 (2026),
[registry record](https://palomar-registry.org/entry?id=PALOMAR-2026-08-26-000005&version=4).
