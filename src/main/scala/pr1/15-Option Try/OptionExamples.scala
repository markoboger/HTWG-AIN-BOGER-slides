// Programming I — Lecture 15: Option and Try
// Option examples from the slides: lookup, User, findUser, lift, for-comprehensions.

package pr1.optiontry

val emails: Map[String, String] =
  Map("Ada" -> "ada@htwg.de", "Bob" -> "bob@htwg.de")

def findEmail(name: String): Option[String] = emails.get(name)

case class User(name: String, email: Option[String])

val ada: User = User("Ada", Some("ada@htwg.de"))
val bob: User = User("Bob", None)

class Users(users: Map[Int, User]):
  def findUser(id: Int): Option[User] = users.get(id)

val users: Users = Users(Map(1 -> User("Ada", Some("ada@htwg.de"))))

def describe(o: Option[Int]): String = o match
  case Some(n) if n > 0 => s"positive $n"
  case Some(n)          => s"non-positive $n"
  case None             => "nothing"

def emailDomain(id: Int): Option[String] =
  for
    user   <- users.findUser(id)
    email  <- user.email
    domain <- email.split("@").lift(1)
  yield domain

def parseAge(input: String): Int =
  input.toIntOption
    .filter(a => a >= 0 && a < 150)
    .getOrElse(0)

def priceTotal(prices: Map[String, Double], a: String, b: String): Option[Double] =
  for
    p <- prices.get(a)
    q <- prices.get(b)
  yield p + q

def safeDiv(a: Int, b: Int): Option[Int] =
  if b == 0 then None else Some(a / b)
