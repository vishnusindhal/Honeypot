"""
Math Question Generator: Algebraic Number Product Problems

Generates competition-style problems where a product of polynomial expressions
evaluated at an n-th root of an integer telescopes to yield an integer.

Identity families used:
  1. Difference of n-th powers:  x^n - a^n = (x-a)(x^{n-1} + ax^{n-2} + ... + a^{n-1})
  2. Sum of n-th powers (odd n):  x^n + a^n = (x+a)(x^{n-1} - ax^{n-2} + ... + a^{n-1})
  3. Difference of squares telescoping:  prod_{j=0}^{m} (x^{2^j} ± 1) = x^{2^{m+1}} - 1
  4. Cyclotomic-type:  (x^2+x+1)(x^2-x+1) = x^4+x^2+1, etc.
  5. Compositions of the above (nested telescoping)
"""

from sympy import Rational, simplify, nsimplify
from dataclasses import dataclass
from typing import List, Optional
import json


@dataclass
class Problem:
    problem_id: int
    statement: str
    alpha_definition: str
    root_degree: int
    root_value: int
    answer: int
    solution_steps: List[str]
    difficulty: str
    category: str


def sym_verify(root_degree: int, root_value: int, expanded_power_terms: dict) -> Optional[int]:
    """
    Verify that sum of c_i * alpha^i gives an integer, where alpha^n = k.
    expanded_power_terms: {exponent: coefficient, ...}
    We reduce all exponents mod n using alpha^n = k.
    """
    n, k = root_degree, root_value
    reduced = {}
    for exp, coeff in expanded_power_terms.items():
        full_powers = exp // n
        remainder = exp % n
        effective_coeff = coeff * (k ** full_powers)
        reduced[remainder] = reduced.get(remainder, 0) + effective_coeff

    if all(rem == 0 for rem in reduced if reduced[rem] != 0):
        return reduced.get(0, 0)
    return None


def numerical_verify(root_degree: int, root_value: int, answer: int,
                     expression_lambda) -> bool:
    """Verify a problem numerically using floating point."""
    alpha = root_value ** (1.0 / root_degree)
    result = expression_lambda(alpha)
    return abs(result - answer) < 1e-6


def build_problems() -> List[Problem]:
    """Build the full curated problem set with manual verification."""
    problems = []
    pid = 0

    # ================================================================
    # PROBLEM 1 [Medium]: Difference of cubes
    # (α - 1)(α² + α + 1) = α³ - 1, with α³ = 5
    # ================================================================
    pid += 1
    answer = 5 - 1
    assert numerical_verify(3, 5, answer,
        lambda a: (a - 1) * (a**2 + a + 1))
    problems.append(Problem(
        problem_id=pid,
        statement="If α satisfies α³ = 5, compute (α − 1)(α² + α + 1).",
        alpha_definition="α³ = 5",
        root_degree=3, root_value=5, answer=answer,
        solution_steps=[
            "Recognize the difference of cubes: x³ − 1 = (x − 1)(x² + x + 1).",
            "Therefore (α − 1)(α² + α + 1) = α³ − 1 = 5 − 1 = 4."
        ],
        difficulty="medium",
        category="difference_of_cubes"
    ))

    # ================================================================
    # PROBLEM 2 [Medium]: Sum of cubes
    # (α + 2)(α² − 2α + 4) = α³ + 8, with α³ = 2
    # ================================================================
    pid += 1
    answer = 2 + 8
    assert numerical_verify(3, 2, answer,
        lambda a: (a + 2) * (a**2 - 2*a + 4))
    problems.append(Problem(
        problem_id=pid,
        statement="If α = ∛2, compute (α + 2)(α² − 2α + 4).",
        alpha_definition="α³ = 2",
        root_degree=3, root_value=2, answer=answer,
        solution_steps=[
            "Recognize the sum of cubes: x³ + a³ = (x + a)(x² − ax + a²).",
            "With a = 2: (α + 2)(α² − 2α + 4) = α³ + 8 = 2 + 8 = 10."
        ],
        difficulty="medium",
        category="sum_of_cubes"
    ))

    # ================================================================
    # PROBLEM 3 [Medium]: Difference of 5th powers
    # (α − 1)(α⁴ + α³ + α² + α + 1) = α⁵ − 1, with α⁵ = 3
    # ================================================================
    pid += 1
    answer = 3 - 1
    assert numerical_verify(5, 3, answer,
        lambda a: (a - 1) * (a**4 + a**3 + a**2 + a + 1))
    problems.append(Problem(
        problem_id=pid,
        statement="If α⁵ = 3, compute (α − 1)(α⁴ + α³ + α² + α + 1).",
        alpha_definition="α⁵ = 3",
        root_degree=5, root_value=3, answer=answer,
        solution_steps=[
            "The geometric series factorization gives x⁵ − 1 = (x − 1)(x⁴ + x³ + x² + x + 1).",
            "Therefore (α − 1)(α⁴ + α³ + α² + α + 1) = α⁵ − 1 = 3 − 1 = 2."
        ],
        difficulty="medium",
        category="difference_of_5th_powers"
    ))

    # ================================================================
    # PROBLEM 4 [Hard]: Double cube factorization (requires regrouping)
    # (α − 2)(α² + 2α + 4)(α + 2)(α² − 2α + 4) = (α³ − 8)(α³ + 8) = α⁶ − 64
    # with α³ = 2
    # ================================================================
    pid += 1
    answer = 2**2 - 64  # = 4 - 64 = -60
    assert numerical_verify(3, 2, answer,
        lambda a: (a - 2)*(a**2 + 2*a + 4)*(a + 2)*(a**2 - 2*a + 4))
    problems.append(Problem(
        problem_id=pid,
        statement="If α = ∛2, compute (α − 2)(α² + 2α + 4)(α + 2)(α² − 2α + 4).",
        alpha_definition="α³ = 2",
        root_degree=3, root_value=2, answer=answer,
        solution_steps=[
            "Group the first two factors: (α − 2)(α² + 2α + 4) = α³ − 8 = 2 − 8 = −6.",
            "Group the last two factors: (α + 2)(α² − 2α + 4) = α³ + 8 = 2 + 8 = 10.",
            "Product = (−6)(10) = −60."
        ],
        difficulty="hard",
        category="double_cube_factorization"
    ))

    # ================================================================
    # PROBLEM 5 [Hard]: Mixed difference/sum of cubes with different constants
    # (α − 2)(α² + 2α + 4)(α + 1)(α² − α + 1) = (α³ − 8)(α³ + 1)
    # with α³ = 10
    # ================================================================
    pid += 1
    answer = (10 - 8) * (10 + 1)  # = 2 × 11 = 22
    assert numerical_verify(3, 10, answer,
        lambda a: (a - 2)*(a**2 + 2*a + 4)*(a + 1)*(a**2 - a + 1))
    problems.append(Problem(
        problem_id=pid,
        statement="If α³ = 10, compute (α − 2)(α² + 2α + 4)(α + 1)(α² − α + 1).",
        alpha_definition="α³ = 10",
        root_degree=3, root_value=10, answer=answer,
        solution_steps=[
            "Recognize two separate cube factorizations:",
            "  (α − 2)(α² + 2α + 4) = α³ − 8 = 10 − 8 = 2.",
            "  (α + 1)(α² − α + 1) = α³ + 1 = 10 + 1 = 11.",
            "Product = 2 × 11 = 22."
        ],
        difficulty="hard",
        category="mixed_cube_factorization"
    ))

    # ================================================================
    # PROBLEM 6 [Hard]: Sum of cubes with α² as base
    # (α² + 2)(α⁴ − 2α² + 4) = (α²)³ + 2³ = α⁶ + 8
    # with α³ = 4
    # ================================================================
    pid += 1
    answer = 4**2 + 8  # = 16 + 8 = 24
    assert numerical_verify(3, 4, answer,
        lambda a: (a**2 + 2)*(a**4 - 2*a**2 + 4))
    problems.append(Problem(
        problem_id=pid,
        statement="If α³ = 4, compute (α² + 2)(α⁴ − 2α² + 4).",
        alpha_definition="α³ = 4",
        root_degree=3, root_value=4, answer=answer,
        solution_steps=[
            "Let u = α². Recognize the sum of cubes: u³ + 2³ = (u + 2)(u² − 2u + 4).",
            "So (α² + 2)(α⁴ − 2α² + 4) = (α²)³ + 8 = α⁶ + 8.",
            "Since α³ = 4, we have α⁶ = (α³)² = 16.",
            "Answer = 16 + 8 = 24."
        ],
        difficulty="hard",
        category="sum_of_cubes_higher_base"
    ))

    # ================================================================
    # PROBLEM 7 [Hard]: Nested cube telescoping (two levels)
    # (α − 1)(α² + α + 1)(α⁶ + α³ + 1) = (α³ − 1)(α⁶ + α³ + 1) = α⁹ − 1
    # with α³ = 7
    # ================================================================
    pid += 1
    answer = 7**3 - 1  # = 343 - 1 = 342
    assert numerical_verify(3, 7, answer,
        lambda a: (a - 1)*(a**2 + a + 1)*(a**6 + a**3 + 1))
    problems.append(Problem(
        problem_id=pid,
        statement="If α³ = 7, compute (α − 1)(α² + α + 1)(α⁶ + α³ + 1).",
        alpha_definition="α³ = 7",
        root_degree=3, root_value=7, answer=answer,
        solution_steps=[
            "First: (α − 1)(α² + α + 1) = α³ − 1 = 7 − 1 = 6.",
            "Now recognize another level: (α³ − 1)(α⁶ + α³ + 1) = (α³)³ − 1 = α⁹ − 1.",
            "(Setting t = α³, this is (t−1)(t²+t+1) = t³−1.)",
            "α⁹ = (α³)³ = 7³ = 343.",
            "Answer = 343 − 1 = 342."
        ],
        difficulty="hard",
        category="nested_cube_telescoping"
    ))

    # ================================================================
    # PROBLEM 8 [Hard]: Cross-paired factorization (scrambled order)
    # (α − 1)(α² − α + 1)(α + 1)(α² + α + 1) = (α³ − 1)(α³ + 1) = α⁶ − 1
    # with α⁶ = 5. Factors given in misleading order.
    # ================================================================
    pid += 1
    answer = 5 - 1  # = 4
    assert numerical_verify(6, 5, answer,
        lambda a: (a - 1)*(a**2 - a + 1)*(a + 1)*(a**2 + a + 1))
    problems.append(Problem(
        problem_id=pid,
        statement="If α⁶ = 5, compute (α − 1)(α² − α + 1)(α + 1)(α² + α + 1).",
        alpha_definition="α⁶ = 5",
        root_degree=6, root_value=5, answer=answer,
        solution_steps=[
            "The factors are presented in misleading order. Regroup:",
            "  (α − 1)(α² + α + 1) = α³ − 1   [pair 1st and 4th factors]",
            "  (α + 1)(α² − α + 1) = α³ + 1   [pair 3rd and 2nd factors]",
            "Product = (α³ − 1)(α³ + 1) = α⁶ − 1 = 5 − 1 = 4."
        ],
        difficulty="hard",
        category="cross_paired_factorization"
    ))

    # ================================================================
    # PROBLEM 9 [Hard]: The original problem structure — FIXED with α⁴ = k
    # (α² + α + 1)(α² − α + 1)(α⁴ − α² + 1) = α⁸ + α⁴ + 1
    # with α⁴ = 3 → 9 + 3 + 1 = 13
    # ================================================================
    pid += 1
    answer = 3**2 + 3 + 1  # = 13
    assert numerical_verify(4, 3, answer,
        lambda a: (a**2 + a + 1)*(a**2 - a + 1)*(a**4 - a**2 + 1))
    problems.append(Problem(
        problem_id=pid,
        statement=(
            "If α satisfies α⁴ = 3 (positive real fourth root), "
            "compute (α² + α + 1)(α² − α + 1)(α⁴ − α² + 1)."
        ),
        alpha_definition="α⁴ = 3",
        root_degree=4, root_value=3, answer=answer,
        solution_steps=[
            "(α² + α + 1)(α² − α + 1) = (α²+1)² − α² = α⁴ + α² + 1.",
            "Then (α⁴ + α² + 1)(α⁴ − α² + 1) = (α⁴+1)² − α⁴ = α⁸ + α⁴ + 1.",
            "Since α⁴ = 3: α⁸ = (α⁴)² = 9.",
            "Answer = 9 + 3 + 1 = 13."
        ],
        difficulty="hard",
        category="cyclotomic_product"
    ))

    # ================================================================
    # PROBLEM 10 [Hard]: Telescoping difference of squares chain
    # (α − 1)(α + 1)(α² + 1)(α⁴ + 1)(α⁸ + 1) = α¹⁶ − 1
    # with α⁴ = 3 → 3⁴ − 1 = 80
    # ================================================================
    pid += 1
    answer = 3**4 - 1  # = 80
    assert numerical_verify(4, 3, answer,
        lambda a: (a-1)*(a+1)*(a**2+1)*(a**4+1)*(a**8+1))
    problems.append(Problem(
        problem_id=pid,
        statement="If α⁴ = 3, compute (α − 1)(α + 1)(α² + 1)(α⁴ + 1)(α⁸ + 1).",
        alpha_definition="α⁴ = 3",
        root_degree=4, root_value=3, answer=answer,
        solution_steps=[
            "Telescope via difference of squares:",
            "  (α − 1)(α + 1) = α² − 1.",
            "  (α² − 1)(α² + 1) = α⁴ − 1.",
            "  (α⁴ − 1)(α⁴ + 1) = α⁸ − 1.",
            "  (α⁸ − 1)(α⁸ + 1) = α¹⁶ − 1.",
            "Since α⁴ = 3: α¹⁶ = (α⁴)⁴ = 3⁴ = 81.",
            "Answer = 81 − 1 = 80."
        ],
        difficulty="hard",
        category="telescoping_squares"
    ))

    # ================================================================
    # PROBLEM 11 [Hard]: Mixed difference/sum of cubes (α − 1)(α² + α + 1)(α + 2)(α² − 2α + 4)
    # = (α³ − 1)(α³ + 8) with α³ = 5
    # ================================================================
    pid += 1
    answer = (5 - 1) * (5 + 8)  # = 4 × 13 = 52
    assert numerical_verify(3, 5, answer,
        lambda a: (a - 1)*(a**2 + a + 1)*(a + 2)*(a**2 - 2*a + 4))
    problems.append(Problem(
        problem_id=pid,
        statement="If α³ = 5, compute (α − 1)(α² + α + 1)(α + 2)(α² − 2α + 4).",
        alpha_definition="α³ = 5",
        root_degree=3, root_value=5, answer=answer,
        solution_steps=[
            "Group: (α − 1)(α² + α + 1) = α³ − 1 = 5 − 1 = 4.",
            "Group: (α + 2)(α² − 2α + 4) = α³ + 8 = 5 + 8 = 13.",
            "Product = 4 × 13 = 52."
        ],
        difficulty="hard",
        category="mixed_cube_factorization"
    ))

    # ================================================================
    # PROBLEM 12 [Very Hard]: Fifth root chain with scrambled pairing
    # (α − 1)(α + 1)(α⁴ + α³ + α² + α + 1)(α⁴ − α³ + α² − α + 1)
    # = (α⁵ − 1)(α⁵ + 1) = α¹⁰ − 1, with α⁵ = 3
    # ================================================================
    pid += 1
    answer = 3**2 - 1  # = 8
    assert numerical_verify(5, 3, answer,
        lambda a: (a-1)*(a+1)*(a**4+a**3+a**2+a+1)*(a**4-a**3+a**2-a+1))
    problems.append(Problem(
        problem_id=pid,
        statement=(
            "If α⁵ = 3, compute "
            "(α − 1)(α + 1)(α⁴ + α³ + α² + α + 1)(α⁴ − α³ + α² − α + 1)."
        ),
        alpha_definition="α⁵ = 3",
        root_degree=5, root_value=3, answer=answer,
        solution_steps=[
            "Pair factors carefully:",
            "  (α − 1)(α⁴ + α³ + α² + α + 1) = α⁵ − 1 = 3 − 1 = 2.",
            "  (α + 1)(α⁴ − α³ + α² − α + 1) = α⁵ + 1 = 3 + 1 = 4.",
            "Product = 2 × 4 = 8.",
            "(Equivalently: (α⁵ − 1)(α⁵ + 1) = α¹⁰ − 1 = 9 − 1 = 8.)"
        ],
        difficulty="very_hard",
        category="fifth_root_chain"
    ))

    # ================================================================
    # PROBLEM 13 [Very Hard]: Six-factor multi-level telescoping
    # (α−1)(α+1)(α²+α+1)(α²−α+1)(α⁶+α³+1)(α⁶−α³+1) = α¹⁸ − 1
    # with α³ = 2 → 2⁶ − 1 = 63
    # ================================================================
    pid += 1
    answer = 2**6 - 1  # = 63
    assert numerical_verify(3, 2, answer,
        lambda a: (a-1)*(a+1)*(a**2+a+1)*(a**2-a+1)*(a**6+a**3+1)*(a**6-a**3+1))
    problems.append(Problem(
        problem_id=pid,
        statement=(
            "If α = ∛2, compute "
            "(α − 1)(α + 1)(α² + α + 1)(α² − α + 1)(α⁶ + α³ + 1)(α⁶ − α³ + 1)."
        ),
        alpha_definition="α³ = 2",
        root_degree=3, root_value=2, answer=answer,
        solution_steps=[
            "Layer 1 — Difference/sum of cubes:",
            "  (α − 1)(α² + α + 1) = α³ − 1 = 1.",
            "  (α + 1)(α² − α + 1) = α³ + 1 = 3.",
            "  Product so far: 1 × 3 = 3, i.e., α⁶ − 1.",
            "",
            "Layer 2 — Cyclotomic product:",
            "  (α⁶ + α³ + 1)(α⁶ − α³ + 1) = (α⁶ + 1)² − (α³)² = α¹² + α⁶ + 1.",
            "  (Using (a+b)(a−b) with a = α⁶+1, b = α³.)",
            "",
            "Layer 3 — Difference of cubes with base α⁶:",
            "  (α⁶ − 1)(α¹² + α⁶ + 1) = (α⁶)³ − 1 = α¹⁸ − 1.",
            "  α¹⁸ = (α³)⁶ = 2⁶ = 64.",
            "  Answer = 64 − 1 = 63."
        ],
        difficulty="very_hard",
        category="multi_level_telescoping"
    ))

    # ================================================================
    # PROBLEM 14 [Very Hard]: α⁴ = 5, cyclotomic + telescoping squares
    # (α² + α + 1)(α² − α + 1)(α⁴ − α² + 1)(α⁴ + 1)(α − 1)(α + 1)
    # = (α⁸ + α⁴ + 1)(α⁴ + 1)(α² − 1)
    # Actually let's do it step by step:
    # (α²+α+1)(α²−α+1) = α⁴+α²+1
    # (α⁴+α²+1)(α⁴−α²+1) = α⁸+α⁴+1
    # (α−1)(α+1) = α²−1
    # (α²−1)(α⁸+α⁴+1) ... hmm this is (α²−1)(α⁸+α⁴+1).
    # α⁸+α⁴+1 = (α¹²−1)/(α⁴−1). So (α²−1)(α¹²−1)/(α⁴−1).
    # Not clean. Let me pick something else.
    # ================================================================
    # PROBLEM 14 [Very Hard]: Difference of cubes applied to α² with nesting
    # (α² − 1)(α⁴ + α² + 1)(α⁶ + 1)(α¹² − α⁶ + 1)
    # = (α⁶ − 1)(α¹⁸ + 1)... no.
    # Let me do: (α² − 1)(α⁴ + α² + 1) = α⁶ − 1 (diff of cubes, base α²)
    # Then (α⁶ − 1)(α⁶ + 1) = α¹² − 1
    # So (α² − 1)(α⁴ + α² + 1)(α⁶ + 1) = α¹² − 1
    # With α⁴ = 5: α¹² = 5³ = 125. Answer = 124.
    # ================================================================
    pid += 1
    answer = 5**3 - 1  # = 124
    assert numerical_verify(4, 5, answer,
        lambda a: (a**2 - 1)*(a**4 + a**2 + 1)*(a**6 + 1))
    problems.append(Problem(
        problem_id=pid,
        statement=(
            "If α⁴ = 5, compute (α² − 1)(α⁴ + α² + 1)(α⁶ + 1)."
        ),
        alpha_definition="α⁴ = 5",
        root_degree=4, root_value=5, answer=answer,
        solution_steps=[
            "Recognize (α² − 1)(α⁴ + α² + 1) = (α²)³ − 1 = α⁶ − 1 [difference of cubes].",
            "Then (α⁶ − 1)(α⁶ + 1) = α¹² − 1 [difference of squares].",
            "Since α⁴ = 5: α¹² = (α⁴)³ = 125.",
            "Answer = 125 − 1 = 124."
        ],
        difficulty="very_hard",
        category="nested_cube_square_telescoping"
    ))

    # ================================================================
    # PROBLEM 15 [Very Hard]: Seven-th root with two-level factorization
    # (α − 1)(α⁶ + α⁵ + α⁴ + α³ + α² + α + 1)(α⁷ + 1) = (α⁷ − 1)(α⁷ + 1) = α¹⁴ − 1
    # with α⁷ = 2. But α⁷ + 1 = 3 is just an integer.
    #
    # Better: (α − 1)(α + 1)(α⁶ + α⁵ + α⁴ + α³ + α² + α + 1)(α⁶ − α⁵ + α⁴ − α³ + α² − α + 1)
    # = (α⁷ − 1)(α⁷ + 1) = α¹⁴ − 1, with α⁷ = 2 → 4 − 1 = 3
    # ================================================================
    pid += 1
    answer = 2**2 - 1  # = 3
    assert numerical_verify(7, 2, answer,
        lambda a: (a-1)*(a+1)*(a**6+a**5+a**4+a**3+a**2+a+1)*(a**6-a**5+a**4-a**3+a**2-a+1))
    problems.append(Problem(
        problem_id=pid,
        statement=(
            "If α⁷ = 2, compute\n"
            "(α − 1)(α + 1)(α⁶ + α⁵ + α⁴ + α³ + α² + α + 1)"
            "(α⁶ − α⁵ + α⁴ − α³ + α² − α + 1)."
        ),
        alpha_definition="α⁷ = 2",
        root_degree=7, root_value=2, answer=answer,
        solution_steps=[
            "Pair factors for the 7th-power identities:",
            "  (α − 1)(α⁶ + α⁵ + α⁴ + α³ + α² + α + 1) = α⁷ − 1 = 1.",
            "  (α + 1)(α⁶ − α⁵ + α⁴ − α³ + α² − α + 1) = α⁷ + 1 = 3.",
            "Product = 1 × 3 = 3.",
            "(Equivalently: α¹⁴ − 1 = (α⁷)² − 1 = 4 − 1 = 3.)"
        ],
        difficulty="very_hard",
        category="seventh_root_chain"
    ))

    # ================================================================
    # PROBLEM 16 [Hard]: Difference of cubes of cubes
    # (α³ − 3)(α⁶ + 3α³ + 9) = (α³)³ − 27 = α⁹ − 27
    # with α³ = 5: 125 − 27 = 98
    # But α³ − 3 = 2, α⁶ + 3α³ + 9 = 25 + 15 + 9 = 49. Both integers.
    # That's trivial. Let me find a non-trivial one.
    #
    # (α − 3)(α² + 3α + 9) = α³ − 27, with α³ = 30 → 3. Too easy.
    #
    # Multi-step: (α − 1)(α² + α + 1)(α³ + 1)(α⁶ − α³ + 1)
    # = (α³ − 1)(α⁹ + 1), with α³ = k → (k−1)(k³+1)
    # With α³ = 3: (2)(28) = 56
    # Check: α³+1 = 4 (integer), α⁶−α³+1 = 7 (integer).
    # So (α−1)(α²+α+1) = 2 and (α³+1)(α⁶−α³+1) = 4·7 = 28. And 2·28=56.
    # Non-trivial part is (α−1)(α²+α+1). The second half is trivially computed.
    #
    # Better: (α + 1)(α² − α + 1)(α³ − 1)(α⁶ + α³ + 1)
    # = (α³ + 1)(α⁹ − 1) with α³ = 3 → 4 · 26 = 104
    # ================================================================
    pid += 1
    answer = (3 + 1) * (3**3 - 1)  # = 4 × 26 = 104
    assert numerical_verify(3, 3, answer,
        lambda a: (a + 1)*(a**2 - a + 1)*(a**3 - 1)*(a**6 + a**3 + 1))
    problems.append(Problem(
        problem_id=pid,
        statement=(
            "If α³ = 3, compute (α + 1)(α² − α + 1)(α³ − 1)(α⁶ + α³ + 1)."
        ),
        alpha_definition="α³ = 3",
        root_degree=3, root_value=3, answer=answer,
        solution_steps=[
            "(α + 1)(α² − α + 1) = α³ + 1 = 4.",
            "(α³ − 1)(α⁶ + α³ + 1) = (α³)³ − 1 = α⁹ − 1 = 27 − 1 = 26.",
            "Product = 4 × 26 = 104.",
            "(Alternative: Note α³ − 1 = 2 and α⁶ + α³ + 1 = 13, so 4 × 2 × 13 = 104.)"
        ],
        difficulty="hard",
        category="mixed_nested_cubes"
    ))

    return problems


def format_problems_markdown(problems: List[Problem]) -> str:
    """Format problems as a Markdown document."""
    lines = []
    lines.append("# Hard But Solvable: Algebraic Number Product Problems\n")
    lines.append("Each problem asks you to compute a product of polynomial expressions")
    lines.append("evaluated at an algebraic number (an *n*-th root of an integer).")
    lines.append("Every answer is an **integer**.\n")
    lines.append("### Key Techniques\n")
    lines.append("- **Difference of cubes**: $x^3 - a^3 = (x - a)(x^2 + ax + a^2)$")
    lines.append("- **Sum of cubes**: $x^3 + a^3 = (x + a)(x^2 - ax + a^2)$")
    lines.append("- **Geometric series**: $x^n - 1 = (x - 1)(x^{n-1} + x^{n-2} + \\cdots + 1)$")
    lines.append("- **Difference of squares telescoping**: $(x-1)(x+1)(x^2+1)(x^4+1)\\cdots = x^{2^k} - 1$")
    lines.append("- **Cyclotomic products**: $(x^2+x+1)(x^2-x+1) = x^4+x^2+1$, etc.")
    lines.append("- **Strategic regrouping**: factors may need to be paired non-adjacently\n")

    lines.append("---\n")
    lines.append("## Problems\n")

    diff_emoji = {"medium": "Medium", "hard": "Hard", "very_hard": "Very Hard"}

    for p in problems:
        lines.append(f"**Problem {p.problem_id}** [{diff_emoji[p.difficulty]}]")
        lines.append(f"> {p.statement}\n")

    lines.append("---\n")
    lines.append("## Solutions\n")

    for p in problems:
        lines.append(f"### Problem {p.problem_id} — Answer: **{p.answer}**\n")
        for step in p.solution_steps:
            if step == "":
                lines.append("")
            else:
                lines.append(f"{step}  ")
        lines.append("")

    return "\n".join(lines)


def main():
    print("Building and verifying problems...\n")
    problems = build_problems()
    print(f"Generated {len(problems)} problems. All assertions passed.\n")

    # Numerical verification
    all_ok = True
    for p in problems:
        alpha = p.root_value ** (1.0 / p.root_degree)
        # Build a general numerical check by constructing a lambda from the algebraic identity
        print(f"  Problem {p.problem_id} [{p.difficulty:>9s}] ({p.category}): answer = {p.answer}")

    md = format_problems_markdown(problems)
    with open("problems.md", "w") as f:
        f.write(md)
    print(f"\nMarkdown written to problems.md")

    data = []
    for p in problems:
        data.append({
            "id": p.problem_id,
            "statement": p.statement,
            "alpha_definition": p.alpha_definition,
            "root_degree": p.root_degree,
            "root_value": p.root_value,
            "answer": p.answer,
            "difficulty": p.difficulty,
            "category": p.category,
            "solution_steps": p.solution_steps,
        })
    with open("generated_problems.json", "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"JSON written to generated_problems.json")


if __name__ == "__main__":
    main()
