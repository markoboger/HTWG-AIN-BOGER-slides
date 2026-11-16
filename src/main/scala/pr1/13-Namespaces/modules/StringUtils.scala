// Slide 19: an object is a namespace (module)
package modules

object StringUtils:
  val Separator = ", "
  def capitalizeWords(s: String): String =
    s.split(" ").map(cap).mkString(" ")
  private def cap(w: String): String =        // hidden helper
    if w.isEmpty then w else s"${w.head.toUpper}${w.tail}"
