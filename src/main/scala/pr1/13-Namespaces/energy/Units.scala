// Slide 40: our own unit syntax with Scala 3 extension methods
package energy

import squants.energy.{Energy, KilowattHours, Kilowatts, Power}
import squants.market.{EUR, Money, USD}
import squants.time.{Hours, Time}

object Units:
  extension (n: Int)
    def kWh: Energy = KilowattHours(n)
    def kW: Power   = Kilowatts(n)
    def hours: Time = Hours(n)
    def eur: Money  = EUR(n)
  extension (d: Double)
    def eur: Money = EUR(d)
    def usd: Money = USD(d)
