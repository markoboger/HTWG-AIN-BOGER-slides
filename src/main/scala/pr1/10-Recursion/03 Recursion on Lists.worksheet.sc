// Lecture 10: Recursion – Chapter 2: lists are recursive

// Slide 12: Lists Are Recursive – List[A] = Nil | A :: List[A]
List(1, 2, 3) == 1 :: (2 :: (3 :: Nil))   // true

// Slide 13: Structural Recursion on Lists
def sum(xs: List[Int]): Int = xs match
  case Nil    => 0
  case h :: t => h + sum(t)

def length[A](xs: List[A]): Int = xs match
  case Nil    => 0
  case _ :: t => 1 + length(t)

def contains[A](xs: List[A], x: A): Boolean =
  xs match
    case Nil    => false
    case h :: t => h == x || contains(t, x)

sum(List(1, 2, 3, 4))           // 10
length(List("a", "b", "c"))     // 3
contains(List(1, 2, 3), 2)      // true
contains(List(1, 2, 3), 5)      // false
