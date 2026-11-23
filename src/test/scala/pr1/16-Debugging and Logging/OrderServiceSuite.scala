// Programming I — Lecture 16: tests for the LazyLogging OrderService example.

package pr1.debugging

class OrderServiceSuite extends munit.FunSuite:
  val service = OrderService()

  test("place accepts an order with a positive total"):
    val order = Order(1, List("book", "pen"), 12.5)
    assertEquals(service.place(order), Right(order))

  test("place rejects a non-positive total"):
    assertEquals(service.place(Order(2, Nil, 0.0)), Left("invalid total"))
    assertEquals(service.place(Order(3, List("x"), -1.0)), Left("invalid total"))
