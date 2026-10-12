---
marp: true
theme: htwg
paginate: true
_paginate: false
footer: "![](../../themes/htwgin40.png)&nbsp;&nbsp;Prof. Dr. Marko Boger, Prof. Dr. Pascal Laube"
_footer: ""
---

![bg](../../themes/htwgin-titel.png)

### Prof. Dr. Marko Boger, Prof. Dr. Pascal Laube
## Programmiertechnik I
# Lecture 26: LeetCode II: Medium and Hard

<p class="small">Six problems with rising difficulty – continuing Lecture 25</p>

---

<!-- _class: inhalt -->

<style scoped>
section { font-size: 20px; }
</style>

# Goals

In this lecture you will

- solve **five Medium** and **one Hard** LeetCode problem
- first write the **obvious** (slow) solution, then find the **better idea**
- see how **complexity** grows: $O(n^2)$ → $O(n)$, exponential → dynamic programming
- group and count with `groupMapReduce` (Lecture 19) and meet its little brother `groupBy`
- carry a **state** through `foldLeft`, recurse over a **grid**, use a `Set` as a work list
- compare with **Python** and **Java** where it helps

---

<style scoped>
section { font-size: 22px; }
</style>

# Overview

Same routine as in Lecture 25: problem → **What do we need to do?** → solutions

| # | Problem | LeetCode | Level | Main idea |
|---|---|---|---|---|
| 1 | Group Anagrams | 49 | Medium | a good **key** for grouping |
| 2 | Top K Frequent Elements | 347 | Medium | count, then sort – or buckets |
| 3 | Longest Substring Without Repeating Characters | 3 | Medium | sliding window in a `foldLeft` |
| 4 | Coin Change | 322 | Medium | recursion → dynamic programming |
| 5 | Number of Islands | 200 | Medium | flood fill on a grid |
| 6 | Trapping Rain Water | 42 | **Hard** | "max so far" from both sides |

---

<!-- _class: kapitel -->

## 1
# Group Anagrams

LeetCode 49 · Medium

---

# Problem 1: Group Anagrams

Two words are **anagrams** if they consist of exactly the same letters, just in a different order: `listen` – `silent`.

Given a list of words, put all anagrams into **groups**. The order of the groups and inside the groups does not matter.

**Input:** `words: List[String]` · **Output:** `List[List[String]]`

**Example:**
`List("listen", "stone", "silent", "notes", "tea", "enlist", "onset")`
→ `List(List("listen", "silent", "enlist"), List("stone", "notes", "onset"), List("tea"))`

<p class="small">LeetCode 49: <a href="https://leetcode.com/problems/group-anagrams/">Group Anagrams</a> (Medium) – statement paraphrased, examples our own. Code tested with Scala 3.9.0.</p>

---

# What Do We Need to Do?

- Comparing **every pair** of words is slow. Can we give each word a **key** so that anagrams get the *same* key?
- Candidates: the sorted letters (`"listen".sorted == "eilnst"`), or the count of each letter
- Grouping by a key – which collection method from Lecture 19 does that?
- `groupMapReduce(key)(map)(reduce)`: what should `map` and `reduce` be if we want to keep the **words**?

---

<style scoped>
section { font-size: 17px; }
</style>

# Group Anagrams: `groupMapReduce` and `groupBy` (1/2)

```scala
def groupAnagrams(words: List[String]): List[List[String]] =
  words.groupMapReduce(_.sorted)(w => List(w))(_ ++ _).values.toList
```

Key: sorted letters. Each word becomes a one-element list, `++` joins the lists of a group

---

<style scoped>
section { font-size: 17px; }
</style>

# Group Anagrams: `groupMapReduce` and `groupBy` (2/2)

```scala
def groupAnagramsBy(words: List[String]): List[List[String]] =
  words.groupBy(_.sorted).values.toList
```

**New:** `groupBy(key)` is exactly `groupMapReduce(key)(x => List(x))(_ ++ _)` – a `Map[K, List[A]]`

---

<style scoped>
section { font-size: 20px; }
</style>

# Comparison: Python

<div class="columns" style="grid-template-columns: 1.3fr 1fr; align-items: start;">
<div>

```python
def group_anagrams(words):
    groups = {}
    for w in words:
        key = "".join(sorted(w))   # sorted gives a list of chars
        groups.setdefault(key, []).append(w)
    return list(groups.values())
```

</div>
<div>

- No `groupBy` built in: we fill a mutable `dict` ourselves
- `sorted(w)` returns a **list** of characters, `"".join(…)` glues it back into a string (Lecture 02: `join`)
- `setdefault(key, [])` = "get, or insert an empty list" – then `append` changes that list **in place**

</div>
</div>

<p class="small">Tested with Python 3 on the example above.</p>

---

<!-- _class: kapitel -->

## 2
# Top K Frequent Elements

LeetCode 347 · Medium

---

# Problem 2: Top K Frequent Elements

Given a list of numbers and a number `k`, return the `k` numbers that occur **most often**. The order of the result does not matter.

**Input:** `nums: List[Int]`, `k: Int` · **Output:** `List[Int]`

**Example:** `nums = List(4, 1, 4, 7, 1, 4, 9, 1, 4)`, `k = 2` → `List(4, 1)`
(`4` occurs 4 times, `1` occurs 3 times, `7` and `9` once)

LeetCode asks for **better than** $O(n \log n)$ – sorting all counts is not allowed.

<p class="small">LeetCode 347: <a href="https://leetcode.com/problems/top-k-frequent-elements/">Top K Frequent Elements</a> (Medium) – statement paraphrased, examples our own. Code tested with Scala 3.9.0.</p>

---

# What Do We Need to Do?

- Step 1: **count** every number. We did that for saillog: `groupMapReduce` (Lecture 19)
- Step 2: the `k` numbers with the highest counts. The easy way: sort by count
- Sorting costs $O(n \log n)$. Can we avoid it?
- Observation: a count lies between `1` and `n`. What if we make one **bucket per count**?
- Then walk the buckets from `n` down to `1` and take numbers until we have `k`

---

<style scoped>
section { font-size: 16px; }
</style>

# Top K: Sort vs. Buckets (1/2)

```scala
def topKFrequent(nums: List[Int], k: Int): List[Int] =
  nums.groupMapReduce(identity)(_ => 1)(_ + _)
    .toList
    .sortBy((_, count) => -count)
    .take(k)
    .map((n, _) => n)
```

`sortBy` with a negative count → descending (Lecture 20)

---

<style scoped>
section { font-size: 16px; }
</style>

# Top K: Sort vs. Buckets (2/2)

```scala
def topKBuckets(nums: List[Int], k: Int): List[Int] =
  val counts = nums.groupMapReduce(identity)(_ => 1)(_ + _)
  val buckets = counts.groupMapReduce((_, c) => c)((n, _) => List(n))(_ ++ _)
  (nums.length to 1 by -1).toList
    .flatMap(c => buckets.getOrElse(c, Nil))
    .take(k)
```

Buckets: count → numbers. `to 1 by -1` walks downwards; no sorting, $O(n)$

---

<!-- _class: kapitel -->

## 3
# Longest Substring Without Repeating Characters

LeetCode 3 · Medium

---

# Problem 3: Longest Substring Without Repeating Characters

Find the length of the longest **contiguous** part of a string in which **no character appears twice**.

**Input:** `s: String` · **Output:** `Int`

**Examples:**
- `"konstanz"` → `6`: `"konsta"` – the next `n` would be the second one
- `"aaaa"` → `1` · `""` → `0`
- `"abba"` → `2` – a tricky one, see next slide

<p class="small">LeetCode 3: <a href="https://leetcode.com/problems/longest-substring-without-repeating-characters/">Longest Substring Without Repeating Characters</a> (Medium) – statement paraphrased, examples our own. Code tested with Scala 3.9.0.</p>

---

# What Do We Need to Do?

- Brute force: all substrings, keep those whose `distinct` equals themselves. How many substrings are there?
- Better: a **window** `[start, i]` that we slide over the string
  - extend it to the right with every character
  - if the new character is already **inside** the window, move `start` behind its last position
- What do we need to remember? → for each character its **last index**: a `Map[Char, Int]`
- `"abba"`: when we reach the last `a`, its old position is already **left of** `start` – it must not move `start` back!

---

<style scoped>
section { font-size: 15px; }
</style>

# Longest Substring: All Substrings vs. Sliding Window (1/2)

```scala
def lengthBrute(s: String): Int =
  val lengths =
    for
      i <- 0 until s.length
      j <- i to s.length
      sub = s.substring(i, j)
      if sub.distinct == sub
    yield sub.length
  lengths.maxOption.getOrElse(0)
```

$O(n^3)$: fine for a test, too slow for LeetCode

---

<style scoped>
section { font-size: 15px; }
</style>

# Longest Substring: All Substrings vs. Sliding Window (2/2)

```scala
def lengthOfLongestSubstring(s: String): Int =
  val (_, _, best) = s.zipWithIndex.foldLeft((0, Map.empty[Char, Int], 0)) {
    case ((start, last, best), (c, i)) =>
      val newStart = last.get(c) match
        case Some(j) if j >= start => j + 1
        case _                     => start
      (newStart, last + (c -> i), math.max(best, i - newStart + 1))
  }
  best
```

State of the fold: `(start, last, best)`. The guard `j >= start` handles `"abba"`

---

<!-- _class: kapitel -->

## 4
# Coin Change

LeetCode 322 · Medium

---

# Problem 4: Coin Change

You have coins of some values, of each value as many as you like. What is the **smallest number of coins** that add up exactly to an amount? If it is impossible, say so.

**Input:** `coins: List[Int]`, `amount: Int` · **Output:** `Option[Int]` (LeetCode: `-1` for "impossible")

**Examples:**
- `coins = List(1, 2, 5)`, `amount = 11` → `Some(3)`: `5 + 5 + 1`
- `coins = List(2, 5)`, `amount = 8` → `Some(4)`: `2 + 2 + 2 + 2` – greedy `5` first fails!
- `coins = List(2)`, `amount = 3` → `None`

<p class="small">LeetCode 322: <a href="https://leetcode.com/problems/coin-change/">Coin Change</a> (Medium) – statement paraphrased, examples our own. Code tested with Scala 3.9.0.</p>

---

# What Do We Need to Do?

- **Greedy** (always the largest coin) fails for `List(2, 5)` and `8`. Why?
- Recursive thinking (Lecture 10): if the **last coin** is `c`, the rest is the best solution for `amount - c`
- So: try every coin, take the minimum, add 1. Base cases: `0` → `Some(0)`, negative → `None`
- This recomputes the same amounts again and again – like naive Fibonacci (Lecture 10)
- **Dynamic programming:** compute the answers for `0, 1, 2, …, amount` in order and **store** them in a `Vector`

---

<style scoped>
section { font-size: 15px; }
</style>

# Coin Change: Recursion vs. Dynamic Programming (1/2)

```scala
def coinChangeRec(coins: List[Int], amount: Int): Option[Int] =
  if amount == 0 then Some(0)
  else if amount < 0 then None
  else
    coins.flatMap(c => coinChangeRec(coins, amount - c)).minOption.map(_ + 1)
```

Exponential – already slow for `amount = 40`. `minOption` is the twin of `maxOption` (Lecture 20)

---

<style scoped>
section { font-size: 15px; }
</style>

# Coin Change: Recursion vs. Dynamic Programming (2/2)

```scala
def coinChange(coins: List[Int], amount: Int): Option[Int] =
  val best = (1 to amount).foldLeft(Vector(Option(0))) { (dp, a) =>
    val options = coins.filter(_ <= a).flatMap(c => dp(a - c))
    dp :+ options.minOption.map(_ + 1)
  }
  best(amount)
```

`dp(a)` = best for amount `a`. `foldLeft` appends one answer per amount: $O(amount \cdot coins)$

---

<!-- _class: kapitel -->

## 5
# Number of Islands

LeetCode 200 · Medium

---

<style scoped>
section { font-size: 22px; }
</style>

# Problem 5: Number of Islands

<div class="columns" style="grid-template-columns: 1.5fr 1fr; align-items: start;">
<div>

A map is a grid of `'1'` (land) and `'0'` (water). Land cells that touch **horizontally or vertically** form one island. Count the islands.

**Input:** `grid: Vector[String]` (one string per row) · **Output:** `Int`

**Example:** the grid on the right has **4** islands – the two cells at the bottom right only touch diagonally.

</div>
<div>

```text
1 1 0 0 0
1 1 0 1 0
0 0 0 1 0
0 1 0 0 1
```

</div>
</div>

<p class="small">LeetCode 200: <a href="https://leetcode.com/problems/number-of-islands/">Number of Islands</a> (Medium) – statement paraphrased, examples our own. Code tested with Scala 3.9.0.</p>

---

# What Do We Need to Do?

- Walk over all cells. Each time we find land we have **not visited**, we found a new island
- Then mark the **whole island** as visited: its neighbours, their neighbours, … – a **flood fill**
- How do we remember what is visited without changing the grid? → keep a `Set` of the land cells that are **left** (Lecture 12)
- **New on `Set`:** `toSet`, `s.contains(x)`, `s - x` (remove one), `s -- xs` (remove many), `headOption`
- Flood fill with a **work list** `todo`: take a cell, add its unvisited land neighbours, repeat

---

<style scoped>
section { font-size: 17px; }
</style>

# Number of Islands: Flood Fill with a `Set`

```scala
def numIslands(grid: Vector[String]): Int =
  val cells = for r <- 0 until grid.length; c <- 0 until grid(r).length yield (r, c)
  val land = cells.filter((r, c) => grid(r)(c) == '1').toSet

  def flood(todo: List[(Int, Int)], left: Set[(Int, Int)]): Set[(Int, Int)] =
    todo match
      case Nil => left
      case (r, c) :: rest =>
        val next = List((r+1, c), (r-1, c), (r, c+1), (r, c-1)).filter(left.contains)
        flood(next ++ rest, left -- next)

  def count(left: Set[(Int, Int)], n: Int): Int =
    left.headOption match
      case None    => n
      case Some(p) => count(flood(List(p), left - p), n + 1)
  count(land, 0)
```

`land`: all `(row, col)` with `'1'` · `flood` removes one island from `left` · `count` floods the island of any remaining cell and adds 1 · both tail recursive

---

<!-- _class: kapitel -->

## 6
# Trapping Rain Water

LeetCode 42 · Hard

---

<style scoped>
section { font-size: 22px; }
</style>

# Problem 6: Trapping Rain Water

<div class="columns" style="grid-template-columns: 1.4fr 1fr; align-items: start;">
<div>

Bars of width 1 with given heights stand side by side. After rain, water collects **between** higher bars. How many units of water stay?

**Input:** `h: Vector[Int]` · **Output:** `Int`

**Example:** `Vector(3, 0, 1, 0, 2, 4, 1, 2)` → `10`

</div>
<div>

```text
          #
# ~ ~ ~ ~ #
# ~ ~ ~ # # ~ #
# ~ # ~ # # # #
3 0 1 0 2 4 1 2
```

</div>
</div>

<p class="small">LeetCode 42: <a href="https://leetcode.com/problems/trapping-rain-water/">Trapping Rain Water</a> (Hard) – statement paraphrased, examples our own. Code tested with Scala 3.9.0.</p>

---

# What Do We Need to Do?

- Look at **one** position `i`. How high can water stand above it?
- It is limited by the **highest bar on the left** and the **highest bar on the right** – by the lower of the two
- Water at `i` = `min(leftMax, rightMax) - h(i)` (never negative if both include `h(i)`)
- Brute force: compute both maxima for every `i` → $O(n^2)$
- Better: all "max so far" values from the left in one `scanLeft` (Lecture 14), from the right the same on the reversed `Vector`
- Hard part: can we do it in $O(1)$ extra memory? → **two pointers**

---

<style scoped>
section { font-size: 16px; }
</style>

# Rain Water: Brute Force and Two Scans (1/2)

```scala
def trapBrute(h: Vector[Int]): Int =
  (0 until h.length).map { i =>
    val left  = h.take(i + 1).max
    val right = h.drop(i).max
    math.min(left, right) - h(i)
  }.sum
```

`take`/`drop` (Lecture 09) build the left and right part each time

---

<style scoped>
section { font-size: 16px; }
</style>

# Rain Water: Brute Force and Two Scans (2/2)

```scala
def trap(h: Vector[Int]): Int =
  val leftMax  = h.scanLeft(0)(math.max).tail
  val rightMax = h.reverse.scanLeft(0)(math.max).tail.reverse
  (0 until h.length).map(i => math.min(leftMax(i), rightMax(i)) - h(i)).sum
```

`scanLeft(0)(math.max)` = running maximum; `.tail` drops the start value

---

<style scoped>
section { font-size: 19px; }
</style>

# Rain Water: Two Pointers

```scala
def trapTwoPointers(h: Vector[Int]): Int =
  @tailrec
  def go(l: Int, r: Int, lMax: Int, rMax: Int, water: Int): Int =
    if l > r then water
    else if lMax <= rMax then
      val m = math.max(lMax, h(l)); go(l + 1, r, m, rMax, water + m - h(l))
    else
      val m = math.max(rMax, h(r)); go(l, r - 1, lMax, m, water + m - h(r))
  go(0, h.length - 1, 0, 0, 0)
```

- Idea: the side with the **smaller** max decides – its water level is already known, so we can move that pointer
- Only five numbers of state, $O(1)$ extra memory

---

<style scoped>
section { font-size: 19px; }
</style>

# Comparison: Java

```java
static int trap(int[] h) {
    int l = 0, r = h.length - 1, lMax = 0, rMax = 0, water = 0;
    while (l <= r) {
        if (lMax <= rMax) { lMax = Math.max(lMax, h[l]); water += lMax - h[l]; l++; }
        else              { rMax = Math.max(rMax, h[r]); water += rMax - h[r]; r--; }
    }
    return water;
}
```

- Java: one `while` loop with five mutable `int`s that change in every round
- Scala: the same five values as **parameters** of a tail-recursive function – each round gets fresh values

<p class="small">Both tested on (3, 0, 1, 0, 2, 4, 1, 2) → 10, (5, 2, 4) → 2, empty → 0.</p>

---

<style scoped>
section { font-size: 15px; }
</style>

# Testing in a Worksheet: `leetcode26.worksheet.sc`

<div class="columns" style="grid-template-columns: 1fr 1fr; align-items: start;">
<div>

```scala
val groups = Anagrams.groupAnagrams(List("tea", "eat", "tan", "ate", "nat"))
val top2   = TopK.topKFrequent(List(4, 1, 4, 7, 1, 4, 9, 1, 4), 2)
val window = LongestSub.lengthOfLongestSubstring("konstanz")
val coins  = Coins.coinChange(List(2, 5), 8)
val noWay  = Coins.coinChange(List(2), 3)
val grid   = Vector("11000", "11010", "00010", "01001")
val isl    = Islands.numIslands(grid)
val water  = Rain.trap(Vector(3, 0, 1, 0, 2, 4, 1, 2))
```

</div>
<div>

```scala
// groups: List[List[String]] = List(
//   List("tea", "eat", "ate"),
//   List("tan", "nat")
// )
// top2: List[Int] = List(4, 1)
// window: Int = 6
// coins: Option[Int] = Some(4)
// noWay: Option[Int] = None
// grid: Vector[String] = Vector("11000", "11010", "00010", "01001")
// isl: Int = 4
// water: Int = 10
```

</div>
</div>

- A **worksheet** (Lecture 04, slide 18 "Worksheets: the REPL in a File"): file name ends in `.worksheet.sc`, evaluated on every save
- Put the solution objects of this lecture in the same folder (or paste them above), then try your **own** examples
- Right: the real output of Scala 3.9.0 for these lines, written as comments – Metals shows it in grey at the end of each line

<p class="small">Results produced by running these lines with Scala 3.9.0 (scala-cli). </p>

---

<!-- _class: inhalt -->

<style scoped>
section { font-size: 20px; }
</style>

# Summary

- Group Anagrams: the right **key** + `groupMapReduce` / `groupBy`
- Top K: count, then **buckets** instead of sorting
- Longest Substring: a **sliding window** as the state of a `foldLeft`
- Coin Change: recursion first, then **dynamic programming** – store answers in a `Vector`
- Islands: flood fill with a `Set` as memory and a `List` as work list
- Rain Water: "max so far" with `scanLeft`, then **two pointers**
- Pattern: write the obvious solution, test it, and use it to check the fast one

---

<!-- _class: aufgabe -->

# Task

- Submit Coin Change and Number of Islands on leetcode.com in Scala (mind `-1` instead of `None` and `Array[Array[Char]]`)
- Coin Change II (LeetCode 518): count the **number of ways** instead of the minimum
- Islands: return the size of the **largest** island (LeetCode 695)
- Longest Substring: return the substring itself, not only its length
- Write a test that compares `trapBrute` and `trapTwoPointers` on 1000 random inputs

---

<!-- _class: abschluss -->

# Questions?

## Thank you!

marko.boger@htwg-konstanz.de
