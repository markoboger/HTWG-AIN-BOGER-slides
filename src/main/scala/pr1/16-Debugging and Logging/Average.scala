// Programming I — Lecture 16: Debugging and Logging
// The buggy loop from the slides, and the corrected average used in the tests.

package pr1.debugging

/** The version from the "Our Buggy Program" slide: skips `xs(0)` and uses integer division. */
def averageBuggy(xs: List[Int]): Double =
  var sum = 0
  for i <- 1 until xs.length do
    sum += xs(i)
  sum / xs.length

/** Corrected version from the walkthrough slide. */
def average(xs: List[Int]): Double =
  require(xs.nonEmpty, "average of empty list")
  xs.sum.toDouble / xs.length

@main def run(): Unit =
  val grades = List(2, 3, 1, 4)
  println(s"Average: ${average(grades)}")   // expected 2.5
