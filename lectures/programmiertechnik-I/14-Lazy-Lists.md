---
marp: true
theme: htwg-pt1
paginate: true
footer: "![](../../themes/htwgin40.png)&nbsp;&nbsp;Prof. Dr. Marko Boger, Prof. Dr. Pascal Laube"
_footer: ""
---

![bg](../../themes/htwgin-titel.png)

### Prof. Dr. Marko Boger, Prof. Dr. Pascal Laube
## Programmiertechnik I
# Lecture 14: Lazy Lists

---

<!-- _class: inhalt -->

<style scoped>
section { font-size: 19px; }
</style>

# Goals

<div class="columns" style="grid-template-columns: 1fr 260px; align-items: start;">
<div markdown="1">

In this lecture you will learn about

- eager vs. lazy evaluation: by-value, by-name, `lazy val`
- sequences and series: dealing with infinity using lazy lists
- Scala's `LazyList` and memoization
- infinite data structures: naturals, Fibonacci, primes
- lazy vs. forcing operations, views and iterators
- live data from the web: HTTP(S), reading URLs, the ISS as an infinite list

Supporting literature:

- Lewis, Art of Programming Using Scala
- Scala docs: Collections – `LazyList`, Views

</div>
<div markdown="1">

<img src="assets/pt12-learn-scala-3-book.png" alt="Book cover: Learn Scala 3 the Fast Way" style="width:240px" />

</div>
</div>

---

<!-- _class: kapitel -->

## 1
# Eager and Lazy Evaluation

When is an expression computed?

---

<style scoped>
section { font-size: 20px; }
pre { font-size: 18px; }
</style>

# Eager Evaluation

**Eager evaluation** means: an expression is computed **as soon as it is reached** – whether or not its value is ever used.

- `val x = e` evaluates `e` **immediately**, at the definition
- Function arguments are evaluated **before** the call, left to right, exactly once (call-by-value)
- Eager collections (`List`, `Vector`, `Array`) compute **all** results of `map` or `filter` at once

```scala
def first(a: Int, b: Int): Int = a           // b is never used

first(1, { println("computing b"); 2 })      // prints "computing b" anyway
val zero = 0
first(1, 10 / zero)                          // ArithmeticException – although b is unused

List(1, 2, 3).map { x => println(s"map $x"); x * 2 }.head
// map 1, map 2, map 3 – all three computed, only the first is needed
```

- **Pro:** predictable order and cost – easy to reason about and to debug
- **Con:** wasted work, and errors or endless loops in values nobody needs
- **Con:** no infinite data – an eager `List` of *all* natural numbers would never finish

---

<style scoped>
section { font-size: 21px; }
</style>

# Lazy Evaluation

A `lazy val` is computed on **first access** and then **cached**.

<div class="columns" style="grid-template-columns: 1fr 1fr; align-items: start;">
<div markdown="1">

```scala
lazy val config =
  println("loading config")
  "ok"

println("before")
println(config)
println(config)
```

</div>
<div markdown="1">

Output:

```text
before
loading config
ok
ok
```

</div>
</div>

| | evaluated | how often |
|---|---|---|
| `val` | at definition | once |
| `lazy val` | at first access | once (cached) |
| `def` / `=> A` | at every access | every time |

---

# Why Laziness?

- **Performance:** never compute what nobody uses
  - "find the first match" stops after the first match
- **Infinite structures:** describe *all* natural numbers, *all* primes – and take only what you need
- **Separation of concerns:** split **generation** of data from its **consumption**
  - the producer describes *what* the values are
  - the consumer decides *how many* it needs
- **Expensive initialization:** load a resource only if needed (`lazy val`)

Laziness is a core idea of functional programming (Haskell is lazy by default).

---

<style scoped>
section { font-size: 19px; }
pre { font-size: 17px; }
table { font-size: 16px; }
</style>

# Call-by-Value vs. Call-by-Name

For function arguments, *eager* and **call-by-value** mean the same thing: the argument is evaluated **before** the call. A parameter of type `=> A` is passed **by name**: it is evaluated each time it is used.

```scala
def expensive(): Int =
  println("computing"); 21

def byValue(use: Boolean, x: Int): Int    = if use then x + x else 0
def byName (use: Boolean, x: => Int): Int = if use then x + x else 0
```

| Call | Output | Result | `x` evaluated |
|---|---|---|---|
| `byValue(false, expensive())` | `computing` | `0` | once – although unused |
| `byName (false, expensive())` | – | `0` | **never** |
| `byValue(true,  expensive())` | `computing` | `42` | once, before the call |
| `byName (true,  expensive())` | `computing` `computing` | `42` | at **every** use – twice |

- by value (eager): evaluated **once**, before the call – even if unused
- by name: evaluated **at every use** – or never

---

<style scoped>
section { font-size: 18px; }
pre { font-size: 16px; }
</style>

# Why Two Strategies?

<div class="columns" style="grid-template-columns: 1fr 1.35fr; align-items: start;">
<div markdown="1">

**Call-by-value** – the default, and the right choice almost always:

- **Predictable:** the argument is computed exactly **once**, at the call site
- **Simple:** side effects and exceptions happen *before* the call – no surprises inside the function
- **Efficient:** a value used many times is not recomputed

**Call-by-name** – when the function decides *if* (or *how often*) the argument is needed:

- **Avoid unnecessary work:** skip expensive or failing computations
- **Own control structures:** `unless`, `repeat`, `retry` look like built-in syntax
- **Infinite data:** the tail of a `LazyList` is passed by name (`#::`)

</div>
<div markdown="1">

```scala
def log(enabled: Boolean, msg: => String): Unit =
  if enabled then println(msg)

log(false, s"state: ${big.mkString(",")}")
                         // string is never built

Some(1).getOrElse(expensive())
                         // getOrElse(default: => B): not computed

def unless(cond: Boolean)(body: => Unit): Unit =
  if !cond then body

unless(list.isEmpty) { println(list.head) }
                         // safe: body runs only if non-empty

1 #:: { println("tail"); LazyList(2) }
                         // tail not computed yet
```

Pitfall: a by-name argument used **twice** is computed twice – cache it with `lazy val v = x`.

</div>
</div>

---

<style scoped>
section { font-size: 20px; }
pre { font-size: 17px; }
</style>

# What Is a Lazy List?

A **lazy list** is a list whose **tail is evaluated on demand** – it is passed *by name* and computed only when someone accesses it. Once computed, an element is **cached**.

- Elements are computed **only when accessed**, and only as far as needed
- So the list can be **potentially infinite**: it describes all elements, but computes only a few

<div class="columns" style="grid-template-columns: 1.3fr 1fr; align-items: start;">
<div markdown="1">

```scala
def from(n: Int): LazyList[Int] =
  println(s"computing $n")
  n #:: from(n + 1)        // tail: by name, not computed yet

val nats = from(1)         // all natural numbers from 1
nats(2)
nats(2)
nats.take(5).toList
nats
```

</div>
<div markdown="1">

Output:

```text
computing 1
computing 2
computing 3                // nats(2) == 3
                           // 2nd access: cached
computing 4
computing 5                // List(1, 2, 3, 4, 5)
LazyList(1, 2, 3, 4, 5, <not computed>)
```

</div>
</div>

More on Scala's `LazyList` on the next slides.

---

# `LazyList` in Scala

A `LazyList` is an immutable linked list – like `List` – but its elements are **computed only when needed**.

- head **and** tail are lazy
- once computed, elements are **memoized** (stored)
- it is a `Seq`: it has `map`, `filter`, `take`, `zip`, … (see Lecture 12)

```scala
val ll = 1 #:: 2 #:: 3 #:: LazyList.empty
println(ll)
```

```text
LazyList(<not computed>)
```

Even the first element has not been computed yet.

> Scala 2.12 had `Stream` (lazy tail only). It is **deprecated since 2.13** – use `LazyList`.

---

<style scoped>
section { font-size: 20px; }
</style>

# Creating LazyLists

```scala
1 #:: 2 #:: 3 #:: LazyList.empty                // like :: for List
LazyList.from(1).take(5).toList                 // List(1, 2, 3, 4, 5)
LazyList.iterate(1)(_ * 2).take(8).toList       // List(1, 2, 4, 8, 16, 32, 64, 128)
LazyList.continually("ha").take(3).mkString     // hahaha
```

Recursive construction with `LazyList.cons` / `LazyList.empty` (compare Lecture 10):

```scala
def countdown(n: Int): LazyList[Int] =
  if n < 0 then LazyList.empty
  else LazyList.cons(n, countdown(n - 1))

countdown(3).toList                             // List(3, 2, 1, 0)
```

The recursive call `countdown(n - 1)` is **not** executed immediately – the tail is passed by name.

---

<style scoped>
.cells { display: flex; gap: 8px; align-items: center; margin: 0.4em 0 0.8em 0; font-family: monospace; font-size: 22px; }
.cell { border: 2px solid #00384f; border-radius: 6px; padding: 6px 14px; background: #d8eef3; }
.todo { border: 2px dashed #999; color: #888; background: #f4f4f4; }
.arrow { color: #00384f; }
section { font-size: 21px; }
</style>

# Evaluated vs. Unevaluated

`val squares = LazyList.from(1).map(n => n * n)` – after creation:

<div class="cells"><span class="cell todo">? (thunk)</span></div>

After `squares.take(3).toList`:

<div class="cells"><span class="cell">1</span><span class="arrow">→</span><span class="cell">4</span><span class="arrow">→</span><span class="cell">9</span><span class="arrow">→</span><span class="cell todo">? (thunk)</span></div>

After `squares.take(4).toList`:

<div class="cells"><span class="cell">1</span><span class="arrow">→</span><span class="cell">4</span><span class="arrow">→</span><span class="cell">9</span><span class="arrow">→</span><span class="cell">16</span><span class="arrow">→</span><span class="cell todo">? (thunk)</span></div>

A **thunk** is a not yet evaluated computation. Evaluated cells stay in memory.

---

<style scoped>
section { font-size: 19px; }
pre { font-size: 16px; }
table { font-size: 17px; }
</style>

# Memoization and Caching

**Memoization:** remember the result of a computation and **reuse** it instead of computing it again. The stored result is the **cache**. It trades **memory** for **time**.

| | evaluated | result |
|---|---|---|
| `def` / `=> A` | at every access | **recomputed** every time |
| `lazy val` | at first access | **cached**, reused afterwards |
| `LazyList` | each element at first access | every cell cached like a `lazy val` |

<div class="columns" style="grid-template-columns: 1.4fr 1fr; align-items: start;">
<div markdown="1">

```scala
def sqDef = LazyList.from(1).map { n => println(s"eval $n"); n * n }
val sqVal = LazyList.from(1).map { n => println(s"eval $n"); n * n }

sqDef(2); sqDef(2)   // new list each time: recomputed
sqVal(2); sqVal(2)   // same list: cached
```

</div>
<div markdown="1">

```text
eval 1  eval 2  eval 3    // sqDef(2)
eval 1  eval 2  eval 3    // sqDef(2) again
eval 1  eval 2  eval 3    // sqVal(2)
                          // sqVal(2): nothing
```

</div>
</div>

Lazy lists **need** memoization: without it, every walk through the list would recompute all elements before it.

---

<style scoped>
section { font-size: 20px; }
</style>

# Memoization in a LazyList

<div class="columns" style="grid-template-columns: 1fr 1fr; align-items: start;">
<div markdown="1">

```scala
val squares = LazyList.from(1).map { n =>
  println(s"eval $n"); n * n
}
println(squares)
println(squares.take(3).toList)
println(squares)
println(squares.take(4).toList)
```

</div>
<div markdown="1">

Output:

```text
LazyList(<not computed>)
eval 1
eval 2
eval 3
List(1, 4, 9)
LazyList(1, 4, 9, <not computed>)
eval 4
List(1, 4, 9, 16)
```

</div>
</div>

- Each element is computed **at most once**
- The second `take(4)` only evaluates the new element `16`

---

<style scoped>
section { font-size: 19px; }
pre { font-size: 17px; }
</style>

# Why Caching Matters: Recompute vs. Cache

The same recursion for Fibonacci numbers – once recomputed, once cached in a `LazyList`:

<div class="columns" style="grid-template-columns: 1fr 1fr; align-items: start;">
<div markdown="1">

**Recomputed** (plain recursion)

```scala
var calls = 0
def fib(n: Int): BigInt =
  calls += 1
  if n < 2 then n else fib(n - 1) + fib(n - 2)

fib(30)     // 832040
calls       // 2692537 calls
```

</div>
<div markdown="1">

**Cached** (memoized in a `LazyList`)

```scala
var steps = 0
lazy val fibs: LazyList[BigInt] =
  LazyList.from(0).map { n =>
    steps += 1
    if n < 2 then n else fibs(n - 1) + fibs(n - 2)
  }

fibs(30)    // 832040, steps == 31
fibs(30)    // cached: steps still 31
fibs(100)   // 354224848179261915075, steps == 101
```

</div>
</div>

- Recomputation grows **exponentially**; with the cache, every element is computed **exactly once**
- Infinite data structures build on earlier elements – caching makes that affordable
- Price: cached elements stay in memory (→ Pitfall 2: holding the head)

---

<!-- _class: kapitel -->

## 2
# Sequences and Series

Dealing with Infinity using Lazy Lists

---

<style scoped>
section { font-size: 21px; }
</style>

# Sequences (Folgen)

A **sequence** assigns a value $a_n$ to every natural number $n$ – it is **infinite** by definition.

$$
a_n = 2n: \ 2, 4, 6, 8, \dots \qquad\qquad b_n = \frac{1}{n}: \ 1, \tfrac12, \tfrac13, \tfrac14, \dots
$$

Nobody writes down *all* elements – we write down the **rule** and look at as many as we need.

```scala
val a = LazyList.from(1).map(n => 2 * n)
val b = LazyList.from(1).map(n => 1.0 / n)

a.take(6).toList   // List(2, 4, 6, 8, 10, 12)
b.take(4).toList   // List(1.0, 0.5, 0.3333333333333333, 0.25)
```

A `LazyList` is the programmer's version of a sequence: an infinite rule, evaluated on demand.

---

<style scoped>
section { font-size: 21px; }
</style>

# Recursively Defined Sequences

Many sequences are defined by a start value and a **recurrence** (Lecture 10):

$$
c_0 = 100, \quad c_{n+1} = \frac{c_n}{2} + 1 \qquad\qquad F_0 = 0,\ F_1 = 1,\ F_{n+2} = F_{n+1} + F_n
$$

`LazyList.iterate(start)(f)` is exactly $x_0,\ f(x_0),\ f(f(x_0)), \dots$

```scala
val c = LazyList.iterate(100.0)(x => x / 2 + 1)
c.take(6).toList   // List(100.0, 51.0, 26.5, 14.25, 8.125, 5.0625)
```

The sequence converges to 2 – we can watch it without ever computing "all" elements.
Fibonacci needs two predecessors – we will build it with `zip` in chapter 3.

---

<style scoped>
section { font-size: 20px; }
</style>

# Series (Reihen) and Partial Sums

A **series** is the sequence of **partial sums** $s_n = \sum_{k=0}^{n} a_k$ of a sequence.

$$
\sum_{k=0}^{\infty} \left(\tfrac12\right)^k = 1 + \tfrac12 + \tfrac14 + \dots = 2
\qquad\qquad
\sum_{k=1}^{\infty} \tfrac1k = 1 + \tfrac12 + \tfrac13 + \dots = \infty
$$

`scanLeft` turns a sequence into its partial sums – lazily:

```scala
val geo = LazyList.from(0).map(k => math.pow(0.5, k)).scanLeft(0.0)(_ + _)
geo.take(6).toList   // List(0.0, 1.0, 1.5, 1.75, 1.875, 1.9375)
geo(30)              // 1.9999999981373549

val harm = LazyList.from(1).map(1.0 / _).scanLeft(0.0)(_ + _)
harm.indexWhere(_ > 5)    // 83
harm.indexWhere(_ > 10)   // 12367
```

The geometric series converges to 2; the harmonic series diverges – but very slowly.

---

<style scoped>
section { font-size: 20px; }
</style>

# Approximating $e$ and $\pi$

$$
e = \sum_{k=0}^{\infty} \frac{1}{k!}
\qquad\qquad
\pi = 4 \sum_{k=0}^{\infty} \frac{(-1)^k}{2k+1} \quad \text{(Leibniz)}
$$

```scala
val facts = LazyList.iterate((0, BigInt(1))) { case (n, f) => (n + 1, f * (n + 1)) }.map(_._2)
val e = facts.map(f => 1.0 / f.toDouble).scanLeft(0.0)(_ + _)
e.take(6).toList   // List(0.0, 1.0, 2.0, 2.5, 2.6666666666666665, 2.708333333333333)
e.zip(e.tail).find((x, y) => (y - x).abs < 1e-12).map(_._2)
                   // Some(2.718281828458995)   math.E = 2.718281828459045

val pi = LazyList.from(0).map(k => (if k % 2 == 0 then 4.0 else -4.0) / (2 * k + 1))
                         .scanLeft(0.0)(_ + _)
pi(10)     // 3.0418396189294032
pi(1000)   // 3.140592653839794
```

**Generation** (the infinite series) is separated from **consumption** (when do we stop?).

---

<!-- _class: kapitel -->

## 3
# Infinite Data Structures

Describe everything, take what you need

---

<style scoped>
section { font-size: 21px; }
</style>

# Fibonacci Numbers with `zip`

Now we can use **lazy evaluation** and **memoization** to compute Fibonacci numbers **faster**.

Mathematically (Lecture 10): $F_0 = 0,\ F_1 = 1,\ F_n = F_{n-1} + F_{n-2}$

```text
fibs          0  1  1  2  3  5  8 ...
fibs.tail     1  1  2  3  5  8 ...
sum           1  2  3  5  8 13 ...   → the rest of fibs
```

```scala
val fibs: LazyList[BigInt] =
  BigInt(0) #:: BigInt(1) #:: fibs.zip(fibs.tail).map((a, b) => a + b)

fibs.take(12).toList   // List(0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89)
fibs(100)              // 354224848179261915075
```

The list is defined **in terms of itself**. Thanks to memoization, `fibs(100)` takes linear time – unlike the naive recursive `fib`.

---

<style scoped>
section { font-size: 21px; }
</style>

# Prime Numbers: Sieve of Eratosthenes

Idea: take the first number $p$, then remove all multiples of $p$ from the rest – repeat.

```scala
def sieve(s: LazyList[Int]): LazyList[Int] =
  s.head #:: sieve(s.tail.filter(_ % s.head != 0))

val primes = sieve(LazyList.from(2))

primes.take(10).toList   // List(2, 3, 5, 7, 11, 13, 17, 19, 23, 29)
```

- A recursive function without a base case – and still no infinite loop
- `#::` takes its right side **by name**: the recursion only proceeds when the next prime is demanded
- (Didactically beautiful, but not the fastest prime algorithm)

---

<!-- _class: kapitel -->

## 4
# Operations

Lazy or forcing? Views and iterators

---

<style scoped>
section { font-size: 21px; }
</style>

# Lazy Operations

These operations return a new `LazyList` **without computing anything**:

```scala
val m = LazyList.from(1).map(_ * 10)
println(m)                 // LazyList(<not computed>)
println(m.take(3))         // LazyList(<not computed>)
println(m.take(3).toList)  // List(10, 20, 30)
```

| Operation | Example | Result (after `toList`) |
|---|---|---|
| `map`, `filter` | `from(1).map(_ * 10)` | 10, 20, 30, … |
| `take(n)` | `from(1).take(3)` | 1, 2, 3 |
| `drop(n)` | `from(1).drop(3).take(3)` | 4, 5, 6 |
| `takeWhile(p)` | `from(1).takeWhile(n => n * n < 50)` | 1 … 7 |
| `dropWhile(p)` | `from(1).dropWhile(_ < 5).head` | 5 |
| `zip` | `from(1).zip(LazyList("a","b","c"))` | (1,a), (2,b), (3,c) |

---

# Forcing Operations

These operations **evaluate** elements – some or all:

| Operation | Evaluates |
|---|---|
| `head`, `tail` | the first cell |
| `apply(n)`, `find`, `exists` | until the answer is known |
| `toList`, `length`, `sum`, `max` | **everything** |
| `foldLeft`, `foreach`, `mkString` | **everything** |

```scala
val nats = LazyList.from(0)
nats.head                    // 0
nats.tail.head               // 1
nats.find(n => n * n > 1000) // Some(32)
```

Rule of thumb: first **limit** (`take`, `takeWhile`), then **force**.

---

<style scoped>
section { font-size: 21px; }
</style>

# Pitfall 1: Forcing an Infinite List

```scala
LazyList.from(1).length          // never terminates
LazyList.from(1).toList          // OutOfMemoryError
LazyList.from(1).foldLeft(0)(_ + _)   // never terminates
LazyList.from(1).filter(_ < 0).head   // searches forever
```

- Forcing operations need **all** elements – there is no "all" for an infinite list
- `filter` can make a list **effectively empty**: `head` keeps searching

Fix: limit first.

```scala
LazyList.from(1).take(100).sum   // 5050
```

---

# Pitfall 2: Holding the Head

Memoization means: **evaluated cells stay in memory** as long as someone references the head.

```scala
val nats = LazyList.from(1)        // nats references the head
nats.drop(100_000_000).head        // all 100 million cells are kept!
```

```scala
LazyList.from(1).drop(100_000_000).head   // no reference: cells can be garbage collected
```

- A `val` holding a large `LazyList` keeps everything that was evaluated
- Prefer `def` or local expressions for big or infinite lists
- If you only need one pass, use an `Iterator` or a view

---

<style scoped>
section { font-size: 21px; }
</style>

# Views

`.view` turns any collection into a **lazy** one – without memoization.

```scala
val v = (1 to 1_000_000).view
  .map(_ * 2)
  .filter(_ % 3 == 0)

v.take(3).toList     // List(6, 12, 18)
```

- No intermediate collections of a million elements are created
- Each element flows through the whole pipeline, one at a time
- Only 9 elements are touched to get the first 3 results
- Results are **not** cached: forcing the view twice computes twice

Use views for **chains of transformations** on large eager collections.

---

# Iterators

An `Iterator` produces elements one by one – and can be traversed **only once**.

```scala
val it = Iterator.from(1).map(_ * 2)
it.take(3).toList         // List(2, 4, 6)

val it2 = Iterator(1, 2, 3)
println(it2.sum)          // 6
println(it2.sum)          // 0  – already consumed!
```

| | lazy | memoized | reusable |
|---|---|---|---|
| `List` | no | – | yes |
| `LazyList` | yes | yes | yes |
| view | yes | no | yes |
| `Iterator` | yes | no | **no** |

---

<!-- _class: kapitel -->

## 5
# Live Data from the Web

Reading URLs – and an infinite list of ISS readings

---

<style scoped>
section { font-size: 21px; }
</style>

# HTTP and HTTPS

The web is built on **requests** and **responses**: a client asks a server for a resource, the server answers.

```text
https://api.wheretheiss.at/v1/satellites/25544
└─┬─┘   └───────┬────────┘└──────────┬────────┘
scheme        host                 path
```

- **HTTP** (Hypertext Transfer Protocol): the client sends e.g. `GET /v1/satellites/25544`
- The server answers with a **status code** and a **body**:
  `200` OK · `404` Not Found · `429` Too Many Requests · `500` Server Error
- **HTTPS** = HTTP over an encrypted **TLS** connection – nobody in between can read or change the data
- Web APIs usually answer with **JSON** instead of HTML – data for programs, not for people

Try it in the browser or in the terminal: `curl https://api.wheretheiss.at/v1/satellites/25544`

---

<style scoped>
section { font-size: 20px; }
pre { font-size: 16px; }
</style>

# Reading a URL in Scala

`scala.io.Source` reads a URL just like a file – one `GET` request, the body as a `String`:

```scala
import scala.io.Source
import scala.util.Using

val url  = "https://api.wheretheiss.at/v1/satellites/25544"
val json = Source.fromURL(url).mkString
// {"name":"iss","id":25544,"latitude":36.620444280425,"longitude":32.206393295839,
//  "altitude":421.37534450492,"velocity":27587.23954958,"visibility":"eclipsed",
//  ..., "timestamp":1794949105, ..., "units":"kilometers"}
```

The network can fail – `Using` closes the connection and returns a `Try`:

```scala
Using(Source.fromURL(url))(_.mkString)                    // Success({"name":"iss",...})
Using(Source.fromURL(".../v1/satellites/1"))(_.mkString)  // Failure(FileNotFoundException) – 404
Using(Source.fromURL("https://no-such-host.invalid/"))(_.mkString)
                                                          // Failure(UnknownHostException)
```

- Every call is a **new request** – and a new, current answer

---

<style scoped>
section { font-size: 21px; }
pre { font-size: 18px; }
</style>

# The ISS API: One Reading

[Where the ISS at](https://wheretheiss.at/w/developer) – no API key, about one request per second.
We only need five fields of the JSON answer:

```scala
case class IssReading(time: Long, lat: Double, lon: Double, altitude: Double, velocity: Double)

def field(json: String, name: String): Double =          // minimal JSON parsing
  raw""""$name":(-?[\d.]+)""".r.findFirstMatchIn(json).get.group(1).toDouble

def fetch(): IssReading =
  val json = Source.fromURL(url).mkString
  IssReading(field(json, "timestamp").toLong, field(json, "latitude"),
             field(json, "longitude"), field(json, "altitude"), field(json, "velocity"))

fetch()
// IssReading(1794949107,36.538001859539,32.321938104627,421.37033549686,27587.194775299)
```

- `altitude` in km, `velocity` in km/h, `timestamp` in seconds since 1970
- `fetch()` has a **side effect**: each call gives a different reading

---

<style scoped>
section { font-size: 19px; }
pre { font-size: 16px; }
</style>

# The ISS as a `LazyList`

A `LazyList` does not have to be computed – each element can be a **new reading from a data source**:

```scala
var requests = 0
def counted(): IssReading = { requests += 1; fetch() }       // fetch() from the previous slide

val iss: LazyList[IssReading] = LazyList.continually { Thread.sleep(1000); counted() }

requests                                     // 0 – defining the list fetches nothing
iss(2).altitude                              // 421.56… – fetches readings 0, 1, 2
requests                                     // 3
iss(1).velocity                              // 27588.9… – cached, no new request
iss.take(3).map(r => (r.lat, r.lon)).toList  // all cached
requests                                     // still 3
```

- **Lazy evaluation:** an endless sensor feed becomes a list – you only fetch what you access
- **Memoization:** every reading is fetched **once**; repeated access reuses the cached value
- Each element is a **snapshot** taken at the moment it was first demanded

---

<style scoped>
section { font-size: 21px; }
pre { font-size: 19px; }
</style>

# Sliding Windows: Average Velocity

`sliding(n)` groups a sequence into overlapping windows of `n` consecutive elements:

```scala
def readings: LazyList[IssReading] =
  LazyList.continually { Thread.sleep(1000); fetch() }  // one request per second

val velocities = readings.map(_.velocity)

val averages = velocities.sliding(60).map(w => w.sum / w.size)
                                         // one window = last 60 readings = 1 minute

averages.take(3).foreach(println)        // waits ~62 s, then prints 3 averages
```

- Nothing is fetched until `take(3)` and `foreach` **demand** values
- `sliding` on a `LazyList` returns an `Iterator` of windows – also lazy
- `readings` is a `def`, not a `val`: a `val` would **memoize** every reading forever (Pitfall 2: holding the head)

---

<!-- _class: inhalt -->

<style scoped>
section { font-size: 22px; }
</style>

# Summary

- Eager: evaluate now. Lazy: evaluate when needed
- Sequences and series are infinite rules – `LazyList`, `iterate` and `scanLeft` model them
- By-name parameters `=> A` and `lazy val` are Scala's building blocks for laziness
- `LazyList` is a lazy, memoized, immutable list; `Stream` is deprecated
- Infinite structures: naturals, Fibonacci via `zip`, prime sieve
- `map`, `filter`, `take`, `drop`, `zip` are lazy; `toList`, `length`, `foldLeft` force
- Limit first, then force – and do not hold on to the head
- Views and iterators: lazy, but not memoized
- HTTPS and `Source.fromURL`: a web API as a lazy, memoized, infinite list

---

<!-- _class: aufgabe -->

# Task

**Build your own ISS pipeline** with the live data from the slides:


1. Write `fetch()` and an infinite `LazyList[IssReading]` with `LazyList.continually`
2. Test with small numbers first: `take(5)` and `sliding(3)` – not `sliding(60)`
3. Compute the average `velocity` and `altitude` per window
4. Extension: estimate the distance flown between two readings from `lat`/`lon` and compare it with `velocity`

<p class="small"><b>Rate limit:</b> about one request per second – always keep the <code>Thread.sleep(1000)</code> and never call <code>toList</code> or <code>sum</code> on the infinite list.</p>

---

<!-- _class: abschluss -->

# Questions?

## Thank you!

marko.boger@htwg-konstanz.de
