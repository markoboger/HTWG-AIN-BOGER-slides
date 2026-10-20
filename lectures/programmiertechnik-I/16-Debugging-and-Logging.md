---
marp: true
theme: htwg-pt1
paginate: true
footer: "![](../../themes/htwgin40.png)&nbsp;&nbsp;Prof. Dr. Marko Boger, Prof. Dr. Pascal Laube"
_footer: ""
---

![bg](../../themes/htwgin-titel.png)

### Prof. Dr. Marko Boger, Prof. Dr. Pascal Laube
## Programmiertechnik I
# Lecture 16: Debugging and Logging

---

<!-- _class: inhalt -->

<style scoped>
section { font-size: 21px; }
</style>

# Goals

In this lecture you will learn about

- what a bug really is – and why the computer is never to blame
- running the debugger in Visual Studio Code with Metals
- breakpoints, logpoints, stepping, call stack, watches and the debug console
- writing debug messages – and why `println` is not enough
- using a logger: SLF4J, Logback and scala-logging
- log levels, context (MDC), configuration and JSON logs
- in which order to approach a bug

New tools: VS Code Debugger (Metals), SLF4J, Logback, scala-logging

---

<!-- _class: kapitel -->

## 1
# What Is a Bug?

---

# What Is a Bug?

<a href="https://www.youtube.com/watch?v=UPuTO9vg5gk"><img src="assets/pt16-bug-video.jpg" alt="Video thumbnail: What is a bug? (click to open on YouTube)" style="display: block; margin: 10px auto 0; height: 400px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.15);" /></a>

<p class="small" style="text-align: center; margin-top: 8px;">▶ <a href="https://www.youtube.com/watch?v=UPuTO9vg5gk">9th September 1947: First computer ‘bug’ found in the Harvard Mark II</a> – HistoryPod, YouTube</p>

---

<style scoped>
section { font-size: 23px; }
</style>

# Tools to Find Bugs

Bugs are no longer insects in hardware but errors in our software.

The computer executes the given code **correctly**, so there is no error in the code or execution of our code, but **in our thinking** and how we express our thoughts in code.

To debug a program is to find the **mismatch between our thoughts and the code** we wrote to express these.

To find a bug, we need to increase our understanding of what the code actually does. We can use

- a **debugger**, a tool that executes code line by line
- **debug messages**, print out states of the program while it runs

---

<style scoped>
section { font-size: 22px; }
</style>

# A Debugger Is a Last Resort

- A debugger does not find bugs – **you** do. It only shows you what the code does.
- Stepping through code line by line is slow and does not scale to large programs.
- A debugging session leaves nothing behind: no test, no log, no insight for the next person.
- If you need a debugger to understand your own code, the code is often **too complicated**.
- Better first: think, read the code, write a test, make functions small and pure.

<br>

> When the debugger is the right tool, use it **well** – that is what the next chapter is about.

---

<!-- _class: kapitel -->

## 2
# The Debugger in VS Code

---

# Debugger

<p style="text-align: center; font-size: 30px; margin-top: 140px;">▶ <a href="https://www.youtube.com/watch?v=zX-t5E5hQh0">Video: Using a Debugger</a></p>

<p class="small" style="text-align: center;">youtube.com/watch?v=zX-t5E5hQh0 (from the original lecture)</p>

---

<style scoped>
section { font-size: 21px; }
</style>

# How a Debugger Works

<div class="columns">
<div markdown="1">

- VS Code talks to a **debug adapter** via the *Debug Adapter Protocol* (DAP)
- For Scala, **Metals** is the debug adapter
- Metals starts your program in a JVM with debugging enabled (JDWP)
- The JVM can **pause** at any line and report all variables and the call stack

</div>
<div markdown="1">

```text
VS Code  ⇄  DAP  ⇄  Metals
                      ⇅ JDWP
                    JVM running
                    your program
```

</div>
</div>

You see: the current line, the variables, the call stack – while the program is paused.

---

<style scoped>
section { font-size: 20px; }
</style>

# Starting a Debug Session

<div class="columns">
<div markdown="1">

**Quick way:** Metals adds code lenses above every `@main` and test:

```scala
run | debug
@main def run(): Unit = ...
```

Click **debug**, or press **F5**.

</div>
<div markdown="1">

**Launch configuration** `.vscode/launch.json`:

```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "type": "scala",
      "request": "launch",
      "name": "Debug run",
      "mainClass": "run",
      "args": []
    }
  ]
}
```

</div>
</div>

---

<style scoped>
section { font-size: 21px; }
</style>

# Our Buggy Program

```scala
def average(xs: List[Int]): Double =
  var sum = 0
  for i <- 1 until xs.length do
    sum += xs(i)
  sum / xs.length

@main def run(): Unit =
  val grades = List(2, 3, 1, 4)
  println(s"Average: ${average(grades)}")   // expected 2.5
```

Output:

```text
Average: 2.0
```

The computer is right. Where is the mismatch with our thinking?

---

<style scoped>
section { font-size: 21px; }
</style>

# Breakpoints

- Click left of a line number – a **red dot** appears (or press **F9**)
- When execution reaches the line, the program **pauses before** executing it
- The line is highlighted; the *Run and Debug* view shows the state

```scala
def average(xs: List[Int]): Double =
  var sum = 0                            // ● breakpoint here
  for i <- 1 until xs.length do
    sum += xs(i)
  sum / xs.length
```

Breakpoints can be disabled, removed, or listed in the **Breakpoints** panel.

---

<style scoped>
section { font-size: 22px; }
</style>

# Stepping

| Action | Key | What it does |
|---|---|---|
| Continue | F5 | run until the next breakpoint |
| Step Over | F10 | execute the current line, do not enter calls |
| Step Into | F11 | enter the function called on this line |
| Step Out | ⇧F11 | finish the current function, return to the caller |
| Restart | ⇧⌘F5 | start the session again |
| Stop | ⇧F5 | end the session |

Rule of thumb: **Step Over** by default, **Step Into** only where you suspect the bug.

---

<style scoped>
section { font-size: 21px; }
</style>

# Variables and Watch

<div class="columns">
<div markdown="1">

**Variables** panel: all locals and parameters of the current frame

```text
▾ Local
    xs   = List(2, 3, 1, 4)
    sum  = 3
    i    = 1
```

Values that changed in the last step are **highlighted**.

</div>
<div markdown="1">

**Watch** panel: expressions you want to see after every step

```text
▾ Watch
    xs(i)              = 3
    xs.sum             = 10
    sum.toDouble / 4   = 0.75
```

You can also **edit** a variable's value while paused.

</div>
</div>

---

<style scoped>
section { font-size: 21px; }
</style>

# Call Stack

- Shows **how** you got to the current line: one frame per function call
- Click a frame to see **its** variables

```text
▾ CALL STACK   Paused on breakpoint
    average   Average.scala  4
    run       Average.scala 11
    run.main  Average.scala  9
```

- Very useful for recursion: each recursive call is its own frame
- And for exceptions: where was the function called from?

---

<style scoped>
section { font-size: 21px; }
</style>

# Debug Console

Paused after the loop (`sum = 8`), the **Debug Console** evaluates Scala expressions in the current frame:

```text
> xs.length
4
> xs(0)
2
> sum / xs.length
2
> sum.toDouble / xs.length
2.0
> xs.sum.toDouble / xs.length
2.5
```

Try out a fix **before** you change the code.

---

<style scoped>
section { font-size: 21px; }
</style>

# Conditional Breakpoints and Hit Counts

Right-click a breakpoint → **Edit Breakpoint**:

- **Expression:** pause only if the condition is true

```scala
for i <- 0 until 1_000_000 do
  process(data(i))        // ● condition: data(i) < 0
```

- **Hit count:** pause only after the line was reached *n* times, e.g. `500`

No need to press *Continue* a thousand times.

---

<style scoped>
section { font-size: 21px; }
</style>

# Logpoints

A **logpoint** prints a message instead of pausing – a `println` without changing the code.

Right-click the gutter → **Add Logpoint**; expressions go in curly braces:

```text
◆  i = {i}, xs(i) = {xs(i)}, sum = {sum}
```

Output in the Debug Console:

```text
i = 1, xs(i) = 3, sum = 0
i = 2, xs(i) = 1, sum = 3
i = 3, xs(i) = 4, sum = 4
```

Nothing to remove afterwards, nothing committed by accident.

---

<style scoped>
section { font-size: 21px; }
</style>

# Exception Breakpoints

In the **Breakpoints** panel, enable *Caught Exceptions* / *Uncaught Exceptions*:

- the debugger pauses **where an exception is thrown**, not where it ends the program
- you see the variables at the moment things went wrong

```scala
average(Nil)      // sum / 0 → ArithmeticException: / by zero
```

The debugger stops at `sum / xs.length` with `xs = List()` – the cause is obvious.

---

<style scoped>
section { font-size: 20px; }
</style>

# Walkthrough: Finding the Bugs

<div class="columns">
<div markdown="1">

1. Breakpoint on `var sum = 0`, **F5**
2. `xs = List(2, 3, 1, 4)` – input correct
3. **F10** into the loop: first `i = 1` – element `2` is skipped! **Bug 1**
4. Loop ends with `sum = 8` instead of `10`
5. Debug console: `sum / xs.length` → `2` – an **Int**! **Bug 2**: integer division

</div>
<div markdown="1">

Fixed version:

```scala
def average(xs: List[Int]): Double =
  require(xs.nonEmpty,
    "average of empty list")
  xs.sum.toDouble / xs.length
```

```text
Average: 2.5
```

Two mismatches between our thinking and our code.

</div>
</div>

---

<style scoped>
section { font-size: 22px; }
</style>

# Debugging Tests

- Metals shows **debug** code lenses on test classes and single tests (MUnit, ScalaTest)
- Turn the bug into a **failing test** first, then debug the test

```scala
class AverageSuite extends munit.FunSuite:
  test("average of 2, 3, 1, 4 is 2.5"):
    assertEquals(average(List(2, 3, 1, 4)), 2.5)
```

- After the fix, the test stays – the bug can never come back unnoticed
- A debugging session is gone after you close it; a test is not

---

<!-- _class: kapitel -->

## 3
# Logging

---

<style scoped>
section { font-size: 22px; }
</style>

# Debug Messages with `println`

```scala
def average(xs: List[Int]): Double =
  println(s"average called with $xs")
  ...
```

Quick, but:

- no way to switch it off without changing the code
- no time stamp, no source, no severity
- always goes to the console – not to a file, not to a server
- gets forgotten and committed
- string is built even if nobody reads it

A **logger** solves all of this.

---

<style scoped>
section { font-size: 21px; }
</style>

# Log Levels

| Level | Use for | Example |
|---|---|---|
| `ERROR` | something failed, needs attention | payment could not be processed |
| `WARN` | unexpected, but the program continues | order rejected, invalid total |
| `INFO` | important business events | order accepted |
| `DEBUG` | details for developers | the items of an order |
| `TRACE` | very fine-grained flow | entering / leaving functions |

The configured level is a **threshold**: at `INFO`, only `INFO`, `WARN` and `ERROR` are written.

---

<style scoped>
section { font-size: 21px; }
</style>

# The Scala Logging Stack

<div class="columns">
<div markdown="1">

- **SLF4J** – *Simple Logging Facade for Java*: the API everyone uses
- **Logback** – the implementation: formats and writes the messages
- **scala-logging** – thin Scala wrapper around SLF4J, using macros

Library code depends only on the facade, the application chooses the backend.

</div>
<div markdown="1">

```text
your code
   │  logger.info(...)
scala-logging
   │
SLF4J (API)
   │
Logback  →  console, file, JSON
```

</div>
</div>

```scala
//> using dep "com.typesafe.scala-logging::scala-logging:3.9.5"
//> using dep "ch.qos.logback:logback-classic:1.5.6"
```

---

<style scoped>
section { font-size: 20px; }
</style>

# scala-logging: `LazyLogging`

```scala
import com.typesafe.scalalogging.LazyLogging

case class Order(id: Int, items: List[String], total: Double)

class OrderService extends LazyLogging:
  def place(order: Order): Either[String, Order] =
    logger.info(s"Placing order with ${order.items.size} items")
    logger.debug(s"Items: ${order.items.mkString(", ")}")
    if order.total <= 0 then
      logger.warn(s"Rejected order, total = ${order.total}")
      Left("invalid total")
    else
      logger.info(f"Order accepted, total = ${order.total}%.2f EUR")
      Right(order)
```

`LazyLogging` provides a `logger`, created on first use and named after the class.

---

<style scoped>
section { font-size: 21px; }
</style>

# `LazyLogging` vs. `StrictLogging`

```scala
import com.typesafe.scalalogging.StrictLogging

object Payment extends StrictLogging:
  def charge(amount: Double): Unit =
    logger.trace(s"charge($amount)")
    logger.info("Charging {} EUR", amount)
```

- `LazyLogging`: logger is a `lazy val` – created when first needed
- `StrictLogging`: logger is created together with the object
- `AnyLogging` / `Logger(...)`: create a logger explicitly
- `{}` placeholders are the SLF4J style; Scala string interpolation works just as well

---

<style scoped>
section { font-size: 21px; }
</style>

# Lazy Messages for Free

```scala
logger.debug(s"State: ${expensiveDump(world)}")
```

scala-logging is a **macro**: the compiler rewrites the call to

```scala
if logger.underlying.isDebugEnabled then
  logger.underlying.debug(s"State: ${expensiveDump(world)}")
```

- When `DEBUG` is off, `expensiveDump` is **never called**
- No cost for disabled log statements – you can leave them in the code
- Remember *by-name* parameters from lecture 14: same idea, done by a macro

---

<style scoped>
section { font-size: 19px; }
</style>

# Configuration: `logback.xml`

Put it in `src/main/resources` (or a resource directory):

```xml
<configuration>
  <appender name="CONSOLE" class="ch.qos.logback.core.ConsoleAppender">
    <encoder>
      <pattern>%d{HH:mm:ss.SSS} %highlight(%-5level) %cyan(%logger{15}) - %msg%n</pattern>
    </encoder>
  </appender>

  <logger name="OrderService" level="DEBUG" />
  <logger name="org.http4s" level="WARN" />

  <root level="INFO">
    <appender-ref ref="CONSOLE" />
  </root>
</configuration>
```

- **Per-package levels:** `DEBUG` for your code, `WARN` for noisy libraries
- Change levels **without recompiling**

---

<style scoped>
section { font-size: 20px; }
</style>

# Colored Console Output

With `%highlight(...)` and `%cyan(...)` in the pattern:

<pre style="font-size: 17px; line-height: 1.5;">
11:56:20.239 <span style="color:#4c7cf3">INFO </span> <span style="color:#1aa3a3">OrderService</span> - Placing order with 2 items
11:56:20.244 DEBUG <span style="color:#1aa3a3">OrderService</span> - Items: Book, Pen
11:56:20.247 <span style="color:#4c7cf3">INFO </span> <span style="color:#1aa3a3">OrderService</span> - Order accepted, total = 23.50 EUR
11:56:20.248 <span style="color:#4c7cf3">INFO </span> <span style="color:#1aa3a3">OrderService</span> - Placing order with 0 items
11:56:20.248 DEBUG <span style="color:#1aa3a3">OrderService</span> - Items:
11:56:20.248 <span style="color:#d33">WARN </span> <span style="color:#1aa3a3">OrderService</span> - Rejected order, total = 0.0
11:56:20.248 <span style="color:#4c7cf3">INFO </span> <span style="color:#1aa3a3">Payment$</span> - Charging 23.5 EUR
</pre>

- Time, level, source and message – at a glance
- `ERROR` and `WARN` stand out immediately

---

<style scoped>
section { font-size: 20px; }
</style>

# Context with MDC

The **Mapped Diagnostic Context** attaches key-value pairs to every log line of the current thread:

```scala
import org.slf4j.MDC

def place(order: Order): Either[String, Order] =
  MDC.put("orderId", order.id.toString)
  try
    logger.info("Placing order")
    ...
  finally MDC.remove("orderId")
```

Pattern `... [%X{orderId}] - %msg%n` gives:

```text
11:56:20.239 INFO  OrderService [1] - Placing order with 2 items
11:56:20.248 WARN  OrderService [2] - Rejected order, total = 0.0
```

All lines of one request can be found with a single search.

---

<style scoped>
section { font-size: 19px; }
</style>

# Appenders and Rolling Files

```xml
<appender name="FILE" class="ch.qos.logback.core.rolling.RollingFileAppender">
  <file>logs/shop.log</file>
  <rollingPolicy class="ch.qos.logback.core.rolling.TimeBasedRollingPolicy">
    <fileNamePattern>logs/shop.%d{yyyy-MM-dd}.log</fileNamePattern>
    <maxHistory>7</maxHistory>
  </rollingPolicy>
  <encoder>
    <pattern>%d %-5level %logger [%X{orderId}] - %msg%n</pattern>
  </encoder>
</appender>

<root level="INFO">
  <appender-ref ref="CONSOLE" />
  <appender-ref ref="FILE" />
</root>
```

- One log statement, **several destinations**: console, file, network
- A new file every day, only the last 7 days are kept

---

<style scoped>
section { font-size: 19px; }
</style>

# Structured Logging: JSON

Replace the pattern encoder with the Logstash encoder:

```xml
<encoder class="net.logstash.logback.encoder.LogstashEncoder" />
```

```scala
//> using dep "net.logstash.logback:logstash-logback-encoder:7.4"
```

Every log line becomes a JSON object – including the MDC fields:

```json
{"@timestamp":"2026-10-12T11:56:20.248+02:00","level":"WARN",
 "logger_name":"OrderService","thread_name":"main","orderId":"2",
 "message":"Rejected order, total = 0.0"}
```

Machines can search, filter and chart it: Elasticsearch/Kibana, Grafana Loki, …

---

<style scoped>
section { font-size: 21px; }
</style>

# Good Logging Practice

- Log **events**, not every line: *what happened*, with the relevant IDs
- Choose the level honestly – not everything is an `ERROR`
- Pass exceptions as the last argument: `logger.error("Payment failed", e)` → full stack trace
- Never log passwords, tokens or personal data
- Keep log statements in the code – switch them by level, not by deleting
- Alternatives in the Scala world:
  - **log4cats** – logging for Cats Effect (pure, `IO`-based)
  - **scribe** – fast, pure-Scala logger without XML configuration

---

<!-- _class: kapitel -->

## 4
# How to Debug

---

<style scoped>
section { font-size: 22px; }
</style>

# Debugging Order (Marko's advice) – TODO

<div style="border: 3px dashed #c00; padding: 1em; color: #c00;">

**Placeholder – to be filled in by Marko.**

In which order should a bug be approached?

1. …
2. …
3. …

</div>

---

<!-- _class: inhalt -->

<style scoped>
section { font-size: 22px; }
</style>

# Summary

- A bug is a mismatch between our thinking and our code – the computer is right
- The debugger is a last resort, but a powerful one
- VS Code + Metals: code lens or `launch.json`, then F5
- Breakpoints, conditional breakpoints, logpoints and exception breakpoints
- Step over / into / out, variables, watch, call stack, debug console
- Turn a bug into a failing test before you fix it
- Prefer a logger over `println`: levels, sources, time stamps, destinations
- SLF4J + Logback + scala-logging; macros make disabled messages free
- `logback.xml`: per-package levels, appenders, rolling files, colors, JSON
- MDC adds context such as an order ID to every line

---

<!-- _class: aufgabe -->

# Task

(Task to fill)

---

<!-- _class: abschluss -->

# Questions?

## Thank you!

marko.boger@htwg-konstanz.de
