// Slide 30: export clauses (package named "delegation" because export is a keyword)
package delegation

class Printer:
  def print(s: String): Unit = println(s"[print] $s")
  def status: String = "ready"
  def reset(): Unit = ()

class Scanner:
  def scan(): String = "page"

class Copier:
  private val printer = Printer()
  private val scanner = Scanner()
  export printer.{print, status as printerStatus, reset as _}
  export scanner.scan
  def copy(): Unit = print(scan())
