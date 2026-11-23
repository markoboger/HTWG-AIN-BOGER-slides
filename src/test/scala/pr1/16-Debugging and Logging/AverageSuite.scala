// Programming I — Lecture 16: MUnit suite from the testing slides.

package pr1.debugging

class AverageSuite extends munit.FunSuite:
  test("average of 2, 3, 1, 4 is 2.5"):
    assertEquals(average(List(2, 3, 1, 4)), 2.5)

  test("average of one element"):
    assertEquals(average(List(7)), 7.0)

  test("average stays in range"):
    val mean = average(List(2, 3, 1, 4))
    assert(mean > 0.0 && mean < 10.0)

  test("empty list is rejected"):
    intercept[IllegalArgumentException]:
      average(List.empty)
