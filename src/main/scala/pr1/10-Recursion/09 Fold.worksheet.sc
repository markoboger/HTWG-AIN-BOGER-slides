// Lecture 10: Recursion – Chapter 4: Fold: Accumulator as a Library Method
// Slide 27: xs.foldLeft(z)(f) – z is the start value of the accumulator,
// f combines accumulator and element

// Slide 28: Fold Examples
def sum(xs: List[Int]) =
  xs.foldLeft(0)(_ + _)

def product(xs: List[Int]) =
  xs.foldLeft(1)(_ * _)

def length(xs: List[Int]) =
  xs.foldLeft(0)((n, _) => n + 1)

def reverse[A](xs: List[A]) =
  xs.foldLeft(List.empty[A])((acc, x) => x :: acc)

sum(List(1, 2, 3, 4))      // 10
product(List(2, 3, 4))     // 24
length(List(1, 2, 3))      // 3
reverse(List(1, 2, 3))     // List(3, 2, 1)
