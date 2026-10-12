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
# Lecture 17: Domain-Driven Design

---

<!-- _class: inhalt -->

<style scoped>
section { font-size: 19px; }
</style>

# Goals

In this lecture you will learn

- why software should contain a **model of the domain**
- the **ubiquitous language** and the idea of a model in code
- Evans' building blocks: entities, value objects, aggregates, bounded contexts
- OO features for modelling a domain: **inheritance**, **traits**, **generic types**,
  **named and default parameters**, **varargs**
- how the same ideas look in Java

Supporting literature:

- Eric Evans, *Domain-Driven Design: Tackling Complexity in the Heart of Software*, Addison-Wesley, 2003

---

<!-- _class: kapitel -->

## 1
# Modelling a Domain

Software is a model of a piece of the world

---

# What Is a Domain?

- The **domain** is the subject area the software is about
  - a library, a shop, a bank, a university, a game
- Developers usually are **not** experts in the domain
- **Domain experts** are: librarians, sales people, bankers, examiners
- The software must capture *their* knowledge
- Evans calls this process **Crunching Knowledge** (Chapter 1)

> The hard part of software is often not the technology, but understanding the domain.

---

# A Model of the Domain

- A **model** is a simplified, selective view of the domain
- It keeps what matters for the problem and leaves out the rest
  - a library cares about *ISBN*, *loan period*, *member*
  - it does not care about the paper weight of a book
- The same model is used
  - in conversations with domain experts
  - in diagrams
  - **in the code**
- Evans: the model and the implementation should be bound together – **Model-Driven Design** (Chapter 3, "Binding Model and Implementation")

---

# Ubiquitous Language

- Evans, Chapter 2 "Communication and the Use of Language"
- Team and domain experts use **one shared language**
- The same words appear in talks, documents **and code**

| Librarian says | Code says |
|---|---|
| "A member borrows a book" | `desk.lend(book, member)` |
| "The loan period is 28 days" | `def loanDays = 28` |
| "A DVD is a kind of item" | `class Dvd extends Item` |
| "Magazines can be reserved" | `class Magazine ... with Reservable` |

- If the code uses other words than the experts, something is wrong

---

# Our Running Example: A Library

- **Items**: books, DVDs, magazines – each with title and ISBN
- **Members** borrow items
- A **loan** connects an item, a member and a loan period
- Some items can be **reserved**, some cost a **fee**
- The library keeps items in a **repository** and a **catalog**
- The **loan desk** makes sure an item is never lent twice

We will model this domain step by step with Scala 3.

---

<!-- _class: kapitel -->

## 2
# Building Blocks

Evans' vocabulary for a model in code

---

# Value Objects

- Defined only by their **values**, have no identity
- Immutable – in Scala: a `case class`
- Two ISBNs with the same digits are the same ISBN

```scala
case class Isbn(value: String):
  require(value.length == 13, "ISBN must have 13 digits")

case class Money(cents: Long):
  def +(o: Money) = Money(cents + o.cents)
  def *(n: Int)   = Money(cents * n)

Isbn("9780321125217") == Isbn("9780321125217")   // true
```

- Use them instead of raw `String` and `Long`: the type says what it is

---

# Entities

- Have an **identity** that stays the same while their data changes
- Ann marries and changes her name – she is still the same member

```scala
class Member(val id: Int, var name: String):
  override def equals(o: Any) = o match
    case m: Member => m.id == id
    case _         => false
  override def hashCode = id.hashCode

Member(1, "Ann") == Member(1, "Ann B.")   // true
```

- Equality is based on the **id**, not on all fields
- Evans, Chapter 5: ENTITIES (a.k.a. reference objects) and VALUE OBJECTS

---

# Aggregates

- A group of objects that is changed **as one unit**
- One **root** object guards the rules (invariants) of the group
- Rule: *an item can only be on loan once*

```scala
class LoanDesk:
  private var loans = Map.empty[Isbn, Loan]

  def lend(item: Item, m: Member): Either[String, Loan] =
    if loans.contains(item.isbn) then Left(s"${item.title} is already on loan")
    else
      val l = Loan(item, m, days = item.loanDays)
      loans = loans + (item.isbn -> l)
      Right(l)
```

- Nobody outside may change `loans` directly – it is `private`
- Evans, Chapter 6 "The Life Cycle of a Domain Object": AGGREGATES, FACTORIES, REPOSITORIES

---

# Bounded Context

- One big model for everything does not work
- A word may mean different things in different parts of an organisation
  - *Item* in the **lending** context: something that can be borrowed
  - *Item* in the **purchasing** context: a line on an invoice
- A **bounded context** draws a border: inside, the model is consistent
- In code: separate **packages** / modules (see Lecture 13 Namespaces)
- Evans, Chapter 14 "Maintaining Model Integrity": BOUNDED CONTEXT, CONTEXT MAP

---

<!-- _class: kapitel -->

## 3
# Inheritance

"A DVD is a kind of item"

---

<style scoped>
section { font-size: 20px; }
pre { font-size: 15px; }
</style>

# Inheritance: Is-A in the Domain

- The domain experts say: *books, DVDs and magazines are items*
- Common data and behaviour go into an `abstract` **superclass** – there are no "plain" items

<div class="columns" style="grid-template-columns: 1fr 1fr; gap: 16px;">
<div markdown="1">

Scala

```scala
abstract class Item(val title: String,
                    val isbn: Isbn):
  def loanDays: Int                // abstract
  def describe: String =           // concrete
    s"$title ($loanDays days)"

class Book(title: String, isbn: Isbn,
           val author: String)
    extends Item(title, isbn):
  def loanDays = 28
```

</div>
<div markdown="1">

Java

```java
abstract class Item {
  protected final String title;
  Item(String title) { this.title = title; }
  abstract int loanDays();
}

class Book extends Item {
  Book(String title) { super(title); }
  int loanDays() { return 28; }
}
```

</div>
</div>

- `Book` must implement `loanDays`; Java needs fields, constructor and `super(...)` by hand

---

# Overriding Behaviour

```scala
class Dvd(title: String, isbn: Isbn, val minutes: Int)
    extends Item(title, isbn):
  def loanDays = 7
  override def describe = s"DVD: ${super.describe}"
```

```scala
val items: List[Item] = List(ddd, film)
items.foreach(i => println(i.describe))
// Domain-Driven Design (28 days)
// DVD: Metropolis (7 days)
```

- `override` replaces inherited behaviour, `super` calls the original
- **Polymorphism**: the call `i.describe` picks the right method at runtime

---

# Sealed Hierarchies: Closed Sets of Cases

- Sometimes the domain has a **fixed** list of cases
- `sealed`: all subtypes are in the same file – the compiler knows them all

```scala
sealed trait LoanState
case object Available                    extends LoanState
case class  OnLoan(to: Member, days: Int) extends LoanState
case object Lost                         extends LoanState

def label(s: LoanState): String = s match
  case Available    => "available"
  case OnLoan(m, d) => s"on loan to ${m.name} for $d days"
  case Lost         => "lost"
```

- Forget a case and the compiler warns you
- Compare: `enum` in Lecture 08

---

# When Not to Inherit

- Inheritance is the **strongest** coupling between classes
- Only use it for a true **is-a** relationship of the domain
  - a `Dvd` *is an* `Item` ✔
  - a `LoanDesk` *is a* `Map` ✘ – it *has a* map
- Deep hierarchies are hard to change
- Prefer **composition** (has-a) and **traits** for optional abilities
- Scala and Java: a class has exactly **one** superclass

---

<!-- _class: kapitel -->

## 4
# Interfaces and Traits

"Magazines can be reserved"

---

# Traits: Abilities, Not Kinds

- Not every item can be reserved, not every item costs a fee
- These are **abilities** that cut across the hierarchy
- A **trait** describes such an ability

```scala
trait Reservable:
  private var queue = List.empty[Member]
  def reserve(m: Member): Unit = queue = queue :+ m
  def nextInLine: Option[Member] = queue.headOption

trait Priced:
  def fee: Money                                   // abstract
  def feeFor(days: Int): Money = fee * days        // concrete
```

---

# Mixing Traits into Classes

```scala
class Magazine(title: String, isbn: Isbn)
    extends Item(title, isbn) with Reservable with Priced:
  def loanDays = 14
  def fee      = Money(20)
```

```scala
val mag = Magazine("c't", Isbn("9771234567003"))
mag.reserve(ann)
mag.nextInLine.map(_.name)   // Some(Ann)
mag.feeFor(14)               // Money(280)
```

- One superclass, but **many traits**
- The class reads like the ubiquitous language: *a magazine is an item that is reservable and priced*

---

# Traits as Types

- A trait is also a **type** – code can ask only for the ability it needs

```scala
def reserveAll(things: List[Reservable], m: Member): Unit =
  things.foreach(_.reserve(m))

def totalCost(things: List[Priced], days: Int): Money =
  things.map(_.feeFor(days)).foldLeft(Money(0))(_ + _)
```

- `reserveAll` does not care whether it gets magazines or anything else
- Small traits keep dependencies small
- Evans, Chapter 10 "Supple Design": INTENTION-REVEALING INTERFACES

---

# Interfaces in Java

```java
interface Reservable {
  void reserve(String member);
  default boolean isReservable() { return true; }
}

class Magazine extends Item implements Reservable {
  private final List<String> queue = new ArrayList<>();
  Magazine(String title) { super(title); }
  int loanDays() { return 14; }
  public void reserve(String member) { queue.add(member); }
}
```

- `implements` many interfaces, `extends` one class
- Since Java 8: `default` methods – but **no state** (no fields)
- Scala traits may hold state (`queue`) – closer to the domain idea

---

# `given`: Providing an Instance

```scala
trait Show[A]:                     // a type class: "values of A can be shown"
  def show(a: A): String

given Show[Book] with              // the instance for Book
  def show(b: Book) = s"${b.title} (${b.genre})"

given Show[Genre] with             // the instance for Genre
  def show(g: Genre) = g.toString.toLowerCase
```

- A **type class** describes an ability – `Book` itself is not changed
- A `def` or `val` defines a value that you use **by name**
- A `given` defines a value that the compiler finds **by its type**: "the `Show` for `Book`"
- Instances for library types like `Int` can be written the same way

---

# `using`: Receiving an Instance

```scala
def printAll[A](xs: List[A])(using s: Show[A]): Unit =
  xs.foreach(x => println(s.show(x)))

printAll(List(ddd, momo))      // compiler passes the given Show[Book]
// Domain-Driven Design (Science)
// Momo (Children)

def describe[A: Show](a: A): String = summon[Show[A]].show(a)
describe(ddd)                  // Domain-Driven Design (Science)
```

- A `using` parameter list is filled in by the **compiler** with a matching `given`
- No `given Show[Member]`? → `printAll(members)` does **not compile**
- `[A: Show]` (context bound) is short for `(using Show[A])`; `summon[Show[A]]` fetches it

---

# `derives`: the Counterpart of `extends`

```scala
import scala.language.strictEquality

enum Genre derives CanEqual:
  case Novel, Science, Children

case class Isbn(value: String) derives CanEqual

Genre.Novel == Genre.Science                     // false
Isbn("9780321125217") == Isbn("9780321125217")   // true
Genre.Novel == Isbn("9780321125217")             // compile error
```

- `extends`: the type **is a** … and **inherits** its members
- `derives`: the compiler **writes the `given` for you** – an instance of the type class `CanEqual`
- `CanEqual`: with `strictEquality`, `==` only compiles for types that allow it

---

# What `derives` Replaces

The `given`, written by hand:

```scala
enum Format:
  case Paper, Ebook
object Format:
  given CanEqual[Format, Format] = CanEqual.derived
```

The same, written by the compiler with `derives`:

```scala
enum Format derives CanEqual:
  case Paper, Ebook

case class Book(title: String, isbn: Isbn, genre: Genre)
    derives CanEqual, ReadWriter
```

- Several type classes at once; `ReadWriter` (uPickle) turns a `Book` into JSON – Lecture 19
- `write(ddd)` → `{"title":"Domain-Driven Design",…,"genre":"Science"}`

---

<!-- _class: kapitel -->

## 5
# Generic Types

One repository for all kinds of things

---

# Repository: A Generic Abstraction

- Evans: a **REPOSITORY** gives access to stored domain objects (Chapter 6)
- Books, members and loans all need one – write it **once**

```scala
trait Repository[K, T]:
  def save(key: K, t: T): Unit
  def find(key: K): Option[T]
  def all: List[T]

class InMemoryRepository[K, T] extends Repository[K, T]:
  private var store = Map.empty[K, T]
  def save(key: K, t: T): Unit = store = store + (key -> t)
  def find(key: K): Option[T]  = store.get(key)
  def all: List[T]             = store.values.toList
```

---

# Using the Generic Repository

```scala
val items   = InMemoryRepository[Isbn, Item]()
val members = InMemoryRepository[Int, Member]()

items.save(ddd.isbn, ddd)
items.find(ddd.isbn).map(_.title)   // Some(Domain-Driven Design)

members.save(1, ann)
members.find(1).map(_.name)         // Some(Ann)
```

- `K` and `T` are **type parameters**, filled in at use
- The compiler checks: `items.save(1, ann)` does **not** compile
- Value objects as keys (`Isbn`) instead of `String` – no mix-ups

---

# Upper Bounds: `T <: Item`

- Sometimes a generic type must be **some kind of** item

```scala
def longest[T <: Item](items: List[T]): Option[T] =
  items.maxByOption(_.loanDays)

case class Shelf[+T <: Item](label: String, items: List[T]):
  def titles: List[String] = items.map(_.title)
```

```scala
longest(List(ddd, film)).map(_.title)   // Some(Domain-Driven Design)
val shelf: Shelf[Item] = Shelf[Book]("SE", List(ddd))
```

- `T <: Item`: we may call `loanDays` and `title` on `T`
- `+T` (covariance): a shelf of books **is a** shelf of items

---

# Generics in Java

```java
class Repo<K, T> {
  private final Map<K, T> store = new HashMap<>();
  void save(K k, T t) { store.put(k, t); }
  Optional<T> find(K k) { return Optional.ofNullable(store.get(k)); }
}

Repo<Isbn, Item> r = new Repo<>();
r.save(new Isbn("978"), b);
```

- `<K, T>` instead of `[K, T]`
- Upper bound: `<T extends Item>`
- Variance in Java at the use site: `List<? extends Item>`
- `record Isbn(String value)` – Java's value object (since Java 16)

---

<!-- _class: kapitel -->

## 6
# Named and Default Parameters

Calls that read like the domain

---

<style scoped>
pre { font-size: 17px; }
</style>

# Default Parameters

- What does this mean? Which number is the loan period, what is `true`?

```scala
Loan(ddd, ann, 28, 0, true)
```

- Better: give the parameters **defaults** that document the domain rules

```scala
case class Loan(item: Item, member: Member,
                days: Int = 28, renewals: Int = 0, express: Boolean = false)

Loan(ddd, ann)   // days = 28, renewals = 0, express = false
```

- The **usual** case needs no extra arguments: a standard loan is 28 days

---

# Named Arguments

```scala
Loan(ddd, ann, express = true)
Loan(member = ann, item = film, days = 7)
```

- Only state what **differs** from the default
- The order of named arguments does not matter
- Code reads like the ubiquitous language: *"a loan of the film to Ann for 7 days"*
- Case classes get `copy` with named arguments for free:

```scala
val renewed = loan.copy(renewals = loan.renewals + 1)
```

---

# Java: No Named Parameters

- Java has neither named nor default parameters
- Work-arounds:
  - **overloading**: many constructors `Loan(item, member)`, `Loan(item, member, days)`, ...
  - **builder pattern**:

```java
Loan loan = Loan.builder()
    .item(film).member(ann)
    .days(7).express(true)
    .build();
```

- Both need a lot of extra code – Scala gets it from the language

---

<!-- _class: kapitel -->

## 7
# Variable Number of Parameters

"A catalog contains items"

---

# Varargs: `T*`

- A catalog may contain any number of items – also none

```scala
class Catalog(name: String, items: Item*):
  def size: Int           = items.length
  def titles: Seq[String] = items.map(_.title)

Catalog("Main", ddd, film, mag).size   // 3
Catalog("Empty").size                   // 0
```

- `Item*` means: zero or more `Item`s
- Inside the class, `items` is a `Seq[Item]`
- Must be the **last** parameter

---

# Passing a Collection as Varargs

```scala
def totalFee(fees: Money*): Money =
  fees.foldLeft(Money(0))(_ + _)

totalFee(Money(150), Money(20), Money(5))   // Money(175)

val fees = List(Money(1), Money(2))
totalFee(fees*)                             // Money(3)
```

- `fees*` spreads a collection into the vararg slot
- You know this already: `List(1, 2, 3)`, `println(s"...")`, `Map(a -> b, ...)`
- Domain readings: *a catalog of items*, *the total of these fees*

---

# Varargs in Java

```java
static int count(Item... items) { return items.length; }

count(b, m);   // 2
count();       // 0
```

- `Item...` instead of `Item*`, inside it is an **array** `Item[]`
- An existing array can be passed directly
- Same rule: only the last parameter

---

# The Library Model at a Glance

| Domain concept | Building block | Language feature |
|---|---|---|
| ISBN, Money | Value object | `case class` |
| Member | Entity | class with id-based `equals` |
| Book, DVD, Magazine | Kinds of item | inheritance, `abstract class` |
| Reservable, Priced | Abilities | traits |
| Loan state | Closed set of cases | `sealed trait` / `enum` |
| Item / member store | Repository | generic types |
| Loan | Value with domain defaults | named & default parameters |
| Catalog, fees | Many of a kind | varargs |
| Loan desk | Aggregate root | encapsulation, `private` |

---

# A Session at the Loan Desk

```scala
val desk = LoanDesk()
desk.lend(ddd, ann)
// Right(Loan(Book,Member,28,0,false))
desk.lend(ddd, ann2)
// Left(Domain-Driven Design is already on loan)
desk.openLoans   // 1
```

- The rule *"lent only once"* is enforced in **one** place
- Errors are values (`Either`) – see Lecture 15
- Every name comes from the librarian's language

---

<!-- _class: inhalt -->

<style scoped>
section { font-size: 20px; }
</style>

# Summary

- DDD: put a **model of the domain** at the heart of the software
- **Ubiquitous language**: the same words for experts, team and code
- Building blocks: **value objects**, **entities**, **aggregates**, **repositories**, **bounded contexts**
- **Inheritance** for true is-a relationships; `sealed` for closed sets
- **Traits** for abilities that cut across the hierarchy
- **Generic types** for reusable abstractions like repositories
- **Named and default parameters** make calls read like the domain
- **Varargs** for "any number of" things
- Java: `extends`/`implements`, `<T>`, `record`, builders, `T...`

---

<!-- _class: aufgabe -->

# Task

(Task to fill)

---

<!-- _class: abschluss -->

# Questions?

## Thank you!

marko.boger@htwg-konstanz.de
