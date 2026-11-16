// Lecture 10: Recursion – Slide 15: Merge Sort with Match and Recursion
// split the list in halves, sort both halves recursively, then merge them

def merge(xs: List[Int], ys: List[Int]): List[Int] = (xs, ys) match
  case (Nil, _) => ys
  case (_, Nil) => xs
  case (x :: xt, y :: yt) =>
    if x <= y then x :: merge(xt, ys)
    else y :: merge(xs, yt)

def mergeSort(xs: List[Int]): List[Int] = xs match
  case Nil | _ :: Nil => xs
  case _ =>
    val (left, right) = xs.splitAt(xs.length / 2)
    merge(mergeSort(left), mergeSort(right))

mergeSort(List(5, 2, 8, 1, 9, 3)) // List(1, 2, 3, 5, 8, 9)
