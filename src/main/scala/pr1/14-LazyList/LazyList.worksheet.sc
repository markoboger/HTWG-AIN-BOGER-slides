// Lecture 14: Lazy Lists and Streams – all code from the slides, in deck order
// Open in VS Code with Metals (worksheet) or run with: scala-cli run LazyList.worksheet.sc
// Expected results are given as comments.

// ============================================================
// Chapter 1: Sequences and Series
// ============================================================

// --- Sequences (Folgen) ---
val a = LazyList.from(1).map(n => 2 * n)
val b = LazyList.from(1).map(n => 1.0 / n)

a.take(6).toList // List(2, 4, 6, 8, 10, 12)
b.take(4).toList // List(1.0, 0.5, 0.3333333333333333, 0.25)

// --- Recursively Defined Sequences ---
val c = LazyList.iterate(100.0)(x => x / 2 + 1)
c.take(6).toList // List(100.0, 51.0, 26.5, 14.25, 8.125, 5.0625)

// --- Series (Reihen) and Partial Sums ---
val geo = LazyList.from(0).map(k => math.pow(0.5, k)).scanLeft(0.0)(_ + _)
geo.take(6).toList // List(0.0, 1.0, 1.5, 1.75, 1.875, 1.9375)
geo(30) // 1.9999999981373549

val harm = LazyList.from(1).map(1.0 / _).scanLeft(0.0)(_ + _)
harm.indexWhere(_ > 5) // 83
harm.indexWhere(_ > 10) // 12367

// --- Approximating e and pi ---
val facts = LazyList
  .iterate((0, BigInt(1))) { case (n, f) => (n + 1, f * (n + 1)) }
  .map(_._2)
val e = facts.map(f => 1.0 / f.toDouble).scanLeft(0.0)(_ + _)
e.take(6)
  .toList // List(0.0, 1.0, 2.0, 2.5, 2.6666666666666665, 2.708333333333333)
e.zip(e.tail)
  .find((x, y) => (y - x).abs < 1e-12)
  .map(_._2) // Some(2.718281828458995)
math.E // 2.718281828459045

val pi = LazyList
  .from(0)
  .map(k => (if k % 2 == 0 then 4.0 else -4.0) / (2 * k + 1))
  .scanLeft(0.0)(_ + _)
pi(10) // 3.0418396189294032
pi(1000) // 3.140592653839794

// ============================================================
// Chapter 2: Strict and Lazy Evaluation
// ============================================================

// --- Call-by-Value vs. Call-by-Name ---
def compute(): Int =
  println("computing"); 21

def twiceV(x: Int): Int = x + x
def twiceN(x: => Int): Int = x + x

twiceV(compute()) // prints "computing" once,  result 42
twiceN(compute()) // prints "computing" twice, result 42

// --- lazy val ---
lazy val config =
  println("loading config")
  "ok"

println("before")
println(config) // prints "loading config", then "ok"
println(config) // prints only "ok" (cached)

// ============================================================
// Chapter 3: LazyList
// ============================================================

// --- LazyList in Scala ---
val ll = 1 #:: 2 #:: 3 #:: LazyList.empty
println(ll) // LazyList(<not computed>)

// --- Creating LazyLists ---
1 #:: 2 #:: 3 #:: LazyList.empty // like :: for List
LazyList.from(1).take(5).toList // List(1, 2, 3, 4, 5)
LazyList.iterate(1)(_ * 2).take(8).toList // List(1, 2, 4, 8, 16, 32, 64, 128)
LazyList.continually("ha").take(3).mkString // hahaha

def countdown(n: Int): LazyList[Int] =
  if n < 0 then LazyList.empty
  else LazyList.cons(n, countdown(n - 1))

countdown(3).toList // List(3, 2, 1, 0)

// --- Memoization ---
val squares = LazyList.from(1).map { n =>
  println(s"eval $n"); n * n
}
println(squares) // LazyList(<not computed>)
println(squares.take(3).toList) // eval 1, eval 2, eval 3, then List(1, 4, 9)
println(squares) // LazyList(1, 4, 9, <not computed>)
println(squares.take(4).toList) // eval 4, then List(1, 4, 9, 16)

// ============================================================
// Chapter 4: Infinite Data Structures
// ============================================================

// --- Fibonacci Numbers with zip ---
val fibs: LazyList[BigInt] =
  BigInt(0) #:: BigInt(1) #:: fibs.zip(fibs.tail).map((a, b) => a + b)

fibs.take(12).toList // List(0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89)
fibs(100) // 354224848179261915075

// --- Prime Numbers: Sieve of Eratosthenes ---
def sieve(s: LazyList[Int]): LazyList[Int] =
  s.head #:: sieve(s.tail.filter(_ % s.head != 0))

val primes = sieve(LazyList.from(2))

primes.take(10).toList // List(2, 3, 5, 7, 11, 13, 17, 19, 23, 29)

// ============================================================
// Chapter 5: Operations
// ============================================================

// --- Lazy Operations ---
val m = LazyList.from(1).map(_ * 10)
println(m) // LazyList(<not computed>)
println(m.take(3)) // LazyList(<not computed>)
println(m.take(3).toList) // List(10, 20, 30)

// --- Forcing Operations ---
val nats = LazyList.from(0)
nats.head // 0
nats.tail.head // 1
nats.find(n => n * n > 1000) // Some(32)

// --- Pitfall 1: Forcing an Infinite List (commented out – would hang or crash) ---
// LazyList.from(1).length                // never terminates
// LazyList.from(1).toList                // OutOfMemoryError
// LazyList.from(1).foldLeft(0)(_ + _)    // never terminates
// LazyList.from(1).filter(_ < 0).head    // searches forever
LazyList.from(1).take(100).sum // 5050 – limit first, then force

// --- Pitfall 2: Holding the Head (commented out – slow and memory-hungry) ---
// val natsFrom1 = LazyList.from(1)          // natsFrom1 references the head
// natsFrom1.drop(100_000_000).head          // all 100 million cells are kept!
// LazyList.from(1).drop(100_000_000).head   // no reference: cells can be garbage collected

// --- Views ---
val v = (1 to 1_000_000).view
  .map(_ * 2)
  .filter(_ % 3 == 0)

v.take(3).toList // List(6, 12, 18)

// --- Iterators ---
val it = Iterator.from(1).map(_ * 2)
it.take(3).toList // List(2, 4, 6)

val it2 = Iterator(1, 2, 3)
println(it2.sum) // 6
println(it2.sum) // 0 – already consumed!

// ============================================================
// Chapter 6: Java Streams (the Java code of the slides, called from Scala)
// ============================================================
import java.util.stream.{Collectors, IntStream, Stream}

// --- Java Streams: Infinite Sources ---
val evens = Stream
  .iterate[Integer](1, n => n + 1)
  .filter(n => n % 2 == 0)
  .map[Integer](n => n * n)
  .limit(5)
  .collect(Collectors.toList())
println(evens) // [4, 16, 36, 64, 100]
println(
  Stream.generate[String](() => "ha").limit(3).collect(Collectors.joining())
) // hahaha
println(IntStream.rangeClosed(1, 100).sum()) // 5050

// Scala equivalent:
LazyList
  .from(1)
  .filter(_ % 2 == 0)
  .map(n => n * n)
  .take(5)
  .toList // List(4, 16, 36, 64, 100)

// --- Java Streams: Lazy and Single-Use ---
Stream
  .of("a", "b", "c")
  .peek(s => println("peek " + s))
  .map[String](_.toUpperCase) // no terminal op: prints nothing

Stream
  .of("a", "b", "c")
  .peek(s => println("peek " + s))
  .map[String](_.toUpperCase)
  .findFirst()
  .ifPresent(x => println(x)) // prints "peek a", then "A"

val js = Stream.of(1, 2, 3)
println(js.count()) // 3
try js.count()
catch
  case ex: IllegalStateException =>
    println(ex.getMessage) // stream has already been operated upon or closed

// ============================================================
// Chapter 7: Practice – stop rule |x(n+1) - x(n)| < eps
// ============================================================

// --- Heron's Method: A Converging Sequence ---
def heron(a: Double): LazyList[Double] =
  LazyList.iterate(a)(x => (x + a / x) / 2)

def converged(xs: LazyList[Double], eps: Double): (Int, Double) =
  val i = xs.zip(xs.tail).indexWhere((x, y) => (y - x).abs < eps)
  (i + 1, xs(i + 1))

heron(2).take(6).toList
// List(2.0, 1.5, 1.4166666666666665, 1.4142156862745097, 1.4142135623746899, 1.414213562373095)
converged(heron(2), 1e-12) // (6,1.414213562373095)
math.sqrt(2) // 1.4142135623730951
converged(heron(1_000_000), 1e-9) // (15,1000.0)

// --- Two Series for pi: Who Converges Faster? ---
def leibniz: LazyList[Double] =
  LazyList
    .from(0)
    .map(k => (if k % 2 == 0 then 4.0 else -4.0) / (2 * k + 1))
    .scanLeft(0.0)(_ + _)

def nilakantha: LazyList[Double] =
  LazyList
    .from(1)
    .map { k =>
      val n = 2.0 * k
      (if k % 2 == 1 then 4.0 else -4.0) / (n * (n + 1) * (n + 2))
    }
    .scanLeft(3.0)(_ + _)

def termsUntil(xs: LazyList[Double], eps: Double): Int =
  xs.indexWhere(s => (s - math.Pi).abs < eps)

termsUntil(leibniz, 1e-3) // 1000
termsUntil(nilakantha, 1e-3) // 6
termsUntil(
  leibniz,
  1e-6
) // 1000001 – about a million partial sums, takes a moment
termsUntil(nilakantha, 1e-6) // 62

// --- The Golden Ratio from Fibonacci Numbers (fibs from chapter 4) ---
val ratios =
  fibs.tail.zip(fibs.tail.tail).map((a, b) => b.toDouble / a.toDouble)

ratios.take(8).toList
// List(1.0, 2.0, 1.5, 1.6666666666666667, 1.6, 1.625, 1.6153846153846154, 1.619047619047619)
converged(ratios, 1e-12) // (30,1.6180339887496482)
(1 + math.sqrt(5)) / 2 // 1.618033988749895
