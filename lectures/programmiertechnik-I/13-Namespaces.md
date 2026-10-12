---
marp: true
theme: htwg
paginate: true
_paginate: false
footer: "![](../../themes/htwgin40.png)&nbsp;&nbsp;Prof. Dr. Marko Boger, Prof. Dr. Pascal Laube"
_footer: ""
---

![bg](../../themes/htwgin-titel.png)

### Prof. Dr. Marko Boger, Prof. Dr. Pascal Laube
## Programmiertechnik I
# Lecture 13: Namespaces, Packages and Visibility

---

<!-- _class: inhalt -->

<style scoped>
section { font-size: 22px; }
</style>

# Goals

<div class="columns" style="grid-template-columns: 1fr 260px; align-items: start;">
<div markdown="1">

In this lecture you will learn about

- namespaces and packages in Java and Scala
- imports: single, wildcard, static, renaming, hiding
- visibility: public, protected, package-private, private
- objects as modules, opaque types and export clauses
- nested classes, inner classes and nested objects

Supporting literature:

- Lewis, Art of Programming Using Scala, ch. 16, 17, 19
- Scala 3 Book: Packaging and Imports, Opaque Types

</div>
<div markdown="1">

<img src="assets/pt12-learn-scala-3-book.png" alt="Book cover: Learn Scala 3 the Fast Way" style="width:240px" />

</div>
</div>

---

<!-- _class: kapitel -->

## 1
# Namespaces

Why names need a home

---

# The Problem: Name Clashes

Programs grow, and names collide.

- `List` – is it `scala.List` or `java.util.List`?
- `Date` – `java.util.Date` or `java.sql.Date`?
- Two libraries both define a class `Parser`

A **namespace** is a named scope that makes names unique:

- the **simple name** `List` is short, but ambiguous
- the **fully qualified name** `java.util.List` is unique

In Java and Scala, namespaces are called **packages**.

---

# Packages Organize Code

Packages serve three purposes:

- **Uniqueness:** names only need to be unique *within* a package
- **Structure:** related classes live together (`bank.model`, `bank.ui`)
- **Access control:** a package is a boundary for visibility

Naming convention: reverse internet domain, all lower case

```
de.htwg.ain.bank.model
```

<p class="small">Lewis: "Bigger Programs" – packages become essential once a program spans many files.</p>

---

<!-- _class: kapitel -->

## 2
# Packages and Imports in Java

---

# Java Packages and Directories

The `package` clause must be the first statement in the file:

```java
package de.htwg.bank;

public class Account { ... }
```

In Java, the **directory structure must match** the package:

```
src/de/htwg/bank/Account.java
```

- At most **one public top-level class** per file, named like the file
- Without a `package` clause, a class lands in the *unnamed* package (only for tiny experiments)

---

# Java Imports

```java
import de.htwg.bank.Account;      // single-type import
import java.util.*;               // on-demand (wildcard) import
import static java.lang.Math.max; // static import of a member

public class Main {
    public static void main(String[] args) {
        Account a = new Account("Ada");
        java.util.List<Integer> xs = new ArrayList<>(List.of(1, 2));
        System.out.println(max(a.getBalance(), 1) + " " + xs);
    }
}
```

- `import` only saves typing – the fully qualified name always works
- `java.lang.*` is imported automatically (`String`, `Math`, ...)
- Imports must be at the top of the file, after `package`

---

# Java Visibility Modifiers

| Modifier | Class | Package | Subclass | Everywhere |
|---|:-:|:-:|:-:|:-:|
| `public` | ✓ | ✓ | ✓ | ✓ |
| `protected` | ✓ | ✓ | ✓ | |
| *(none)* package-private | ✓ | ✓ | | |
| `private` | ✓ | | | |

- The **default** in Java is *package-private*
- `protected` includes the whole package – often surprising

<p class="small">Source: Oracle Java Tutorials, "Controlling Access to Members of a Class".</p>

---

# Java Visibility in Code

```java
package de.htwg.bank;

public class Account {
    private int balance;          // only inside Account
    int branch;                   // package-private
    protected String owner;       // package + subclasses
    public Account(String owner) { this.owner = owner; }
    public int getBalance() { return balance; }
    public void deposit(int amount) {
        if (amount <= 0) throw new IllegalArgumentException("amount must be positive");
        balance += amount;
    }
}
```

- Fields `private`, access via `public` methods: **encapsulation**
- `deposit` can enforce an invariant – a public field could not

---

<!-- _class: kapitel -->

## 3
# Packages and Imports in Scala

---

# Scala Package Clauses

Same style as Java:

```scala
package de.htwg.bank

class Account(val owner: String)
```

Differences to Java:

- The directory structure **should** match, but the compiler does not enforce it
- Many public classes per file are allowed
- `java.lang.*`, `scala.*` and `Predef` are imported automatically

<p class="small">Scala 3 Book, "Packaging and Imports".</p>

---

# Nested Packages

Package clauses can enclose definitions – also several in one file:

```scala
package de.htwg.bank:

  class Account(val owner: String)

  package util:                       // de.htwg.bank.util
    def describe(a: Account): String = a.owner

package app:
  import de.htwg.bank.Account
  @main def run(): Unit = println(Account("Ada").owner)
```

- Inner packages see the members of outer packages
- Useful for small examples – in projects: one package per file

---

# Top-Level Definitions

Scala 3: `def`, `val`, `given`, ... can live **directly in a package**:

```scala
package de.htwg.bank

def fee(amount: Int): Int = amount / 100

val MaxBalance = 1_000_000
```

- In Scala 2 this needed a **package object**:<br>`package object bank { def fee(...) = ... }`
- Package objects are deprecated in Scala 3
- In Java, everything must be inside a class (`static` helper methods)

---

# Scala Imports: Selectors

```scala
import de.htwg.bank.Account              // one member
import de.htwg.bank.{Account, fee}       // several members
import de.htwg.bank.*                    // everything (Java: .*)
import scala.math.max                    // a method from an object
```

- `*` is the Scala 3 wildcard (Scala 2: `_`)
- Importing members of an object = Java's **static import**
- Same package: no import needed

---

# Renaming and Hiding

```scala
import java.util.{List as JList}          // rename
import de.htwg.bank.{fee as bankFee}      // rename a method
import java.util.{Random as _, *}         // hide Random, import the rest

val jl: JList[Int] = new ArrayList[Int]()
val xs: List[Int] = List(1, 2)            // still scala.List
```

- Renaming solves **name clashes** without fully qualified names
- `X as _` excludes a member from a wildcard import
- Scala 2 syntax: `{List => JList}`, `{Random => _, _}`

---

# Imports Anywhere

Unlike Java, a Scala `import` can appear in **any block**:

```scala
class Report:
  import scala.math.{max, min}     // only visible inside Report
  def clamp(x: Int): Int = max(0, min(100, x))

def area(r: Double): Double =
  import scala.math.Pi             // only inside this method
  Pi * r * r
```

- Keep imports close to where they are used
- Scope of an import = the enclosing block

<p class="small">Lewis, ch. 17 / 2nd ed. 3.8 "import Options".</p>

---

# Importing givens

A wildcard `*` does **not** import `given` instances:

```scala
object Codes:
  given Ordering[Account] = Ordering.by(_.getBalance)

import Codes.*         // all non-given members
import Codes.given     // only the givens
import Codes.{given Ordering[?]}  // givens of a given type

List(a, b).max         // uses the imported Ordering
```

- Makes it explicit **where** implicit values come from
- `_root_.pkg` refers to a package from the root if a name is shadowed

---

<!-- _class: kapitel -->

## 4
# Objects as Modules

Singleton objects as namespaces

---

# An object Is a Namespace

A Scala `object` groups related functions and constants – a **module**:

```scala
object StringUtils:
  val Separator = ", "
  def capitalizeWords(s: String): String =
    s.split(" ").map(cap).mkString(" ")
  private def cap(w: String): String =        // hidden helper
    if w.isEmpty then w else s"${w.head.toUpper}${w.tail}"

import StringUtils.*
capitalizeWords("hello scala world")   // "Hello Scala World"
```

- Access via `StringUtils.capitalizeWords` or after `import StringUtils.*`
- `private` helpers are invisible to users of the module

---

# Java: Static Utility Classes

```java
public final class StringUtils {
    private StringUtils() {}                       // no instances
    public static final String SEPARATOR = ", ";
    public static String capitalizeWords(String s) {
        StringBuilder b = new StringBuilder();
        for (String w : s.split(" ")) b.append(cap(w)).append(' ');
        return b.toString().trim();
    }
    private static String cap(String w) {
        return w.isEmpty() ? w : Character.toUpperCase(w.charAt(0)) + w.substring(1);
    }
}
```

- Java needs `final`, a `private` constructor and `static` everywhere
- Scala: an `object` is exactly one instance – and a real value (can extend traits, be passed around)

---

<!-- _class: kapitel -->

## 5
# Visibility in Scala

---

# Public by Default

| Java | Scala |
|---|---|
| `public` | *(default – no keyword)* |
| *(none)* package-private | `private[pkg]` |
| `protected` (package + subclasses) | `protected` (subclasses only) |
| `private` | `private` |

- Scala has no `public` keyword – everything is public unless restricted
- Scala's `protected` is **stricter** than Java's

<p class="small">Lewis, 16.1.1.2 "Visibility", 19.2.2 "Protected Visibility".</p>

---

# private and protected

```scala
class Account(val owner: String):
  private var balance = 0
  protected def audit(): String = s"$owner: $balance"
  def deposit(amount: Int): Unit =
    require(amount > 0, "amount must be positive")
    balance += amount
  def sameBalance(other: Account): Boolean =
    balance == other.balance       // OK: private is per class

class Savings(o: String) extends Account(o):
  def report: String = audit()     // OK: protected in subclass
  // def peek = balance            // error: private
```

- `private` members are **not** visible in subclasses (Lewis 19.2.1)
- Access to `other.balance` is allowed: same class

---

# Qualified Access: private[X]

```scala
package de.htwg.bank:
  class Account(val owner: String):
    private[bank] var branch = 0   // visible in package bank

  package util:
    def describe(a: Account) = s"${a.owner} at ${a.branch}"  // OK
```

- `private[bank]` ≈ Java's package-private, but **you choose** the boundary
- `private[Account]` – visible in the class and its nested definitions
- `protected[pkg]` exists as well
- `private[this]` (object-private) is deprecated in Scala 3 – the compiler infers it

---

# Companion Objects

A class and an `object` with the same name in the same file are **companions**:

```scala
class Account(val owner: String):
  private var balance = 0

object Account:
  def withBonus(owner: String): Account =
    val a = new Account(owner)
    a.balance = 10          // companion may access private members
    a
```

- Companions see each other's `private` members
- The object holds what Java would declare `static`
- Typical use: factory methods

<p class="small">Lewis, 16.1.5.2 "Introduction to Companion Objects".</p>

---

<!-- _class: kapitel -->

## 6
# Opaque Types

Hiding a type's representation

---

# Opaque Type Aliases

```scala
object Money:
  opaque type Euro = BigDecimal          // inside: Euro == BigDecimal
  object Euro:
    def apply(d: BigDecimal): Euro = d
    def cents(c: Long): Euro = BigDecimal(c) / 100
  extension (e: Euro)
    def +(o: Euro): Euro = (e: BigDecimal) + o
    def amount: BigDecimal = e

import Money.*
val total: Euro = Euro(BigDecimal("1.50")) + Euro.cents(250)   // 4.00
```

- **Inside** `Money` the compiler knows `Euro = BigDecimal`
- **Outside** `Euro` is a distinct type – only the public API is usable

---

# Opaque Types: Visibility for Types

```scala
val bad: Money.Euro = BigDecimal(3)
// error: Found: BigDecimal  Required: Money.Euro
```

- `private` hides **members**; `opaque` hides a **type's representation**
- Clients cannot mix up `Euro`, `Dollar` and plain `BigDecimal`
- **Zero runtime cost:** at runtime a `Euro` *is* a `BigDecimal` – no wrapper object
- Compare: a `case class Euro(value: BigDecimal)` allocates an object per value
- Java has no equivalent (only wrapper classes)

<p class="small">Scala 3 Book, "Opaque Types".</p>

---

<!-- _class: kapitel -->

## 7
# Export Clauses

Delegation made easy (Scala 3)

---

# export: Forward Selected Members

```scala
class Printer:
  def print(s: String): Unit = println(s"[print] $s")
  def status: String = "ready"
  def reset(): Unit = ()

class Scanner:
  def scan(): String = "page"

class Copier:
  private val printer = Printer()
  private val scanner = Scanner()
  export printer.{print, status as printerStatus, reset as _}
  export scanner.scan
  def copy(): Unit = print(scan())
```

- `export` creates **forwarder methods**: `Copier().print("x")` calls `printer.print("x")`
- Same selector syntax as `import`: rename with `as`, exclude with `as _`, `*` for all

---

# Delegation vs. Inheritance

| | Inheritance (`extends`) | Composition + `export` |
|---|---|---|
| Relation | *is-a* | *has-a* |
| What is visible | everything inherited | only what is exported |
| Combine several | one class only | any number of parts |
| Coupling | tight | loose, parts are `private` |

- "Prefer composition over inheritance" – without writing forwarders by hand
- Java: delegation needs one hand-written method per forwarded member
- `import` makes names usable *here*; `export` makes them **members** for others

<p class="small">Scala 3 Reference, "Export Clauses".</p>

---

<!-- _class: kapitel -->

## 8
# Nesting

---

# Nested Classes in Java

```java
public class Account {
    private int balance;
    public static class Statement {          // static nested class
        public final int value;
        public Statement(int value) { this.value = value; }
    }
    public class Card {                      // inner class
        public int balance() { return balance; }
    }
}

Account.Statement s = new Account.Statement(42);
Account.Card c = a.new Card();               // needs an Account
```

- **static nested:** just a namespace, no outer instance
- **inner:** each object belongs to one outer object, sees its `private` fields

---

# Nested Classes in Scala

Scala has no `static` – a nested class is always **inner**:

```scala
class Account(val owner: String):
  private var balance = 0
  class Card:
    def show: Int = balance

val a = Account("Ada")
val b = Account("Bob")
val c1 = new a.Card
val c2: b.Card = new b.Card   // a.Card and b.Card are different types
```

- `a.Card` is a **path-dependent type**
- Java's static nested class → put it into the **companion object**

---

# Nested Objects and Functions

Everything can be nested in Scala:

```scala
object Codes:
  object Limits:
    val Max = 1000          // Codes.Limits.Max

def total(xs: List[Int]): Int =
  def go(rest: List[Int], acc: Int): Int =   // local function
    if rest.isEmpty then acc else go(rest.tail, acc + rest.head)
  go(xs, 0)
```

- Objects act as **namespaces** for related constants and functions
- Local functions hide helpers – nobody outside can call `go`
- Java: local classes and lambdas, but no local methods

---

<!-- _class: kapitel -->

## 9
# Encapsulation

---

# Encapsulation: Best Practices

**Separate interface from implementation** (Lewis, 16.1.3):

- Make fields `private`, expose behaviour through methods
- Prefer `val` and immutable data – then public fields are harmless
- Choose the **smallest** visibility that works
- Use `private[pkg]` for helpers shared within a module
- One package per subsystem; avoid cyclic dependencies between packages
- Prefer explicit imports over wildcards in larger code bases

---

<style scoped>
table, th, td { font-size: 17px !important; padding: 2px 10px !important; }
</style>

# Summary: Java vs. Scala

| | Java | Scala 3 |
|---|---|---|
| Package & directory | must match | convention only |
| Package blocks | – | `package p:` nested |
| Top-level functions | – | yes |
| Static import | `import static` | import object members |
| Rename / hide | – | `as`, `as _` |
| Import position | top of file | anywhere |
| Default visibility | package-private | public |
| `protected` | package + subclasses | subclasses |
| Static nested class | `static class` | class in companion object |
| Utility module | `final` class + `static` | `object` |
| Hide representation | wrapper class | `opaque type` |
| Delegation | hand-written | `export` |

---

<!-- _class: inhalt -->

<style scoped>
section { font-size: 23px; }
</style>

# Summary

- Namespaces avoid name clashes; in Java and Scala they are packages
- Java: package = directory, imports at the top, `import static`
- Scala: package blocks, top-level definitions, imports anywhere with renaming and hiding
- Visibility: Java defaults to package-private, Scala to public
- `private[pkg]` qualifies access; companions share private members
- `object` as module; `opaque type` hides representations at zero cost; `export` delegates
- Nesting: Java static vs inner classes, Scala path-dependent types and nested objects

---

<!-- _class: aufgabe -->

# Task

(Task to fill)

- Reading: Learn Scala 3, Chapter 36

---

<!-- _class: abschluss -->

# Questions?

## Thank you!

marko.boger@htwg-konstanz.de
