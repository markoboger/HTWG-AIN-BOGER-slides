// Programming I — Lecture 15: Option and Try
// Try examples from the slides: parse, recover, readLines, chaining fallible steps.

package pr1.optiontry

import scala.io.Source
import scala.util.{Failure, Success, Try, Using}

def parse(s: String): Try[Int] = Try(s.trim.toInt)

def divTry(a: Int, b: Int): Try[Int] = Try(a / b)

def report(t: Try[Int]): String = t match
  case Success(n)  => s"got $n"
  case Failure(ex) => s"failed: ${ex.getMessage}"

def readLines(path: String): Try[List[String]] =
  Try(Using.resource(Source.fromFile(path, "UTF-8"))(_.getLines().toList))

def averageFromFile(path: String): Try[Double] =
  for
    lines <- readLines(path)
    nums  <- Try(lines.map(_.trim.toInt))
    avg   <- Try(
               if nums.isEmpty then throw IllegalArgumentException("no numbers")
               else nums.sum.toDouble / nums.size)
  yield avg
