// Lecture 10: Recursion – Slide 16: LeetCode 21: Merge Two Sorted Lists
// base cases: one list is empty -> take the other
// recursive step: the smaller head goes first, merge the rest
// (LeetCode uses its own ListNode class; same idea)

def merge(a: List[Int], b: List[Int]): List[Int] =
  (a, b) match
    case (Nil, _) => b
    case (_, Nil) => a
    case (x :: xs, y :: ys) =>
      if x <= y then x :: merge(xs, b)
      else y :: merge(a, ys)

merge(List(1, 2, 4), List(1, 3, 4))   // List(1, 1, 2, 3, 4, 4)
