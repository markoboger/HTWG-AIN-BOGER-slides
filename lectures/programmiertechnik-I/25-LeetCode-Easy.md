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
# Lecture 25: LeetCode I: Easy Problems

<p class="small">Six classic problems, from easy to less easy – with the tools of Lectures 01–24</p>

---

<!-- _class: inhalt -->

<style scoped>
section { font-size: 20px; }
</style>

# Goals

In this lecture you will

- solve **six LeetCode problems** of rising difficulty – all rated *Easy*
- practise a fixed routine: **read** the problem, **think** first, then **code**
- write each solution in **two or three styles**: loop with `var`, recursion, `foldLeft`, collection methods
- use what you know: pattern matching (09), `Option` (15), `Map` (12/15), `@tailrec` (10), `enum` (08), `scanLeft` (14)
- see **Python** and **Java** next to Scala where it teaches something

Lecture 26 continues with *Medium* and one *Hard* problem.

---

<style scoped>
section { font-size: 22px; }
</style>

# Our Routine for Every Problem

1. **The problem** – what goes in, what comes out, an example
2. **What do we need to do?** – questions to discuss *before* coding
3. **Solution(s)** in Scala – first the obvious one, then a more elegant or faster one
4. Sometimes: the same in **Python** or **Java**

| # | Problem | LeetCode | Main idea |
|---|---|---|---|
| 1 | Fizz Buzz | 412 | `match` on a tuple |
| 2 | Two Sum | 1 | `Map` as memory |
| 3 | Valid Palindrome | 125 | strings, two indices |
| 4 | Valid Parentheses | 20 | `List` as a stack |
| 5 | Maximum Depth of Binary Tree | 104 | `enum` + recursion |
| 6 | Best Time to Buy and Sell Stock | 121 | `foldLeft` with a state |

<p class="small">Remember Lecture 03: LeetCode 55 Jump Game; Lecture 10: LeetCode 21, 22 and 779.</p>

---

<!-- _class: kapitel -->

## 1
# Fizz Buzz

LeetCode 412 · Easy

---

# Problem 1: Fizz Buzz

Given a number `n`, produce a list of strings for the numbers `1` to `n`:

- a multiple of **3 and 5** becomes `"FizzBuzz"`
- a multiple of **3** becomes `"Fizz"`, a multiple of **5** becomes `"Buzz"`
- every other number becomes its own digits, e.g. `"7"`

**Input:** `n: Int` · **Output:** `List[String]`

**Example:** `n = 10` → `1, 2, Fizz, 4, Buzz, Fizz, 7, 8, Fizz, Buzz`

<p class="small">LeetCode 412: <a href="https://leetcode.com/problems/fizz-buzz/">Fizz Buzz</a> (Easy) – statement paraphrased, examples our own. Code tested with Scala 3.9.0.</p>

---

# What Do We Need to Do?

- How do we test "multiple of 3"? → `i % 3 == 0` (Lecture 05)
- Does the **order** of the tests matter? What happens for `15` if we test `% 3` first?
- One result per number: is this a **loop**, a `for … yield` or a `map`?
- Can we look at `i % 3` and `i % 5` **at the same time**?

---

<style scoped>
section { font-size: 20px; }
</style>

# Fizz Buzz: Two Solutions

<div class="columns" style="grid-template-columns: 1fr 1fr; align-items: start;">
<div>

```scala
def fizzBuzzImp(n: Int): List[String] =
  for i <- (1 to n).toList yield
    if i % 15 == 0 then "FizzBuzz"
    else if i % 3 == 0 then "Fizz"
    else if i % 5 == 0 then "Buzz"
    else i.toString
```

`if`-chain: the order is the logic

</div>
<div>

```scala
def fizzBuzz(n: Int): List[String] =
  (1 to n).toList.map { i =>
    (i % 3, i % 5) match
      case (0, 0) => "FizzBuzz"
      case (0, _) => "Fizz"
      case (_, 0) => "Buzz"
      case _      => i.toString
  }
```

`match` on the tuple `(i % 3, i % 5)` – the four cases are visible at once (Lecture 09)

</div>
</div>

---

<!-- _class: kapitel -->

## 2
# Two Sum

LeetCode 1 · Easy

---

# Problem 2: Two Sum

Given a sequence of numbers and a **target**, find the positions of **two different** elements that add up to the target.

**Input:** `nums: Vector[Int]`, `target: Int`
**Output:** a pair of indices `(i, j)` with `i < j`

**Example:** `nums = Vector(4, 9, 6, 1)`, `target = 7` → `(2, 3)`, because `6 + 1 = 7`

LeetCode promises exactly one solution. We are more careful: if there is none, we return `None` – so the result type is `Option[(Int, Int)]` (Lecture 15).

<p class="small">LeetCode 1: <a href="https://leetcode.com/problems/two-sum/">Two Sum</a> (Easy) – statement paraphrased, examples our own. Code tested with Scala 3.9.0.</p>

---

# What Do We Need to Do?

- The obvious way: try **every pair**. How many pairs are there for `n` elements?
- Can we do it in **one pass**? Walking through, which number do we *hope* to have seen before?
- What do we need to **remember** about earlier numbers – the value, the index, both?
- Which collection answers "have I seen `x`, and where?" quickly?
- Why must the two elements be **different** positions? Test: `Vector(5, 5)`, target `10`

---

<style scoped>
section { font-size: 17px; }
</style>

# Two Sum: Brute Force vs. `Map`

<div class="columns" style="grid-template-columns: 1fr 1fr; align-items: start;">
<div>

```scala
def twoSumBrute(nums: Vector[Int], target: Int): Option[(Int, Int)] =
  val pairs =
    for
      i <- 0 until nums.length
      j <- (i + 1) until nums.length
      if nums(i) + nums(j) == target
    yield (i, j)
  pairs.headOption
```

Nested `for` with a guard (Lecture 07): $n^2/2$ pairs

</div>
<div>

```scala
def twoSum(nums: Vector[Int], target: Int): Option[(Int, Int)] =
  @tailrec
  def go(i: Int, seen: Map[Int, Int]): Option[(Int, Int)] =
    if i == nums.length then None
    else seen.get(target - nums(i)) match
      case Some(j) => Some((j, i))
      case None    => go(i + 1, seen + (nums(i) -> i))
  go(0, Map.empty)
```

One pass: `seen` maps value → index; `get` returns an `Option`

</div>
</div>

---

<style scoped>
section { font-size: 20px; }
</style>

# Comparison: Python

<div class="columns" style="grid-template-columns: 1.2fr 1fr; align-items: start;">
<div>

```python
def two_sum(nums, target):
    seen = {}                      # dict = mutable Map
    for i, n in enumerate(nums):   # enumerate = zipWithIndex
        if target - n in seen:
            return (seen[target - n], i)
        seen[n] = i
    return None                    # None = Scala's None
```

</div>
<div>

- Same idea, but `seen` is **mutable**: a Python `dict` is a mutable `Map`
- `enumerate(nums)` gives pairs `(index, value)` – like `zipWithIndex` (Lecture 03), just the other way round
- `x in seen` ↔ `seen.contains(x)`
- Python's `None` is a plain `null`-like value – no `Some` around the result

</div>
</div>

<p class="small">Tested with Python 3: (4, 9, 6, 1) / 7 → (2, 3); (5, 5) / 10 → (0, 1); (1, 2) / 9 → None.</p>

---

<!-- _class: kapitel -->

## 3
# Valid Palindrome

LeetCode 125 · Easy

---

# Problem 3: Valid Palindrome

A text is a **palindrome** if it reads the same forwards and backwards – after we

- **ignore** everything that is not a letter or a digit (spaces, commas, `?`)
- **ignore** upper and lower case

**Input:** `s: String` · **Output:** `Boolean`

**Examples:**
- `"Was it a car or a cat I saw?"` → `true` (`wasitacaroracatisaw`)
- `"Scala rocks"` → `false`
- `" , "` → `true` – nothing is left, and the empty string is a palindrome

<p class="small">LeetCode 125: <a href="https://leetcode.com/problems/valid-palindrome/">Valid Palindrome</a> (Easy) – statement paraphrased, examples our own. Code tested with Scala 3.9.0.</p>

---

# What Do We Need to Do?

- Step 1 **clean**, step 2 **compare**: which methods do we know for each step?
- New on `Char`: `c.isLetterOrDigit` (true for `a`–`z`, `A`–`Z`, `0`–`9`) and `c.toLower`
- Cleaning builds a **new string**. Can we compare *without* copying?
- Idea: one index from the **left**, one from the **right**, walking towards each other
- When do we stop? What do we do when one side points at a comma?

---

<style scoped>
section { font-size: 18px; }
</style>

# Valid Palindrome: Copy vs. Two Indices

<div class="columns" style="grid-template-columns: 1fr 1.3fr; align-items: start;">
<div>

```scala
def isPalindromeSimple(s: String): Boolean =
  val clean = s.filter(_.isLetterOrDigit).toLowerCase
  clean == clean.reverse
```

`filter` and `reverse` (Lectures 06 and 09) – short and clear, but two copies of the string

</div>
<div>

```scala
def isPalindrome(s: String): Boolean =
  @tailrec
  def check(i: Int, j: Int): Boolean =
    if i >= j then true
    else if !s(i).isLetterOrDigit then check(i + 1, j)
    else if !s(j).isLetterOrDigit then check(i, j - 1)
    else if s(i).toLower != s(j).toLower then false
    else check(i + 1, j - 1)
  check(0, s.length - 1)
```

Two indices, tail recursive (Lecture 10): no copy, each character is read once

</div>
</div>

---

<!-- _class: kapitel -->

## 4
# Valid Parentheses

LeetCode 20 · Easy

---

# Problem 4: Valid Parentheses

A string consists only of the brackets `( ) [ ] { }`. It is **valid** if

- every opening bracket is closed by a bracket of the **same kind**
- brackets are closed in the **right order** – the last one opened is closed first

**Input:** `s: String` · **Output:** `Boolean`

**Examples:**
- `"{[()()]}"` → `true`
- `"([)]"` → `false` – `[` is closed by `)`
- `"(("` → `false` – never closed; `")"` → `false` – nothing to close

<p class="small">LeetCode 20: <a href="https://leetcode.com/problems/valid-parentheses/">Valid Parentheses</a> (Easy) – statement paraphrased, examples our own. Code tested with Scala 3.9.0.</p>

---

# What Do We Need to Do?

- Is it enough to **count** brackets? Try `"([)]"`
- "The last one opened is closed first": which data structure works like this? (Lecture 06: **stack**)
- A Scala `List` is a perfect stack: `c :: stack` pushes, `top :: rest` pops
- Which **cases** are there for the next character and the stack? Write them as a `match`
- What must be true at the **end**?

---

<style scoped>
section { font-size: 18px; }
</style>

# Valid Parentheses: Recursion with a `List` Stack

<div class="columns" style="grid-template-columns: 1.6fr 1fr; align-items: start;">
<div>

```scala
val pairs = Map(')' -> '(', ']' -> '[', '}' -> '{')

def isValid(s: String): Boolean =
  @tailrec
  def go(rest: List[Char], stack: List[Char]): Boolean =
    (rest, stack) match
      case (Nil, _) => stack.isEmpty
      case (c :: cs, _) if !pairs.contains(c) => go(cs, c :: stack)
      case (c :: cs, top :: ts) if pairs(c) == top => go(cs, ts)
      case _ => false
  go(s.toList, Nil)
```

</div>
<div>

- `pairs` maps a **closing** bracket to its opening partner
- Case 2: an opening bracket → **push**
- Case 3: closing bracket matches the top → **pop**
- Every other case: wrong kind, or empty stack → `false`
- Guards `if …` in `case` (Lecture 15)

</div>
</div>

---

<style scoped>
section { font-size: 18px; }
</style>

# Variant: `foldLeft` with `Option` as "Still OK?"

<div class="columns" style="grid-template-columns: 1.6fr 1fr; align-items: start;">
<div>

```scala
def isValidFold(s: String): Boolean =
  val end = s.foldLeft(Option(List.empty[Char])) {
    case (None, _) => None
    case (Some(stack), c) if !pairs.contains(c) => Some(c :: stack)
    case (Some(top :: ts), c) if pairs(c) == top => Some(ts)
    case _ => None
  }
  end == Some(Nil)
```

</div>
<div>

- The state is `Option[List[Char]]`: `Some(stack)` while all is well, `None` after the first error
- Once `None`, it stays `None` (case 1)
- Valid if we end with `Some(Nil)` – an empty stack
- Downside: no early exit, `foldLeft` always reads the whole string

</div>
</div>

---

<style scoped>
section { font-size: 18px; }
</style>

# Comparison: Java

<div class="columns" style="grid-template-columns: 1.5fr 1fr; align-items: start;">
<div>

```java
static boolean isValid(String s) {
    Map<Character, Character> pairs = Map.of(')', '(', ']', '[', '}', '{');
    Deque<Character> stack = new ArrayDeque<>();
    for (char c : s.toCharArray()) {
        if (!pairs.containsKey(c)) stack.push(c);
        else if (stack.isEmpty() || !stack.pop().equals(pairs.get(c))) return false;
    }
    return stack.isEmpty();
}
```

</div>
<div>

- `Deque` / `ArrayDeque`: Java's **mutable** stack: `push` adds on top, `pop` removes and returns the top
- `toCharArray()` turns the `String` into a `char[]` for the loop
- **Pitfall:** `Character` is an object – compare with `equals`, not `!=` (that compares references!)
- In Scala, `==` always compares values

</div>
</div>

<p class="small">Tested with javac/java (JDK 21) on the same five examples as the Scala code.</p>

---

<!-- _class: kapitel -->

## 5
# Maximum Depth of a Binary Tree

LeetCode 104 · Easy

---

<style scoped>
section { font-size: 22px; }
</style>

# Problem 5: Maximum Depth of Binary Tree

<div class="columns" style="grid-template-columns: 1.4fr 1fr; align-items: start;">
<div>

The **depth** of a binary tree is the number of nodes on the **longest path** from the root down to a leaf.

**Input:** a binary tree · **Output:** `Int`

**Example:** the tree on the right has depth **4** (path `5 → 8 → 9 → 10`); the empty tree has depth **0**.

LeetCode gives a class `TreeNode` with `null` children. We model the tree as an `enum` (Lecture 08) – no `null` (Lecture 15).

</div>
<div>

```text
        5
      /   \
     2     8
          / \
         6   9
              \
               10
```

</div>
</div>

<p class="small">LeetCode 104: <a href="https://leetcode.com/problems/maximum-depth-of-binary-tree/">Maximum Depth of Binary Tree</a> (Easy) – statement paraphrased, examples our own. Code tested with Scala 3.9.0.</p>

---

<style scoped>
section { font-size: 22px; }
</style>

# What Do We Need to Do?

<div class="columns" style="grid-template-columns: 1fr 1fr; align-items: start;">
<div>

```scala
enum Tree:
  case Leaf
  case Node(left: Tree, value: Int, right: Tree)
```

</div>
<div>

- The type is **recursive**: a `Node` contains two `Tree`s
- What is the depth of a `Leaf`?
- If we know the depth of both children, what is the depth of the node?
- Alternative: count the **levels** – start with the root, then all children, then their children …

</div>
</div>

---

<style scoped>
section { font-size: 18px; }
</style>

# Maximum Depth: Recursive vs. Level by Level

<div class="columns" style="grid-template-columns: 1fr 1.25fr; align-items: start;">
<div>

```scala
import Tree.*

def maxDepth(t: Tree): Int = t match
  case Leaf => 0
  case Node(l, _, r) => 1 + math.max(maxDepth(l), maxDepth(r))
```

The structure of the code follows the structure of the type – **structural recursion** (Lecture 10)

</div>
<div>

```scala
def maxDepthBfs(t: Tree): Int =
  @tailrec
  def go(level: List[Tree], depth: Int): Int =
    val nodes = level.collect { case n: Node => n }
    if nodes.isEmpty then depth
    else go(nodes.flatMap(n => List(n.left, n.right)), depth + 1)
  go(List(t), 0)
```

`collect` keeps the `Node`s only; each round is one level. Tail recursive – no deep call stack

</div>
</div>

---

<!-- _class: kapitel -->

## 6
# Best Time to Buy and Sell Stock

LeetCode 121 · Easy

---

# Problem 6: Best Time to Buy and Sell Stock

You get the price of a share for each day. You may **buy once** and **sell once later**. What is the **highest profit**? If you cannot win, the answer is `0`.

**Input:** `prices: Vector[Int]` · **Output:** `Int`

**Examples:**
- `Vector(8, 3, 6, 2, 7, 4)` → `5`: buy at `2` (day 4), sell at `7` (day 5)
- `Vector(9, 7, 4)` → `0`: prices only fall

Note: buying at the overall minimum is **not** always right – here the minimum `2` happens to work, but try `Vector(3, 9, 1, 2)`.

<p class="small">LeetCode 121: <a href="https://leetcode.com/problems/best-time-to-buy-and-sell-stock/">Best Time to Buy and Sell Stock</a> (Easy) – statement paraphrased, examples our own. Code tested with Scala 3.9.0.</p>

---

# What Do We Need to Do?

- Brute force: every pair (buy day, later sell day) – like Two Sum, $O(n^2)$
- Walk from left to right. If we **sell today**, which buy day is best?
- So, what do we need to **remember** while walking? Two numbers – which ones?
- Two numbers carried along a sequence: a loop with two `var`s, or a `foldLeft` with a **pair** as state
- Or: first compute the "lowest price so far" for each day with `scanLeft` (Lecture 14)

---

<style scoped>
section { font-size: 16px; }
</style>

# Stock: Loop, `foldLeft`, `scanLeft`

<div class="columns" style="grid-template-columns: 1fr 1fr; align-items: start;">
<div>

```scala
def maxProfitImp(prices: Vector[Int]): Int =
  var minPrice = Int.MaxValue
  var best = 0
  for p <- prices do
    minPrice = math.min(minPrice, p)
    best = math.max(best, p - minPrice)
  best
```

```scala
def maxProfitScan(prices: Vector[Int]): Int =
  val minSoFar = prices.scanLeft(Int.MaxValue)(math.min).tail
  prices.zip(minSoFar).map((p, m) => p - m).maxOption.getOrElse(0)
```

</div>
<div>

```scala
def maxProfit(prices: Vector[Int]): Int =
  prices.foldLeft((Int.MaxValue, 0)) { case ((minP, best), p) =>
    (math.min(minP, p), math.max(best, p - minP))
  }._2
```

- The `var`s of the loop become the **pair** `(minP, best)` of the fold (Lecture 10: loop, recursion, fold)
- `scanLeft` keeps **all** intermediate minimums; `zip` pairs each price with it
- `maxOption` (Lecture 20) handles the empty `Vector`

</div>
</div>

---

<style scoped>
section { font-size: 15px; }
</style>

# Testing in a Worksheet: `leetcode25.worksheet.sc`

<div class="columns" style="grid-template-columns: 1fr 1fr; align-items: start;">
<div>

```scala
import Tree.*

val fizz = FizzBuzz.fizzBuzz(15).takeRight(5)
val pair = TwoSum.twoSum(Vector(4, 9, 6, 1), 7)
val none = TwoSum.twoSum(Vector(1, 2), 9)
val pal  = Palindrome.isPalindrome("Was it a car or a cat I saw?")
val ok   = Parens.isValid("{[()()]}")
val bad  = Parens.isValid("([)]")
val dep  = Depth.maxDepth(Node(Leaf, 1, Node(Node(Leaf, 3, Leaf), 2, Leaf)))
val gain = Stock.maxProfit(Vector(8, 3, 6, 2, 7, 4))
```

</div>
<div>

```scala
// fizz: List[String] = List("11", "Fizz", "13", "14", "FizzBuzz")
// pair: Option[(Int, Int)] = Some((2, 3))
// none: Option[(Int, Int)] = None
// pal: Boolean = true
// ok: Boolean = true
// bad: Boolean = false
// dep: Int = 3
// gain: Int = 5
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

- A routine: **read** the problem, **discuss** ideas, then code – and test with your own examples
- Fizz Buzz: `match` on a tuple shows all cases at once
- Two Sum: a `Map` as memory turns $O(n^2)$ into $O(n)$
- Palindrome: two indices instead of a copy
- Parentheses: a `List` is a stack; `Option` as "still OK?" in a `foldLeft`
- Tree depth: an `enum` instead of `null`, structural recursion
- Stock: two `var`s become the state of a `foldLeft`; `scanLeft` for "so far" values

---

<!-- _class: aufgabe -->

# Task

- Submit two of today's solutions on leetcode.com (choose Scala as language). Mind LeetCode's signatures: `Array[Int]`, `TreeNode`, no `Option`
- Two Sum: what changes if the input is **sorted**? (LeetCode 167, Two Sum II)
- Palindrome: write a version with `foldLeft` – is it still efficient?
- Tree: write `minDepth` (LeetCode 111) – careful with nodes that have only one child
- Stock: allow **many** buy/sell rounds (LeetCode 122)

---

<!-- _class: abschluss -->

# Questions?

## Thank you!

marko.boger@htwg-konstanz.de
