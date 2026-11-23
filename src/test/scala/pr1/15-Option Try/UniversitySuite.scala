// Programming I — Lecture 15: tests for the university example.

package pr1.optiontry

import java.time.LocalDate
import java.nio.file.Files
import scala.util.{Failure, Success}

class UniversitySuite extends munit.FunSuite:
  test("validMatrikel accepts digits only"):
    assertEquals(validMatrikel("12345"), Some(12345))
    assertEquals(validMatrikel("12a45"), None)
    assertEquals(validMatrikel(""), None)
    assertEquals(validMatrikel("007"), Some(7))

  test("validEmail requires @"):
    assertEquals(validEmail("ada@htwg.de"), Some("ada@htwg.de"))
    assertEquals(validEmail("not-an-email"), None)
    assertEquals(validEmail(""), None)

  test("validDate parses an ISO date"):
    assertEquals(validDate("2024-10-01"), Some(LocalDate.of(2024, 10, 1)))
    assertEquals(validDate("01.10.2024"), None)
    assertEquals(validDate("not-a-date"), None)

  test("toStudent combines the three validations"):
    val ok = StudentInput("12345", "ada@htwg.de", "2024-10-01")
    assertEquals(toStudent(ok), Some(Student(12345, "ada@htwg.de", LocalDate.of(2024, 10, 1))))
    assertEquals(toStudent(ok.copy(matrikel = "12a45")), None)
    assertEquals(toStudent(ok.copy(email = "nope")), None)
    assertEquals(toStudent(ok.copy(enrolled = "01.10.2024")), None)

  test("parseLine requires three comma-separated fields"):
    assertEquals(
      parseLine("12345, ada@htwg.de, 2024-10-01"),
      Success(StudentInput("12345", "ada@htwg.de", "2024-10-01"))
    )
    val bad = parseLine("only,two-fields")
    assert(bad.isFailure)
    assert(bad.failed.get.isInstanceOf[IllegalArgumentException])
    assert(bad.failed.get.getMessage.contains("expected 3 comma-separated fields"))

  test("processLines reports valid, invalid and failed lines"):
    val lines = List(
      "12345,ada@htwg.de,2024-10-01",
      "12a45,bob@htwg.de,2024-10-01",
      "only,two-fields"
    )
    val results = processLines(lines)
    assertEquals(
      results(0),
      LineResult.Valid(Student(12345, "ada@htwg.de", LocalDate.of(2024, 10, 1)))
    )
    assertEquals(
      results(1),
      LineResult.InvalidInput(StudentInput("12a45", "bob@htwg.de", "2024-10-01"))
    )
    results(2) match
      case LineResult.FailedLine(message) =>
        assert(message.contains("expected 3 comma-separated fields"))
      case other =>
        fail(s"expected FailedLine, got $other")

  test("readConfig and processStudents on a temporary csv"):
    val path = Files.createTempFile("pr1-15-students", ".csv")
    try
      Files.writeString(
        path,
        """12345,ada@htwg.de,2024-10-01
          |12a45,bob@htwg.de,2024-10-01
          |only,two-fields
          |""".stripMargin
      )
      val results = processStudents(path.toString).get
      assertEquals(results.size, 3)
      assert(results(0).isInstanceOf[LineResult.Valid])
      assert(results(1).isInstanceOf[LineResult.InvalidInput])
      assert(results(2).isInstanceOf[LineResult.FailedLine])
    finally
      Files.deleteIfExists(path)

  test("readConfigResource loads the sample students.csv"):
    val results = readConfigResource().map(processLines).get
    assertEquals(results.size, 6)
    assert(results.head.isInstanceOf[LineResult.Valid])
    assertEquals(results.count(_.isInstanceOf[LineResult.Valid]), 2)
    assertEquals(results.count(_.isInstanceOf[LineResult.InvalidInput]), 3)
    assertEquals(results.count(_.isInstanceOf[LineResult.FailedLine]), 1)
