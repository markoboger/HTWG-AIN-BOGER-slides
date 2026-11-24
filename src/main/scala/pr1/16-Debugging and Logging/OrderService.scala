// Programming I — Lecture 16: Debugging and Logging
// scala-logging example from the slides: LazyLogging plus MDC context.

package pr1.debugging

import java.util.Locale
import scala.util.{Try, Success, Failure}
import com.typesafe.scalalogging.LazyLogging
import org.slf4j.MDC

case class Order(id: Int, items: List[String], total: Double)

class OrderService extends LazyLogging:
  def place(order: Order): Try[Order] =
    MDC.put("orderId", order.id.toString)
    try
      logger.info(s"Placing order with ${order.items.size} items")
      logger.debug(s"Items: ${order.items.mkString(", ")}")
      if order.total <= 0 then
        logger.warn(s"Rejected order, total = ${order.total}")
        Failure(IllegalArgumentException("invalid total"))
      else
        logger.info(s"Order accepted, total = ${String.format(Locale.US, "%.2f", order.total)} EUR")
        Success(order)
    finally MDC.remove("orderId")

@main def runOrders(): Unit =
  val service = OrderService()
  println(service.place(Order(1, List("book", "pen"), 12.5)))
  println(service.place(Order(2, Nil, 0.0)))
