// Slides 37–38: opaque type on top of Squants
package energy

import squants.energy.{Energy, KilowattHours}

object Metering:
  opaque type Reading = Energy         // inside Metering: Reading == Energy
  object Reading:
    def apply(kWh: Double): Reading =
      require(kWh >= 0, "a meter reading is never negative")
      KilowattHours(kWh)
  extension (r: Reading)
    def since(earlier: Reading): Energy = r - earlier

// Slide 38 – does not compile on purpose (outside Metering):
// val r: Reading = KilowattHours(5)
// error: Found: squants.energy.Energy  Required: Metering.Reading
// val s = jan + dec
// error: value + is not a member of Metering.Reading
