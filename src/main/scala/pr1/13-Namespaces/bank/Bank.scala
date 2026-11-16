// Slides 12–14 and 24: package clauses, nested packages, top-level definitions, private[bank]
package bank:

  class Account(val owner: String):
    private[bank] var branch = 0         // slide 24: visible in package bank

  package util:                          // bank.util (slide 13)
    // slide 24 version; slide 13 shows the shorter `def describe(a: Account): String = a.owner`
    def describe(a: Account): String = s"${a.owner} at ${a.branch}"   // OK: inside bank

  // slide 14: top-level definitions
  def fee(amount: Int): Int = amount / 100

  val MaxBalance = 1_000_000

package app:                             // slide 13: a second package in the same file
  import bank.Account
  @main def run(): Unit = println(Account("Ada").owner)   // ./mill pr1.namespaces.runMain app.run
