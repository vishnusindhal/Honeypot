# Hard But Solvable: Algebraic Number Product Problems

Each problem asks you to compute a product of polynomial expressions
evaluated at an algebraic number (an *n*-th root of an integer).
Every answer is an **integer**.

### Key Techniques

- **Difference of cubes**: $x^3 - a^3 = (x - a)(x^2 + ax + a^2)$
- **Sum of cubes**: $x^3 + a^3 = (x + a)(x^2 - ax + a^2)$
- **Geometric series**: $x^n - 1 = (x - 1)(x^{n-1} + x^{n-2} + \cdots + 1)$
- **Difference of squares telescoping**: $(x-1)(x+1)(x^2+1)(x^4+1)\cdots = x^{2^k} - 1$
- **Cyclotomic products**: $(x^2+x+1)(x^2-x+1) = x^4+x^2+1$, etc.
- **Strategic regrouping**: factors may need to be paired non-adjacently

---

## Problems

**Problem 1** [Medium]
> If α satisfies α³ = 5, compute (α − 1)(α² + α + 1).

**Problem 2** [Medium]
> If α = ∛2, compute (α + 2)(α² − 2α + 4).

**Problem 3** [Medium]
> If α⁵ = 3, compute (α − 1)(α⁴ + α³ + α² + α + 1).

**Problem 4** [Hard]
> If α = ∛2, compute (α − 2)(α² + 2α + 4)(α + 2)(α² − 2α + 4).

**Problem 5** [Hard]
> If α³ = 10, compute (α − 2)(α² + 2α + 4)(α + 1)(α² − α + 1).

**Problem 6** [Hard]
> If α³ = 4, compute (α² + 2)(α⁴ − 2α² + 4).

**Problem 7** [Hard]
> If α³ = 7, compute (α − 1)(α² + α + 1)(α⁶ + α³ + 1).

**Problem 8** [Hard]
> If α⁶ = 5, compute (α − 1)(α² − α + 1)(α + 1)(α² + α + 1).

**Problem 9** [Hard]
> If α satisfies α⁴ = 3 (positive real fourth root), compute (α² + α + 1)(α² − α + 1)(α⁴ − α² + 1).

**Problem 10** [Hard]
> If α⁴ = 3, compute (α − 1)(α + 1)(α² + 1)(α⁴ + 1)(α⁸ + 1).

**Problem 11** [Hard]
> If α³ = 5, compute (α − 1)(α² + α + 1)(α + 2)(α² − 2α + 4).

**Problem 12** [Very Hard]
> If α⁵ = 3, compute (α − 1)(α + 1)(α⁴ + α³ + α² + α + 1)(α⁴ − α³ + α² − α + 1).

**Problem 13** [Very Hard]
> If α = ∛2, compute (α − 1)(α + 1)(α² + α + 1)(α² − α + 1)(α⁶ + α³ + 1)(α⁶ − α³ + 1).

**Problem 14** [Very Hard]
> If α⁴ = 5, compute (α² − 1)(α⁴ + α² + 1)(α⁶ + 1).

**Problem 15** [Very Hard]
> If α⁷ = 2, compute
(α − 1)(α + 1)(α⁶ + α⁵ + α⁴ + α³ + α² + α + 1)(α⁶ − α⁵ + α⁴ − α³ + α² − α + 1).

**Problem 16** [Hard]
> If α³ = 3, compute (α + 1)(α² − α + 1)(α³ − 1)(α⁶ + α³ + 1).

---

## Solutions

### Problem 1 — Answer: **4**

Recognize the difference of cubes: x³ − 1 = (x − 1)(x² + x + 1).  
Therefore (α − 1)(α² + α + 1) = α³ − 1 = 5 − 1 = 4.  

### Problem 2 — Answer: **10**

Recognize the sum of cubes: x³ + a³ = (x + a)(x² − ax + a²).  
With a = 2: (α + 2)(α² − 2α + 4) = α³ + 8 = 2 + 8 = 10.  

### Problem 3 — Answer: **2**

The geometric series factorization gives x⁵ − 1 = (x − 1)(x⁴ + x³ + x² + x + 1).  
Therefore (α − 1)(α⁴ + α³ + α² + α + 1) = α⁵ − 1 = 3 − 1 = 2.  

### Problem 4 — Answer: **-60**

Group the first two factors: (α − 2)(α² + 2α + 4) = α³ − 8 = 2 − 8 = −6.  
Group the last two factors: (α + 2)(α² − 2α + 4) = α³ + 8 = 2 + 8 = 10.  
Product = (−6)(10) = −60.  

### Problem 5 — Answer: **22**

Recognize two separate cube factorizations:  
  (α − 2)(α² + 2α + 4) = α³ − 8 = 10 − 8 = 2.  
  (α + 1)(α² − α + 1) = α³ + 1 = 10 + 1 = 11.  
Product = 2 × 11 = 22.  

### Problem 6 — Answer: **24**

Let u = α². Recognize the sum of cubes: u³ + 2³ = (u + 2)(u² − 2u + 4).  
So (α² + 2)(α⁴ − 2α² + 4) = (α²)³ + 8 = α⁶ + 8.  
Since α³ = 4, we have α⁶ = (α³)² = 16.  
Answer = 16 + 8 = 24.  

### Problem 7 — Answer: **342**

First: (α − 1)(α² + α + 1) = α³ − 1 = 7 − 1 = 6.  
Now recognize another level: (α³ − 1)(α⁶ + α³ + 1) = (α³)³ − 1 = α⁹ − 1.  
(Setting t = α³, this is (t−1)(t²+t+1) = t³−1.)  
α⁹ = (α³)³ = 7³ = 343.  
Answer = 343 − 1 = 342.  

### Problem 8 — Answer: **4**

The factors are presented in misleading order. Regroup:  
  (α − 1)(α² + α + 1) = α³ − 1   [pair 1st and 4th factors]  
  (α + 1)(α² − α + 1) = α³ + 1   [pair 3rd and 2nd factors]  
Product = (α³ − 1)(α³ + 1) = α⁶ − 1 = 5 − 1 = 4.  

### Problem 9 — Answer: **13**

(α² + α + 1)(α² − α + 1) = (α²+1)² − α² = α⁴ + α² + 1.  
Then (α⁴ + α² + 1)(α⁴ − α² + 1) = (α⁴+1)² − α⁴ = α⁸ + α⁴ + 1.  
Since α⁴ = 3: α⁸ = (α⁴)² = 9.  
Answer = 9 + 3 + 1 = 13.  

### Problem 10 — Answer: **80**

Telescope via difference of squares:  
  (α − 1)(α + 1) = α² − 1.  
  (α² − 1)(α² + 1) = α⁴ − 1.  
  (α⁴ − 1)(α⁴ + 1) = α⁸ − 1.  
  (α⁸ − 1)(α⁸ + 1) = α¹⁶ − 1.  
Since α⁴ = 3: α¹⁶ = (α⁴)⁴ = 3⁴ = 81.  
Answer = 81 − 1 = 80.  

### Problem 11 — Answer: **52**

Group: (α − 1)(α² + α + 1) = α³ − 1 = 5 − 1 = 4.  
Group: (α + 2)(α² − 2α + 4) = α³ + 8 = 5 + 8 = 13.  
Product = 4 × 13 = 52.  

### Problem 12 — Answer: **8**

Pair factors carefully:  
  (α − 1)(α⁴ + α³ + α² + α + 1) = α⁵ − 1 = 3 − 1 = 2.  
  (α + 1)(α⁴ − α³ + α² − α + 1) = α⁵ + 1 = 3 + 1 = 4.  
Product = 2 × 4 = 8.  
(Equivalently: (α⁵ − 1)(α⁵ + 1) = α¹⁰ − 1 = 9 − 1 = 8.)  

### Problem 13 — Answer: **63**

Layer 1 — Difference/sum of cubes:  
  (α − 1)(α² + α + 1) = α³ − 1 = 1.  
  (α + 1)(α² − α + 1) = α³ + 1 = 3.  
  Product so far: 1 × 3 = 3, i.e., α⁶ − 1.  

Layer 2 — Cyclotomic product:  
  (α⁶ + α³ + 1)(α⁶ − α³ + 1) = (α⁶ + 1)² − (α³)² = α¹² + α⁶ + 1.  
  (Using (a+b)(a−b) with a = α⁶+1, b = α³.)  

Layer 3 — Difference of cubes with base α⁶:  
  (α⁶ − 1)(α¹² + α⁶ + 1) = (α⁶)³ − 1 = α¹⁸ − 1.  
  α¹⁸ = (α³)⁶ = 2⁶ = 64.  
  Answer = 64 − 1 = 63.  

### Problem 14 — Answer: **124**

Recognize (α² − 1)(α⁴ + α² + 1) = (α²)³ − 1 = α⁶ − 1 [difference of cubes].  
Then (α⁶ − 1)(α⁶ + 1) = α¹² − 1 [difference of squares].  
Since α⁴ = 5: α¹² = (α⁴)³ = 125.  
Answer = 125 − 1 = 124.  

### Problem 15 — Answer: **3**

Pair factors for the 7th-power identities:  
  (α − 1)(α⁶ + α⁵ + α⁴ + α³ + α² + α + 1) = α⁷ − 1 = 1.  
  (α + 1)(α⁶ − α⁵ + α⁴ − α³ + α² − α + 1) = α⁷ + 1 = 3.  
Product = 1 × 3 = 3.  
(Equivalently: α¹⁴ − 1 = (α⁷)² − 1 = 4 − 1 = 3.)  

### Problem 16 — Answer: **104**

(α + 1)(α² − α + 1) = α³ + 1 = 4.  
(α³ − 1)(α⁶ + α³ + 1) = (α³)³ − 1 = α⁹ − 1 = 27 − 1 = 26.  
Product = 4 × 26 = 104.  
(Alternative: Note α³ − 1 = 2 and α⁶ + α³ + 1 = 13, so 4 × 2 × 13 = 104.)  
