// Slide 25: companion objects with an apply factory
package companion

class Account(val owner: String):
  private var balance = 0
  def currentBalance: Int = balance     // added so Main can print the balance

object Account:
  def apply(owner: String, initialBalance: Int = 0): Account =
    val a = new Account(owner)
    a.balance = initialBalance  // companion may access private members
    a
