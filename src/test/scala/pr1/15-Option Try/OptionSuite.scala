// Programming I — Lecture 15: tests for the Option examples.

package pr1.optiontry

class OptionSuite extends munit.FunSuite:
  test("findEmail returns Some for a known name and None otherwise"):
    assertEquals(findEmail("Ada"), Some("ada@htwg.de"))
    assertEquals(findEmail("Eve"), None)
    assertEquals(findEmail("Eve").map(_.length).getOrElse(0), 0)

  test("User makes a missing email visible in the type"):
    assertEquals(ada.email, Some("ada@htwg.de"))
    assertEquals(bob.email, None)

  test("describe pattern-matches on Option"):
    assertEquals(describe(Some(3)), "positive 3")
    assertEquals(describe(Some(0)), "non-positive 0")
    assertEquals(describe(None), "nothing")

  test("findUser.flatMap unwraps a nested Option"):
    assertEquals(users.findUser(1).map(_.email), Some(Some("ada@htwg.de")))
    assertEquals(users.findUser(1).flatMap(_.email), Some("ada@htwg.de"))
    assertEquals(users.findUser(2).flatMap(_.email), None)

  test("emailDomain chains findUser, email and lift in a for-comprehension"):
    assertEquals(emailDomain(1), Some("htwg.de"))
    assertEquals(emailDomain(3), None)

  test("Array.lift is a safe index"):
    val parts = "ada@htwg.de".split("@")
    assertEquals(parts.lift(1), Some("htwg.de"))
    assertEquals(parts.lift(2), None)
    assertEquals("no-at-sign".split("@").lift(1), None)

  test("parseAge uses toIntOption and a range filter"):
    assertEquals(parseAge("17"), 17)
    assertEquals(parseAge("4x2"), 0)
    assertEquals(parseAge("200"), 0)

  test("priceTotal looks up two map entries"):
    val prices = Map("apple" -> 0.5, "pear" -> 0.8)
    assertEquals(prices.get("kiwi"), None)
    assertEquals(prices.getOrElse("kiwi", 0.0), 0.0)
    assertEquals(priceTotal(prices, "apple", "pear"), Some(1.3))
    assertEquals(priceTotal(prices, "apple", "kiwi"), None)

  test("safeDiv returns None when dividing by zero"):
    assertEquals(safeDiv(10, 2), Some(5))
    assertEquals(safeDiv(1, 0), None)

  test("getOrElse, orElse and fold"):
    val some: Option[Int] = Some(3)
    val none: Option[Int] = None
    assertEquals(some.getOrElse(0), 3)
    assertEquals(none.getOrElse(0), 0)
    assertEquals(some.orElse(Some(7)), Some(3))
    assertEquals(none.orElse(Some(7)), Some(7))
    assertEquals(some.fold("none")(x => s"value $x"), "value 3")
    assertEquals(none.fold("none")(x => s"value $x"), "none")

  test("map, filter and Option as a collection"):
    assertEquals(Some(3).map(_ * 2), Some(6))
    assertEquals(Option.empty[Int].map(_ * 2), None)
    assertEquals(Some(3).filter(_ > 5), None)
    assertEquals(List(Some(1), None, Some(3)).flatten, List(1, 3))
    assertEquals(List("1", "x", "3").flatMap(_.toIntOption), List(1, 3))
