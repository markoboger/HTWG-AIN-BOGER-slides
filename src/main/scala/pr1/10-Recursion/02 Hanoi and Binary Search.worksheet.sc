// Lecture 10: Recursion – Chapter 2: Beautiful Computer Science

// Slide 10: Towers of Hanoi – moves(n) = 2^n - 1
def hanoi(n: Int, from: Char, to: Char,
          via: Char): Unit =
  if n > 0 then
    hanoi(n - 1, from, via, to)
    println(s"disc $n: $from -> $to")
    hanoi(n - 1, via, to, from)

hanoi(3, 'A', 'C', 'B')
// disc 1: A -> C
// disc 2: A -> B
// disc 1: C -> B
// disc 3: A -> C
// disc 1: B -> A
// disc 2: B -> C
// disc 1: A -> C      (7 = 2^3 - 1 moves)

// Slide 11: Binary Search – the array must be sorted
def search(a: Array[Int], x: Int,
           lo: Int, hi: Int): Int =
  if lo > hi then -1
  else
    val mid = (lo + hi) / 2
    if a(mid) == x then mid
    else if a(mid) > x then search(a, x, lo, mid - 1)
    else search(a, x, mid + 1, hi)

val sorted = Array(1, 3, 5, 7, 9, 11, 13)
search(sorted, 9, 0, sorted.length - 1)   // 4
search(sorted, 4, 0, sorted.length - 1)   // -1
