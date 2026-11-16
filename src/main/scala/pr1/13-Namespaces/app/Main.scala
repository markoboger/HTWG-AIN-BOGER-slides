// Runs the examples of Lecture 13 and prints the results.
// Expected output is given as comments.
package app

import java.util.Locale

def show(label: String, value: Any): Unit = println(s"$label = $value")

@main def namespaces(): Unit =
  // Squants formats numbers with the default locale; on a German system it prints 3500,0 kWh.
  // The slides use an English locale:
  Locale.setDefault(Locale.US)
  packagesAndVisibility()
  squantsBasics()
  unitsAndBill()

def packagesAndVisibility(): Unit =
  println("--- Chapter 3: Packages and Imports in Scala ---")
  import bank.{Account, fee, MaxBalance}
  import bank.util.describe
  val ada = Account("Ada")
  show("Account(\"Ada\").owner", ada.owner) // Ada
  show("describe(ada)", describe(ada)) // Ada at 0
  show("fee(500)", fee(500)) // 5
  show("MaxBalance", MaxBalance) // 1000000

  import imports.{ImportDemo, Report, area}
  show("ImportDemo.xs", ImportDemo.xs) // List(1, 2)
  show("ImportDemo.jl.size", ImportDemo.jl.size) // 0
  show("ImportDemo.biggerFee", ImportDemo.biggerFee) // 10
  show("Report().clamp(150)", Report().clamp(150)) // 100
  show("area(1.0)", area(1.0)) // 3.141592653589793

  println("--- Chapter 4: Objects as Modules ---")
  import modules.StringUtils.*
  show(
    "capitalizeWords(\"hello scala world\")",
    capitalizeWords("hello scala world")
  ) // Hello Scala World

  println("--- Chapter 5: Visibility in Scala ---")
  import visibility.Savings
  val s = Savings("Bob")
  s.deposit(50)
  show("Savings(\"Bob\").report after deposit(50)", s.report) // Bob: 50
  show(
    "s.sameBalance(Savings(\"Eve\"))",
    s.sameBalance(Savings("Eve"))
  ) // false

  import companion.Account as CAccount
  val acc = CAccount("Ada", 100) // calls Account.apply
  show("Account(\"Ada\", 100).currentBalance", acc.currentBalance) // 100

  println("--- Chapter 6: Opaque Types ---")
  import money.Money.*
  val total: Euro = Euro(BigDecimal("1.50")) + Euro.cents(250)
  show("Euro(1.50) + Euro.cents(250)", total.amount) // 4.00

  println("--- Chapter 7: Export Clauses ---")
  import delegation.Copier
  val c = Copier()
  show("Copier().printerStatus", c.printerStatus) // ready
  c.copy() // [print] page

def squantsBasics(): Unit =
  println("--- Chapter 8: Example Library: Squants ---")
  import squants.energy.{Energy, KilowattHours, Kilowatts, WattHours}
  import squants.market.{EUR, Money, Price}
  import squants.time.Hours

  // Slide 33: the electricity bill in a few lines
  val consumption: Energy = KilowattHours(3500)
  val workPrice: Price[Energy] = EUR(0.32) / KilowattHours(1)
  val baseFee: Money = EUR(12) * 12
  val total: Money = workPrice * consumption + baseFee
  show("consumption", consumption) // 3500.0 kWh
  show("workPrice", workPrice) // 0.32 EUR/1.0 kWh
  show("baseFee", baseFee) // 144 EUR
  show("total.toFormattedString", total.toFormattedString) // €1264.00

  // Slide 35: units are singleton objects
  show("KilowattHours.symbol", KilowattHours.symbol) // kWh
  show("KilowattHours(3500)", KilowattHours(3500)) // 3500.0 kWh
  show(
    "KilowattHours(3500).in(WattHours)",
    KilowattHours(3500).in(WattHours)
  ) // 3500000.0 Wh

  // Slide 36: private constructors and companion factories
  // new Energy(3500, KilowattHours)   // does not compile:
  // error: private constructor Energy can only be accessed from class Energy in package squants.energy.
  show(
    "Money(BigDecimal(\"12.00\"), EUR)",
    Money(BigDecimal("12.00"), EUR)
  ) // 12 EUR
  show(
    "Energy(Kilowatts(2), Hours(3)).in(KilowattHours)",
    Energy(Kilowatts(2), Hours(3)).in(KilowattHours)
  ) // 6.0 kWh

  // Slide 37: opaque type Reading on top of Squants
  import energy.Metering.*
  val jan = Reading(12_400)
  val dec = Reading(15_900)
  show("dec.since(jan)", dec.since(jan)) // 3500.0 kWh

  // Slide 39: Squants' own implicit classes (Scala 2 style)
  import squants.energy.EnergyConversions.*
  import squants.energy.PowerConversions.*
  show("3500.kWh (Squants)", 3500.kWh) // 3500.0 kWh
  show("EnergyConversions(3500).kWh", EnergyConversions(3500).kWh) // 3500.0 kWh
  show("5.kW (Squants)", 5.kW) // 5.0 kW
  show("PowerConversions(5).kW", PowerConversions(5).kW) // 5.0 kW

def unitsAndBill(): Unit =
  import squants.energy.{Energy, KilowattHours}
  import squants.market.*
  import energy.Units.*
  import energy.given // the MoneyContext (1 EUR = 1.10 USD)

  // Slide 41: using our own extensions
  show("3500.kWh", 3500.kWh) // 3500.0 kWh
  show("5.kW", 5.kW) // 5.0 kW
  show("5.kW * 3.hours", 5.kW * 3.hours) // 15000.0 Wh
  show(
    "(5.kW * 3.hours).in(KilowattHours)",
    (5.kW * 3.hours).in(KilowattHours)
  ) // 15.0 kWh
  show("kWh(3500)", kWh(3500)) // 3500.0 kWh
  show("Units.kWh(3500)", energy.Units.kWh(3500)) // 3500.0 kWh

  // Slide 42 – without import Units.* this does not compile:
  // val e: Energy = 3500.kWh
  // error: value kWh is not a member of Int, but could be made available as an extension method.

  // Slides 43–44: the bill in EUR and USD
  val usage: Energy = 2.kW * 1750.hours // heat pump, 2 kW for 1750 h
  val priceUsd: Price[Energy] = 0.35.usd / 1.kWh
  val baseFee: Money = 12.eur * 12
  show("usage.in(KilowattHours)", usage.in(KilowattHours)) // 3500.0 kWh
  show("priceUsd", priceUsd) // 0.35 USD/1.0 kWh
  show("baseFee", baseFee) // 144 EUR

  val priceEur = priceUsd in EUR
  val total: Money = priceEur * usage + baseFee
  show("priceEur", priceEur) // 0.3181818181818181818181818181818182 EUR/1.0 kWh
  show("total.toFormattedString", total.toFormattedString) // €1257.64
  show(
    "(total in USD).toFormattedString",
    (total in USD).toFormattedString
  ) // $1383.40
  show("total to USD", total to USD) // 1383.400000000000000000000000000000
  show(
    "(priceUsd * usage + baseFee).toFormattedString",
    (priceUsd * usage + baseFee).toFormattedString
  ) // $1383.40
