// Slides 27–28: opaque type aliases
package money

object Money:
  opaque type Euro = BigDecimal          // inside: Euro == BigDecimal
  object Euro:
    def apply(d: BigDecimal): Euro = d
    def cents(c: Long): Euro = BigDecimal(c) / 100
  extension (e: Euro)
    def +(o: Euro): Euro = (e: BigDecimal) + o
    def amount: BigDecimal = e

// Slide 28 – does not compile on purpose:
// val bad: Money.Euro = BigDecimal(3)
// error: Found: BigDecimal  Required: Money.Euro
