//> using dep org.typelevel::squants:1.8.3
// Squants: units of measure as types

import squants.space.{Length, Meters, Kilometers}
import squants.mass.{Mass, Kilograms}
import squants.time.{Time, Minutes}
import squants.motion.KilometersPerHour
import squants.thermal.{Celsius, Fahrenheit}

// 1.0 Quantities with Constructors
val distance1 = Meters(5)
val weight1 = Kilograms(10)
val duration1 = Minutes(90)

// 1.1 Quantities with unit names as methods (Scala 3 extension methods)
import squants.space.LengthConversions.*
import squants.mass.MassConversions.*
import squants.time.TimeConversions.*

val distance2 = 5.meters
val weight2 = 10.kilograms
val duration2 = 90.minutes

// 2. Converting between units
distance1.toCentimeters
weight1.toPounds
duration1.toHours
Kilometers(42.195).toUsMiles

// 3. Arithmetic within one dimension
val total = 5.meters + 30.centimeters
total.toMeters
weight1 * 3
weight1 / 4

// 4. Mixing dimensions creates new ones
val area = 2.meters * 3.meters // Length * Length = Area
area.toSquareMeters

val speed = 100.meters / 9.58.seconds // Length / Time = Velocity
speed.in(KilometersPerHour)

val trip = KilometersPerHour(120) * 2.5.hours // Velocity * Time = Length
trip.in(Kilometers)

// 5. Temperature
val today = Celsius(21)
today.in(Fahrenheit)

// 6. Type safety: this does not compile
// 5.meters + 10.kilograms
