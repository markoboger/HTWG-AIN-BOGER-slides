// Lecture 10: Recursion – Slide 29: Loop, Recursion, Fold
// The same sum three times

// Loop: mutable accumulator
def sumLoop(xs: List[Int]) =
  var acc = 0
  for x <- xs do acc += x
  acc

// Recursion: structural, follows the list
def sum(xs: List[Int]): Int =
  xs match
    case Nil    => 0
    case h :: t => h + sum(t)

// Fold: the accumulator as a library method
def sumFold(xs: List[Int]) =
  xs.foldLeft(0)(_ + _)

sumLoop(List(1, 2, 3, 4))   // 10
sum(List(1, 2, 3, 4))       // 10
sumFold(List(1, 2, 3, 4))   // 10
