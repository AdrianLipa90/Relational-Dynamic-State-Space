# Indexed Tensor Gate

## Status

**OPEN by design.**

RTOFA already has:

- tensor rank \((p,q)\);
- a typed tensor-product interface;
- an explicit contraction-rule interface;
- tensor-map monoidality diagnostics;
- contraction naturality diagnostics.

The current reference element stores a flat component vector and total tensor rank. That is sufficient to test type-level laws, but it is **not sufficient** to derive canonical contraction identities on tensor products.

## Missing data

A concrete indexed tensor realization needs, at minimum:

1. an ordered list of tensor slots;
2. variance of each slot (upper/lower);
3. dimension or basis domain of each slot;
4. an explicit pairing rule identifying which upper and lower slots may contract;
5. where required, the evaluation/metric/bilinear form used by contraction;
6. a component shape compatible with those slots.

Rank alone,

\[
(p,q),
\]

does not determine these data.

## Why the gate matters

Without slot metadata, a statement such as

\[
\operatorname{Contr}(X\otimes Y)
\]

does not specify which index of \(X\) is paired with which index of \(Y\), nor which evaluation map performs the pairing. Any automatic formula would therefore smuggle a realization-specific choice into the general algebra.

RTOFA consequently keeps contraction abstract:

\[
\operatorname{Contr}_{c}:
\mathcal A^{p,q}\to\mathcal A^{p-1,q-1},
\]

where \(c\) denotes an explicitly supplied contraction rule.

## Promotion condition

The contraction/tensor coherence row may be promoted from OPEN only after an indexed realization provides:

\[
\text{slot signature}
+
\text{pairing}
+
\text{component shape}
+
\text{contraction evaluator}
+
\text{tests}.
\]

At that point one can test identities such as contraction naturality, contractions internal to one tensor factor, and cross-factor contractions without ambiguity.

## Non-conclusion

This gate is not a defect in the abstract algebra. It is a boundary between the general tensor-scalar signature and a concrete indexed tensor realization.
