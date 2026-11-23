// Programming I — Lecture 15: tests for the Try examples.

package pr1.optiontry

import java.io.FileNotFoundException
import java.nio.file.{Files, Path}
import scala.util.{Failure, Success}

class TrySuite extends munit.FunSuite:
  test("parse wraps toInt in Success or Failure"):
    assertEquals(parse("42"), Success(42))
    assert(parse("4x2").isFailure)
    assert(parse("4x2").failed.get.isInstanceOf[NumberFormatException])

  test("report pattern-matches on Try"):
    assertEquals(report(parse("7")), "got 7")
    assertEquals(report(parse("x")), "failed: For input string: \"x\"")

  test("map and flatMap on Try"):
    assertEquals(parse("21").map(_ * 2), Success(42))
    assert(parse("x").map(_ * 2).isFailure)
    assertEquals(parse("10").flatMap(x => divTry(100, x)), Success(10))
    val byZero = parse("0").flatMap(x => divTry(100, x))
    assert(byZero.isFailure)
    assert(byZero.failed.get.isInstanceOf[ArithmeticException])

  test("recover, recoverWith, getOrElse and toOption"):
    assertEquals(parse("x").getOrElse(-1), -1)
    assertEquals(parse("x").recover { case _: NumberFormatException => 0 }, Success(0))
    assertEquals(
      parse("x").recoverWith { case _: NumberFormatException => parse("1") },
      Success(1)
    )
    assertEquals(parse("5").toOption, Some(5))
    assertEquals(parse("x").toOption, None)

  test("for-comprehension chains parse and divTry"):
    val r = for
      x <- parse("10")
      y <- parse("2")
      q <- divTry(x, y)
    yield q
    assertEquals(r, Success(5))

    val failed = for
      x <- parse("10")
      y <- parse("0")
      q <- divTry(x, y)
    yield q
    assert(failed.isFailure)

  test("divTry reports division by zero as Failure"):
    assertEquals(divTry(10, 2), Success(5))
    assert(divTry(1, 0).isFailure)

  val numbersFile = FunFixture[Path](
    setup = { _ =>
      val path = Files.createTempFile("pr1-15-numbers", ".txt")
      Files.writeString(path, "10\n20\n30\n")
      path
    },
    teardown = { path => Files.deleteIfExists(path); () }
  )

  val emptyFile = FunFixture[Path](
    setup = { _ =>
      val path = Files.createTempFile("pr1-15-empty", ".txt")
      Files.writeString(path, "")
      path
    },
    teardown = { path => Files.deleteIfExists(path); () }
  )

  numbersFile.test("readLines and averageFromFile on a valid file"): path =>
    assertEquals(readLines(path.toString).map(_.size), Success(3))
    assertEquals(averageFromFile(path.toString), Success(20.0))

  emptyFile.test("averageFromFile rejects an empty file"): path =>
    val result = averageFromFile(path.toString)
    assert(result.isFailure)
    assert(result.failed.get.isInstanceOf[IllegalArgumentException])
    assertEquals(result.failed.get.getMessage, "no numbers")

  test("readLines fails when the file is missing"):
    val result = readLines("missing-pr1-15-file.txt")
    assert(result.isFailure)
    assert(result.failed.get.isInstanceOf[FileNotFoundException])
