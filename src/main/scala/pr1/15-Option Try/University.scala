// Programming I — Lecture 15: Option and Try
// University example from the task slide: StudentInput → Student, with Option and Try.

package pr1.optiontry

import java.time.LocalDate
import scala.io.Source
import scala.util.{Failure, Success, Try, Using}

case class StudentInput(matrikel: String, email: String, enrolled: String)
case class Student(matrikel: Int, email: String, enrolled: LocalDate)

enum LineResult:
  case Valid(student: Student)
  case InvalidInput(input: StudentInput)
  case FailedLine(message: String)

def validMatrikel(s: String): Option[Int] =
  Option(s).filter(_.nonEmpty).filter(_.forall(_.isDigit)).flatMap(_.toIntOption)

def validEmail(s: String): Option[String] =
  Option(s).filter(_.contains('@'))

def validDate(s: String): Option[LocalDate] =
  Try(LocalDate.parse(s)).toOption

def toStudent(in: StudentInput): Option[Student] =
  for
    matrikel <- validMatrikel(in.matrikel)
    email    <- validEmail(in.email)
    enrolled <- validDate(in.enrolled)
  yield Student(matrikel, email, enrolled)

def parseLine(line: String): Try[StudentInput] =
  line.split(",", -1).map(_.trim).toList match
    case matrikel :: email :: enrolled :: Nil =>
      Success(StudentInput(matrikel, email, enrolled))
    case _ =>
      Failure(IllegalArgumentException(s"expected 3 comma-separated fields: $line"))

def readConfig(path: String): Try[List[String]] =
  Try(Using.resource(Source.fromFile(path, "UTF-8"))(_.getLines().toList))

def readConfigResource(name: String = "students.csv"): Try[List[String]] =
  Try {
    val in = Option(Thread.currentThread.getContextClassLoader.getResourceAsStream(name))
      .getOrElse(throw java.io.FileNotFoundException(name))
    Using.resource(Source.fromInputStream(in, "UTF-8"))(_.getLines().toList)
  }

def processLines(lines: List[String]): List[LineResult] =
  lines.map { line =>
    parseLine(line) match
      case Failure(ex) => LineResult.FailedLine(ex.getMessage)
      case Success(input) =>
        toStudent(input) match
          case Some(student) => LineResult.Valid(student)
          case None          => LineResult.InvalidInput(input)
  }

def processStudents(path: String): Try[List[LineResult]] =
  readConfig(path).map(processLines)

def formatReport(results: List[LineResult]): String =
  results.map {
    case LineResult.Valid(student)       => s"valid: $student"
    case LineResult.InvalidInput(input)  => s"invalid input: $input"
    case LineResult.FailedLine(message)  => s"failed line: $message"
  }.mkString("\n")

@main def university(): Unit =
  readConfigResource() match
    case Failure(ex) =>
      println(s"could not read students.csv: ${ex.getMessage}")
    case Success(lines) =>
      println(formatReport(processLines(lines)))
