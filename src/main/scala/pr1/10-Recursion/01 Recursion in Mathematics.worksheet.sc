// Lecture 10: Recursion – Chapter 1: Recursion in Mathematics
// Recurrence equation -> Scala: base case + recursive step

// Slide 6: Factorial
def factorial(n: Int): BigInt =
  if n == 0 then 1
  else n * factorial(n - 1)

factorial(5)   // 120
factorial(21)  // 51090942171709440000 (no longer fits into a Long)

// Slide 7: Fibonacci
def fib(n: Int): Long =
  if n <= 1 then n
  else fib(n - 1) + fib(n - 2)

fib(10)   // 55

// Slide 8: Greatest Common Divisor: Euclid
def gcd(a: Int, b: Int): Int =
  if b == 0 then a
  else gcd(b, a % b)

gcd(48, 18)   // 6
// gcd(18,12) → gcd(12,6) → gcd(6,0) → 6
