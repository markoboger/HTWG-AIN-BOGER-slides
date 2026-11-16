// Slides 15–17: import selectors, renaming and hiding, imports anywhere
package imports

import bank.Account                      // one member
import bank.{Account, fee}               // several members
import bank.*                            // everything (Java: .*)
import scala.math.max                    // a method from an object

import bank.{fee as bankFee}             // rename a method
import java.util.{List as JList, Random as _, *}   // rename List, hide Random, import the rest

// Note: the slide writes the renaming and the wildcard as two separate imports:
//   import java.util.{List as JList}
//   import java.util.{Random as _, *}
// Then the wildcard also imports java.util.List, which shadows scala.List, and
//   val xs: List[Int] = List(1, 2)
// fails with "object List in package java.util does not take parameters".
// Renaming List in the SAME import clause excludes it from the wildcard.

object ImportDemo:
  val jl: JList[Int] = new ArrayList[Int]()
  val xs: List[Int] = List(1, 2)            // still scala.List
  def biggerFee: Int = max(fee(500), bankFee(1000))

class Report:
  import scala.math.{max, min}     // only visible inside Report
  def clamp(x: Int): Int = max(0, min(100, x))

def area(r: Double): Double =
  import scala.math.Pi             // only inside this method
  Pi * r * r
