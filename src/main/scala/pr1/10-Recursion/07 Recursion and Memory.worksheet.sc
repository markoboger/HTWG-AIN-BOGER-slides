// Lecture 10: Recursion – Chapter 3: Recursion and Memory

// Slide 18: Tracing factorial(3) – one stack frame per call,
// the multiplication happens after the recursive call returns: 1 → 1 → 2 → 6
def factorial(n: Int): BigInt =
  if n == 0 then 1
  else n * factorial(n - 1)

factorial(3)   // 6

// Slide 19: Stack and Heap – frames hold references to the list cells
def sum(xs: List[Int]): Int = xs match
  case Nil    => 0
  case h :: t => h + sum(t)

sum(List(1, 2, 3))   // 6

// Slide 20: Termination and StackOverflow
// No base case -> infinite recursion. Commented out on purpose.
// Note: the slide says java.lang.StackOverflowError, but the recursive call is the
// last action (a tail call), so the Scala compiler turns it into a loop: countDown
// never overflows, it prints 0, -1, -2, ... forever (tested with Scala 3.9.0).
// def countDown(n: Int): Unit =
//   println(n)
//   countDown(n - 1)        // no base case!

// Even correct recursion can overflow the stack (commented out on purpose):
// factorial(100000)   // java.lang.StackOverflowError
