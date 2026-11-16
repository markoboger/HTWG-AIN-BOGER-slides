// Slide 23: private and protected
package visibility

class Account(val owner: String):
  private var balance = 0
  protected def audit(): String = s"$owner: $balance"
  def deposit(amount: Int): Unit =
    require(amount > 0, "amount must be positive")
    balance += amount
  def sameBalance(other: Account): Boolean =
    balance == other.balance       // OK: private is per class

class Savings(o: String) extends Account(o):
  def report: String = audit()     // OK: protected in subclass
  // def peek = balance            // error: private (does not compile)
