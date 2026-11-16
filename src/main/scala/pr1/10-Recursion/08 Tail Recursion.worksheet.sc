// Lecture 10: Recursion – Chapter 4: Tail Recursion
import scala.annotation.tailrec

// Slide 22: Tail Calls and the Accumulator
def factTail(n: Int): BigInt =
  @tailrec
  def loop(i: Int, acc: BigInt): BigInt =
    if i == 0 then acc
    else loop(i - 1, acc * i)    // tail call
  loop(n, 1)

factTail(5)        // 120
factTail(100000).toString.length   // 456574 digits – no StackOverflowError

// Slide 23: Compiled to a Loop
// What you write:
@tailrec
def loop(i: Int, acc: BigInt): BigInt =
  if i == 0 then acc
  else loop(i - 1, acc * i)

// What the compiler makes of it (roughly) – renamed to loopCompiled here,
// because the worksheet cannot define loop twice:
def loopCompiled(i0: Int, acc0: BigInt): BigInt =
  var i = i0
  var acc = acc0
  while i != 0 do
    acc = acc * i
    i = i - 1
  acc

loop(5, 1)           // 120
loopCompiled(5, 1)   // 120

// Slide 24: Tail Recursion on Lists
// Not tail recursive: + happens after the call
def sum(xs: List[Int]): Int =
  xs match
    case Nil    => 0
    case h :: t => h + sum(t)

// Tail recursive
def sumTail(xs: List[Int]): Int =
  @tailrec
  def loop(rest: List[Int],
           acc: Int): Int =
    rest match
      case Nil    => acc
      case h :: t => loop(t, acc + h)
  loop(xs, 0)

sum(List(1, 2, 3, 4))       // 10
sumTail(List(1, 2, 3, 4))   // 10
sumTail((1 to 100000).toList)   // 705082704 – no stack overflow, but the Int overflows (exact: 5000050000)
// sum((1 to 100000).toList)    // java.lang.StackOverflowError – commented out on purpose

// Slide 25: Fibonacci: Exponential vs. Linear
// Naive – two calls, not tail recursive, ≈ 1.6^n calls
def fib(n: Int): Long =
  if n <= 1 then n
  else fib(n - 1) + fib(n - 2)

// Accumulators – tail recursive, n calls, one frame
def fibTail(n: Int): Long =
  @tailrec
  def loop(i: Int, a: Long, b: Long): Long =
    if i == 0 then a
    else loop(i - 1, b, a + b)
  loop(n, 0, 1)

fib(20)       // 6765
fibTail(20)   // 6765
fibTail(90)   // 2880067194370816120 – instantly
// fib(50)    // 12586269025 – but takes minutes; commented out on purpose
