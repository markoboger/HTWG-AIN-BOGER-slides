---
marp: true
theme: htwg
paginate: true
_paginate: false
footer: "![](../../themes/htwgin40.png)&nbsp;&nbsp;Prof. Dr. Marko Boger"
_footer: ""
---

![bg](../../themes/htwgin-titel.png)
### Prof. Dr. Marko Boger
## Software Engineering
# Lecture 04: More Scala

Type system, collections, control structures, pattern matching and new Scala 3 types.

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 20px; }
.vs { display: grid; grid-template-columns: 170px 1fr; gap: 0.6rem 1rem; align-items: center; }
.vs .lbl { font-size: 26px; color: #575e75; }
.vs .sep { grid-column: 1 / 3; border-top: 3px dashed #b0b4bf; margin: 0.3rem 0; }
</style>

# A class ...

<div class="vs">
<div class="lbl">... in Java:</div>

```java
public class Person {
  public final String name;
  public final int age;
  Person(String name, int age) {
      this.name = name;
      this.age = age;
  }
}
```

<div class="sep"></div>
<div class="lbl">... in Scala:</div>

```scala
case class Person(name: String, age: Int)
```

</div>

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 19px; }
.vs { display: grid; grid-template-columns: 170px 1fr; gap: 0.6rem 1rem; align-items: center; }
.vs .lbl { font-size: 26px; color: #575e75; }
.vs .sep { grid-column: 1 / 3; border-top: 3px dashed #b0b4bf; margin: 0.3rem 0; }
</style>

# ... and its usage

<div class="vs">
<div class="lbl">... in Java:</div>

```java
import java.util.ArrayList;
...
Person[] people;
Person[] minors;
Person[] adults;
{  ArrayList<Person> minorsList = new ArrayList<Person>();
   ArrayList<Person> adultsList = new ArrayList<Person>();
   for (int i = 0; i < people.length; i++)
       (people[i].age < 18 ? minorsList : adultsList)
           .add(people[i]);
   minors = minorsList.toArray(people);
   adults = adultsList.toArray(people);
}
```

<div class="sep"></div>
<div class="lbl">... in Scala:</div>

```scala
val people = List(Person("Luke Skywalker",19))
val (minors, adults) = people partition (_.age < 18)
```

</div>

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 14px; line-height: 1.35; margin: 0.2rem 0; padding: 12px 14px; }
section { font-size: 22px; padding-left: 50px; padding-right: 50px; }
p { margin: 0.3rem 0; }
.cmp { display: grid; grid-template-columns: 450px 1fr; gap: 0 0.8rem; align-items: start; margin-top: 0.4rem; }
.cmp .lbl { font-size: 22px; color: #575e75; }
.note { font-size: 20px; margin-top: 0.6rem; }
.src { position: absolute; left: 50px; bottom: 82px; font-size: 14px; color: #888; }
</style>

# Another Example: Phone Mnemonics

Encode a phone number as words on a phone keypad, e.g. `7225276257` → "Scala rocks"

<div class="cmp">
<div class="lbl">... in Scala 3:</div>
<div class="lbl">... in Java 25:</div>
<div>

```scala
// all ways to encode a number as a list of words
def encode(number: String): Set[List[String]] =
  if number.isEmpty then Set(Nil)
  else
    (for
      split <- 1 to number.length
      word  <- wordsForNum(number.take(split))
      rest  <- encode(number.drop(split))
    yield word :: rest).toSet
```

</div>
<div>

```java
// all ways to encode a number as a list of words
Set<List<String>> encode(String number) {
  if (number.isEmpty()) return Set.of(List.of());
  return IntStream.rangeClosed(1, number.length()).boxed()
      .flatMap(split -> wordsForNum
          .getOrDefault(number.substring(0, split), List.of()).stream()
          .flatMap(word -> encode(number.substring(split)).stream()
              .map(rest -> Stream.concat(Stream.of(word), rest.stream()).toList())))
      .collect(toSet());
}
```

</div>
</div>

<div class="note">Full program: 21 lines Scala vs. 37 lines Java (Java 25 with streams)</div>

<div class="src">Martin Odersky, Scala at Work, JAOO 2010; task from L. Prechelt, IEEE Computer 2000</div>

---

<style scoped>
section { font-size: 22px; }
p { margin: 0.3rem 0; }
.kwgrid { display: grid; grid-template-columns: 1fr 2.3fr 1.25fr 1.15fr; gap: 0.7rem; align-items: stretch; margin-top: 0.6rem; }
.kwbox { background: #f6f8fa; border: 1px solid #d0d7de; border-radius: 8px; padding: 0.5rem 0.8rem 0.6rem 0.8rem; }
.kwh { font-weight: 700; font-size: 19px; color: #575e75; border-bottom: 1px solid #d0d7de; padding-bottom: 0.25rem; margin-bottom: 0.4rem; }
.kwl { font-family: var(--font-mono, ui-monospace, SFMono-Regular, Menlo, Consolas, monospace); font-size: 19px; line-height: 1.45; column-gap: 1rem; font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
.kwl span { display: block; break-inside: avoid; }
.core .kwl span { font-weight: 700; color: #000; }
.java .kwl span { color: #999; }
.kwl .soft { font-style: italic; }
.kwnote { font-size: 17px; color: #575e75; margin-top: 0.5rem; }
</style>

# Small Grammar

- The grammar of Scala 3 is very small in comparison to other languages. It fits on [8 pages in A4 format](http://dotty.epfl.ch/docs/reference/syntax.html).
- Here is a list of all keywords

<div class="kwgrid">
<div class="kwbox core"><div class="kwh">Core Scala</div><div class="kwl" style="columns: 1;"><span>case</span><span>def</span><span>enum</span><span class="soft">extension</span><span>given</span><span>match</span><span>object</span><span>sealed</span><span>trait</span><span class="soft">using</span><span>val</span><span>yield</span></div></div>
<div class="kwbox every"><div class="kwh">Everyday &amp; Advanced</div><div class="kwl" style="columns: 3;"><span>abstract</span><span class="soft">as</span><span>class</span><span class="soft">derives</span><span>do</span><span>else</span><span class="soft">end</span><span>export</span><span>extends</span><span>false</span><span>final</span><span>for</span><span>if</span><span>import</span><span class="soft">infix</span><span class="soft">inline</span><span>lazy</span><span>new</span><span class="soft">opaque</span><span class="soft">open</span><span>override</span><span>package</span><span>private</span><span>protected</span><span>super</span><span>then</span><span class="soft">transparent</span><span>true</span><span>type</span><span>with</span></div></div>
<div class="kwbox java"><div class="kwh">Java Compatibility (avoid)</div><div class="kwl" style="columns: 1;"><span>catch</span><span>finally</span><span>implicit</span><span>null</span><span>return</span><span>throw</span><span>try</span><span>var</span><span>while</span></div></div>
<div class="kwbox sym"><div class="kwh">Symbols</div><div class="kwl" style="columns: 2;"><span>#</span><span class="soft">*</span><span class="soft">+</span><span class="soft">-</span><span>:</span><span>&lt;-</span><span>&lt;:</span><span>=</span><span>=&gt;</span><span>=&gt;&gt;</span><span>&gt;:</span><span>?=&gt;</span><span>@</span><span class="soft">|</span></div></div>
</div>

<p class="kwnote"><i>italic</i> = soft keyword (a keyword only in certain positions, otherwise usable as a name)</p>

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 18px; line-height: 1.3; margin-top: 0.2rem; }
.nlbl { font-size: 22px; font-weight: 700; color: #575e75; margin-top: 0.6rem; }
</style>

# Significant Indentation

- In Scala 2, blocks of code are formed by braces, Java style

<div class="nlbl">Java-Style</div>

```scala
case class Person(name:String, birthdate:Date) extends Ordered[Person]{
 override def compare(that: Person) = this.age - that.age
 def age = birthdate.fullYearsSince
 def age(date:Date) = birthdate.fullYearsSince(date)
}
```

- Scala 3 also allows blocks by significant indentation, Python style

<div class="nlbl">Python-Style</div>

```scala
case class Person(name:String, birthdate:Date) extends Ordered[Person]:
 override def compare(that: Person) = this.age - that.age
 def age = birthdate.fullYearsSince
 def age(date:Date) = birthdate.fullYearsSince(date)
```

---

<style scoped>
section { font-size: 21px; }
li { margin: 0.1rem 0; }
.src { position: absolute; right: 70px; bottom: 78px; font-size: 14px; color: #888; }
</style>

# Scala Type Hierarchy

- `Any` is the top type, the supertype of all types (`equals`, `hashCode`, `toString`)
- `Matchable` (new in Scala 3): only values of a subtype of `Matchable` can be pattern matched
- `AnyVal`: value types (`Int`, `Boolean`, `Unit`, …), non-nullable; `AnyRef` (= `java.lang.Object`): all reference types
- `Null` is a subtype of all reference types, its only value is `null`; avoid it (Java interop only)
- `Nothing` is the bottom type, a subtype of all types; there is no value of type `Nothing`

<svg viewBox="0 0 1000 345" style="display: block; width: 860px; margin: 0.2rem auto 0 auto; font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;">
<defs><marker id="th-arr" viewBox="0 0 10 10" refX="10" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#555"/></marker></defs>
<line x1="500" y1="67" x2="500" y2="37" stroke="#555" stroke-width="1.5" marker-end="url(#th-arr)"/>
<line x1="294" y1="133" x2="440" y2="97" stroke="#555" stroke-width="1.5" marker-end="url(#th-arr)"/>
<line x1="674" y1="129" x2="556" y2="97" stroke="#555" stroke-width="1.5" marker-end="url(#th-arr)"/>
<line x1="90" y1="198" x2="206" y2="159" stroke="#555" stroke-width="1.5" marker-end="url(#th-arr)"/>
<line x1="184" y1="195" x2="231" y2="159" stroke="#555" stroke-width="1.5" marker-end="url(#th-arr)"/>
<line x1="265" y1="195" x2="255" y2="159" stroke="#555" stroke-width="1.5" marker-end="url(#th-arr)"/>
<line x1="374" y1="195" x2="286" y2="159" stroke="#555" stroke-width="1.5" marker-end="url(#th-arr)"/>
<line x1="622" y1="195" x2="698" y2="159" stroke="#555" stroke-width="1.5" marker-end="url(#th-arr)"/>
<line x1="711" y1="195" x2="724" y2="159" stroke="#555" stroke-width="1.5" marker-end="url(#th-arr)"/>
<line x1="846" y1="195" x2="764" y2="159" stroke="#555" stroke-width="1.5" marker-end="url(#th-arr)"/>
<line x1="696" y1="257" x2="624" y2="225" stroke="#555" stroke-width="1.5" marker-end="url(#th-arr)"/>
<line x1="724" y1="257" x2="711" y2="225" stroke="#555" stroke-width="1.5" marker-end="url(#th-arr)"/>
<line x1="765" y1="258" x2="844" y2="225" stroke="#555" stroke-width="1.5" marker-end="url(#th-arr)"/>
<line x1="371" y1="307" x2="90" y2="221" stroke="#555" stroke-width="1.5" marker-end="url(#th-arr)"/>
<line x1="386" y1="307" x2="199" y2="225" stroke="#555" stroke-width="1.5" marker-end="url(#th-arr)"/>
<line x1="400" y1="307" x2="290" y2="225" stroke="#555" stroke-width="1.5" marker-end="url(#th-arr)"/>
<line x1="419" y1="307" x2="411" y2="225" stroke="#555" stroke-width="1.5" marker-end="url(#th-arr)"/>
<line x1="470" y1="314" x2="695" y2="278" stroke="#555" stroke-width="1.5" marker-end="url(#th-arr)"/>
<rect x="465" y="7" width="70" height="30" rx="8" fill="#e0f3f1" stroke="#009b91" stroke-width="1.5"/>
<text x="500" y="28" text-anchor="middle" font-size="17" font-weight="700" fill="#222">Any</text>
<rect x="440" y="67" width="120" height="30" rx="8" fill="#e0f3f1" stroke="#009b91" stroke-width="1.5"/>
<text x="500" y="88" text-anchor="middle" font-size="17" font-weight="700" fill="#222">Matchable</text>
<rect x="206" y="129" width="89" height="30" rx="8" fill="#f6f8fa" stroke="#9aa4ae" stroke-width="1.5"/>
<text x="250" y="150" text-anchor="middle" font-size="17" font-weight="700" fill="#222">AnyVal</text>
<rect x="638" y="129" width="184" height="30" rx="8" fill="#f6f8fa" stroke="#9aa4ae" stroke-width="1.5"/>
<text x="730" y="150" text-anchor="middle" font-size="17" font-weight="700" fill="#222">AnyRef / Object</text>
<rect x="20" y="195" width="70" height="30" rx="8" fill="#f6f8fa" stroke="#9aa4ae" stroke-width="1.5"/>
<text x="55" y="216" text-anchor="middle" font-size="17" font-weight="400" fill="#222">Unit</text>
<rect x="115" y="195" width="100" height="30" rx="8" fill="#f6f8fa" stroke="#9aa4ae" stroke-width="1.5"/>
<text x="165" y="216" text-anchor="middle" font-size="17" font-weight="400" fill="#222">Boolean</text>
<rect x="235" y="195" width="70" height="30" rx="8" fill="#f6f8fa" stroke="#9aa4ae" stroke-width="1.5"/>
<text x="270" y="216" text-anchor="middle" font-size="17" font-weight="400" fill="#222">Int</text>
<rect x="318" y="195" width="184" height="30" rx="8" fill="#f6f8fa" stroke="#9aa4ae" stroke-width="1.5"/>
<text x="410" y="216" text-anchor="middle" font-size="17" font-weight="400" fill="#222">… (value types)</text>
<rect x="546" y="195" width="89" height="30" rx="8" fill="#f6f8fa" stroke="#9aa4ae" stroke-width="1.5"/>
<text x="590" y="216" text-anchor="middle" font-size="17" font-weight="400" fill="#222">String</text>
<rect x="645" y="195" width="120" height="30" rx="8" fill="#f6f8fa" stroke="#9aa4ae" stroke-width="1.5"/>
<text x="705" y="216" text-anchor="middle" font-size="17" font-weight="400" fill="#222">List[Int]</text>
<rect x="767" y="195" width="226" height="30" rx="8" fill="#f6f8fa" stroke="#9aa4ae" stroke-width="1.5"/>
<text x="880" y="216" text-anchor="middle" font-size="17" font-weight="400" fill="#222">… (reference types)</text>
<rect x="695" y="257" width="70" height="30" rx="8" fill="#e0f3f1" stroke="#009b91" stroke-width="1.5"/>
<text x="730" y="278" text-anchor="middle" font-size="17" font-weight="700" fill="#222">Null</text>
<rect x="370" y="307" width="100" height="30" rx="8" fill="#e0f3f1" stroke="#009b91" stroke-width="1.5"/>
<text x="420" y="328" text-anchor="middle" font-size="17" font-weight="700" fill="#222">Nothing</text>
</svg>

<div class="src">Source: Scala 3 Book, "A First Look at Types", docs.scala-lang.org/scala3/book/first-look-at-types.html</div>

---

<style scoped>
section { font-size: 21px; }
.numtypes { display: grid; grid-template-columns: 1fr 1fr; gap: 0 2rem; margin-top: 1.2rem; }
.numtypes ul { margin: 0; }
.numtypes li { margin: 0.15rem 0; }
</style>

# Type Casting for Value Types

- Value types can easily be converted into a suitable more complex value type.

<img src="assets/se04-value-type-conversion.png" alt="Conversion chain of value types: Byte to Short to Int to Long to Float to Double, and Char to Int" style="display: block; width: 800px; margin: 2rem auto 0 auto;">

<div class="numtypes">
<div>

- `Byte`: 8-bit signed integer, −128 to 127
- `Short`: 16-bit signed integer, −32,768 to 32,767
- `Int`: 32-bit signed integer, −2³¹ to 2³¹−1 (default for integer literals)

</div>
<div>

- `Long`: 64-bit signed integer, −2⁶³ to 2⁶³−1 (suffix `L`)
- `Float`: 32-bit IEEE 754 single-precision floating point (suffix `F`)
- `Double`: 64-bit IEEE 754 double-precision floating point (default for decimal literals)

</div>
</div>

---

# The Type Unit

- Similar to void in Java
- But Java-void is not a type, it is a keyword
- In Scala Unit is a type
  - So we can do type checking on it
  - It is a subtype of AnyVal
- It has only a single instance value
  - `()`
- Try to avoid Unit, try to always return a result from a function

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 19px; }
section { font-size: 22px; }
li { margin: 0.1rem 0; }
.src { position: absolute; left: 70px; bottom: 82px; font-size: 14px; color: #888; }
</style>

# The Type Nothing

- `Nothing` is the bottom type: a subtype of every type, and there is no value of type `Nothing`
- Expressions of type `Nothing` never return normally: `throw`, `sys.exit()`, `???`
- So they fit wherever any type is expected:

```scala
def fail(msg: String): Nothing = throw IllegalArgumentException(msg)

def age(s: String): Int     = if s.nonEmpty then s.toInt else fail("no age")
def name(s: String): String = if s.nonEmpty then s.trim  else fail("no name")

def parse(s: String): Person = ???   // placeholder: compiles for any type
```

- `if … then Int else Nothing` has type `Int`; the same `fail` works for `String`, `Person`, …

<div class="src">Sources: Scala 3 Book, "A First Look at Types"; scala.Nothing API docs; Rock the JVM, "Much Ado About Nothing in Scala"</div>

---

# The Type Null

- In Java null is a value that is allowed for many Types
  - It can be checked for its value, but not for its type
- Null in Scala is a Type
  - Null is a subtype of any Reference Type
    - It is type compatible with any Reference Type
  - null is an instance of Null
    - Value Types can not contain null, only Reference Types can
- Null should be avoided, instead the type Option should be used
  - it is only present for compatibility reasons

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 17px; line-height: 1.3; margin: 0.2rem 0 0.3rem 0; }
section { font-size: 21px; }
li { margin: 0.1rem 0; }
.cmp { display: grid; grid-template-columns: 1fr 1.25fr; gap: 0 1rem; align-items: start; }
.src { position: absolute; left: 70px; bottom: 82px; font-size: 14px; color: #888; }
</style>

# The Type Option

- In Java, "no value" is often `null`: every caller has to remember a null check, otherwise `NullPointerException`
- In Scala, a result that may be missing has the type `Option[A]`: either `Some(value)` or `None`

<div class="cmp">
<div>

```scala
def makeInt(s: String): Option[Int] =
  try
    Some(Integer.parseInt(s.trim))
  catch
    case e: Exception => None

val a = makeInt("1")     // Some(1)
val b = makeInt("one")   // None
```

</div>
<div>

```scala
makeInt(x) match
  case Some(i) => println(i)
  case None    => println("That didn’t work.")

makeInt("42").map(_ * 2)      // Some(84)
makeInt("one").getOrElse(0)   // 0
for a <- makeInt("1"); b <- makeInt("2")
yield a + b                   // Some(3)
```

</div>
</div>

- The type makes absence explicit: the compiler forces you to handle `None`, no null checks needed
- The standard library already offers this, e.g. `"42".toIntOption` or `map.get(key)`

<div class="src">Example: Scala 3 Book, "Functional Error Handling" (docs.scala-lang.org/scala3/book/fp-functional-error-handling.html)</div>

---

<style scoped>
section { font-size: 22px; }
</style>

# Extending the Type System

- Java has inheritance from one class and realization from several interfaces
  - A class can extend only one (abstract) class
  - Interfaces can have default methods (since Java 8), but no instance state
    - Default methods allow rich interfaces, but without state they stay limited
- Scala has
  - Inheritance from at most one class, plus any number of traits
  - Mix-in of several traits using `with` or, since Scala 3, commas (`extends A, B, C`)
  - Traits can have attributes and method implementations
    - Rich Traits are very convenient, they provide a lot
  - Since Scala 3, traits can also have parameters
- This brings Scala very close to multiple inheritance: behavior and state, without the diamond problem (resolved by linearization)

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 15px; line-height: 1.4; margin: 0.2rem 0; padding: 12px 14px; }
section { font-size: 22px; padding-left: 50px; padding-right: 50px; }
.cmp { display: grid; grid-template-columns: 495px 1fr; gap: 0 0.8rem; align-items: start; margin-top: 0.6rem; }
.src { position: absolute; left: 50px; bottom: 82px; font-size: 14px; color: #888; }
</style>

# Traits - a Simple Example

- A trait defines behavior: abstract methods (`speak`) and concrete methods (`startTail`, …)
- A class mixes in several traits (`extends A, B, C`) and implements or overrides their methods

<div class="cmp">
<div>

```scala
trait Speaker:
  def speak(): String  // has no body, so it’s abstract

trait TailWagger:
  def startTail(): Unit = println("tail is wagging")
  def stopTail(): Unit = println("tail is stopped")

trait Runner:
  def startRunning(): Unit = println("I’m running")
  def stopRunning(): Unit = println("Stopped running")
```

</div>
<div>

```scala
class Dog(name: String) extends Speaker, TailWagger, Runner:
  def speak(): String = "Woof!"

class Cat(name: String) extends Speaker, TailWagger, Runner:
  def speak(): String = "Meow"
  override def startRunning(): Unit = println("Yeah ... I don’t run")
  override def stopRunning(): Unit = println("No need to stop")

val d = Dog("Rover")
println(d.speak())   // Woof!
d.startTail()        // tail is wagging
val c = Cat("Morris")
c.startRunning()     // Yeah ... I don’t run
```

</div>
</div>

<div class="src">Example: Scala 3 Book, "Domain Modeling" in "A Taste of Scala" (docs.scala-lang.org/scala3/book/taste-modeling.html)</div>

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 21px; line-height: 1.35; }
</style>

# Traits - an Example

```scala
trait Ordered[A] {
  def compare(that: A): Int   // abstract method
  def <  (that: A): Boolean = (this compare that) <  0
  def >  (that: A): Boolean = (this compare that) >  0
}
class Health(val value : Int) extends Ordered[Health]
{
  override def compare(other : Health) = {
    this.value - other.value }
  def isCritical() = …
}
```

---

# Collection Abstractions

<div class="columns" style="grid-template-columns: 1fr 1fr;">
<div>

- Scala has a very nice collection library. At its core are some very clean abstractions of different types of collections. They very nicely unify the API.
- These abstractions are available both as immutable and mutable implementations.
- Unless you have a very strong reason, use the immutable one.

</div>
<img src="assets/se04-collection-abstractions.png" alt="Collection abstractions: Iterable with Seq, Set and Map; IndexedSeq, LinearSeq, SortedSet, BitSet, SortedMap" style="height: 380px;">
</div>

---

# Immutable Collections

<img src="assets/se04-collections-legend.png" alt="Legend: trait to class via implicit conversion, default implementation, implemented by" style="position: absolute; top: 30px; right: 40px; height: 120px;">

<img src="assets/se04-immutable-collections.png" alt="Hierarchy of the immutable collections in scala.collection.immutable" style="display: block; width: 1020px; margin: 1.2rem auto 0 auto;">

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 20px; line-height: 1.3; margin: 0.2rem 0 0.4rem 0; }
p { margin: 0.3rem 0; }
</style>

# Creation of Collections

Creation of collections is uniform and simple. Here are examples:

```scala
Iterable("x", "y", "z")
Map("x" -> 24, "y" -> 25, "z" -> 26)
Set(Color.red, Color.green, Color.blue)
SortedSet("hello", "world")
Buffer(x, y, z)
IndexedSeq(1.0, 2.0)
LinearSeq(a, b, c)
```

Often you will use the default types:

```scala
List(1, 2, 3)
Vector(1, 2, 3)
Map("x" -> 24, "y" -> 25, "z" -> 26)
```

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 16px; line-height: 1.25; margin: 0.15rem 0 0.4rem 0; padding: 10px 14px; }
section { font-size: 21px; padding-left: 50px; padding-right: 50px; }
li { margin: 0.05rem 0; }
.cmp { display: grid; grid-template-columns: 1fr 1.12fr; gap: 0 1rem; align-items: start; margin-top: 0.4rem; }
.lbl { font-size: 18px; font-weight: 700; color: #575e75; }
.src { position: absolute; right: 50px; bottom: 82px; font-size: 14px; color: #888; }
</style>

# Iterators

- An `Iterator` delivers elements one at a time: `next()` returns the next one, `hasNext` tells if there are more
- Unlike a collection, an iterator can be traversed **only once**

<div class="cmp">
<div>
<div class="lbl">Step by step</div>

```scala
scala> val it = List(1, 2, 3, 4, 5).iterator
val it: Iterator[Int] = non-empty iterator
scala> it.next()
val res0: Int = 1
scala> it.next()
val res1: Int = 2
scala> it.next()
val res2: Int = 3
scala> it.hasNext
val res3: Boolean = true
scala> it.next()
val res4: Int = 4
scala> it.next()
val res5: Int = 5
scala> it.hasNext
val res6: Boolean = false
scala> it.toList
val res7: List[Int] = List()
```

</div>
<div>
<div class="lbl">Used up after one pass</div>

```scala
scala> val words = List("one", "two", "three").iterator
val words: Iterator[String] = non-empty iterator
scala> words.map(_.length).toList
val res8: List[Int] = List(3, 3, 5)
scala> words.map(_.length).toList
val res9: List[Int] = List()
```

</div>
</div>

<div class="src">Scala 3.9.0 REPL output · docs.scala-lang.org: Collections › Iterators</div>

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 16px; line-height: 1.25; margin: 0.15rem 0 0.4rem 0; padding: 10px 14px; }
section { font-size: 21px; padding-left: 50px; padding-right: 50px; }
li { margin: 0.05rem 0; }
.cmp { display: grid; grid-template-columns: 1.15fr 1fr; gap: 0 1rem; align-items: start; margin-top: 0.4rem; }
.lbl { font-size: 18px; font-weight: 700; color: #575e75; }
.src { position: absolute; right: 50px; bottom: 82px; font-size: 14px; color: #888; }
</style>

# Iterators: grouped and sliding

- Many methods return an iterator: `Source.fromFile("data.txt").getLines()`, `"Hello".iterator`, …
- `xs.grouped(n)`: chunks of `n` elements, the last chunk may be shorter
- `xs.sliding(n)`: a window of `n` elements that moves one step at a time

<div class="cmp">
<div>
<div class="lbl">grouped(3)</div>

```scala
scala> val xs = List(1, 2, 3, 4, 5, 6, 7)
val xs: List[Int] = List(1, 2, 3, 4, 5, 6, 7)
scala> val g = xs.grouped(3)
val g: Iterator[List[Int]] = non-empty iterator
scala> g.next()
val res0: List[Int] = List(1, 2, 3)
scala> g.next()
val res1: List[Int] = List(4, 5, 6)
scala> g.next()
val res2: List[Int] = List(7)
scala> g.hasNext
val res3: Boolean = false
```

</div>
<div>
<div class="lbl">sliding(2)</div>

```scala
scala> xs.sliding(2).toList
val res4: List[List[Int]] = List(
  List(1, 2),
  List(2, 3),
  List(3, 4),
  List(4, 5),
  List(5, 6),
  List(6, 7)
)
```

</div>
</div>

<div class="src">Scala 3.9.0 REPL output · docs.scala-lang.org: Collections › Iterators</div>

---

<style scoped>
table { font-size: 18px; margin: 0.4rem auto 0 auto; border-collapse: collapse; }
th, td { padding: 3px 14px; line-height: 1.3; }
td:first-child { white-space: nowrap; }
td code { font-size: 17px; font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
</style>

# API of Set

- A Set is a Traversable and an Iterator, and has specific operations for sets

| Operation | Description |
|---|---|
| `xs contains x`, `xs(x)` | Test whether `x` is an element of `xs`. |
| `xs + x` | The set containing all elements of `xs` as well as `x`. |
| `xs + (x, y, z)` | The set containing all elements of `xs` as well as with the given additional elements. |
| `xs ++ ys` | The set containing all elements of `xs` as well as all elements of `ys`. |
| `xs - x` | The set containing all elements of `xs` except for `x`. |
| `xs - (x, y, z)` | The set containing all elements of `xs` except for the given elements. |
| `xs -- ys` | The set containing all elements of `xs` except for the elements of `ys`. |
| `xs & ys`, `xs intersect ys` | The set intersection of `xs` and `ys`. |
| `xs \| ys`, `xs union ys` | The set union of `xs` and `ys`. |
| `xs &~ ys`, `xs diff ys` | The set difference of `xs` and `ys`. |
| `xs subsetOf ys` | Test whether `xs` is a subset of `ys`. |
| `xs.empty` | An empty set of the same class as `xs`. |

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 20px; line-height: 1.3; margin: 0.2rem 0 0.4rem 0; }
</style>

# Lists

- Lists are heavily used in Scala, like in all functional programming languages
- Simple lists

```scala
List('a', 'b', 'c')
List( 1, 2, 3, 4)
List("apples", "oranges", "pears")
List(List(1,0), List(0,1))
List()
```

- The elements all have the same (super-) Type

```scala
List[Char], List[Int], List[String], List[List[Int]]
val fruit: List[String] = List("apples", "oranges")
```

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 19px; margin: 0.1rem 0 0.3rem 0; }
section { font-size: 22px; }
li { margin: 0.1rem 0; }
</style>

# List concatenator

<div class="columns" style="align-items: start;">
<div>

- Empty List

```scala
Nil
```

- Element Concatenator `::`

```scala
val nums = 1 :: (2 :: (3 :: (4 :: Nil)))
```

- Concatenation works from right to left

```scala
val nums = 1 :: 2 :: 3 :: 4 :: Nil
```

</div>
<div>

- Basic Operations

```scala
head
tail
isEmpty
```

- List Concatenator `:::`

```scala
List(1,2,3):::List(4,5,6)
```

</div>
</div>

---

<style scoped>
.blocks { display: grid; grid-template-columns: auto auto auto; gap: 0.4rem 2rem; align-items: start; justify-content: end; margin-top: -0.5rem; }
.blocks div { text-align: center; font-weight: bold; color: #0b3c68; }
.blocks img { display: block; margin: 0.5rem auto 0 auto; }
</style>

# The fundamental building blocks of programming languages

<div class="columns" style="grid-template-columns: 0.9fr 1.1fr; align-items: start;">
<div>

- Most programming languages consist of these fundamental building blocks
  - Assignment
  - Conditionals
  - Iterations
- We already saw them im Scratch.

</div>
<div class="blocks">
<div>Assignment<img src="assets/se04-scratch-set-change.png" alt="Scratch blocks: set and change a variable" style="width: 230px;"></div>
<div>Conditionals<img src="assets/se04-scratch-if.png" alt="Scratch blocks: if then and if then else" style="width: 120px;"></div>
<div>Iterations<img src="assets/se04-scratch-repeat-forever.png" alt="Scratch blocks: repeat 10 and forever" style="width: 115px;"><img src="assets/se04-scratch-repeat-until.png" alt="Scratch block: repeat until" style="width: 115px;"></div>
</div>
</div>

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 21px; }
</style>

# Assignment

- An assignment stores a data value into a variable, usually written with the equals sign (=)

```scala
var x = 42
x = 21
var anakin: String = "Anakin Skywalker"
anakin = "Darth Vader"
var theForceIsStrong = true
```

- This differs from Math, were = denotes an equality relationship, not assignment.

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 21px; margin: 0.2rem 0 0.4rem 0; }
.cmp { display: grid; grid-template-columns: 340px 1fr; gap: 0 1rem; align-items: start; }
.cmp pre.repl, .cmp .repl pre { font-size: 15.5px; line-height: 1.3; }
.lbl { font-size: 18px; font-weight: 700; color: #575e75; }
ul.eq { font-size: 21px; margin-top: 0.3rem; }
</style>

# Equality

- In programming, the equality is usually written with two equal signs (==) and is a boolean condition.

<div class="cmp">
<div>
<div class="lbl">Conditions</div>

```scala
x==21
x==42
anakin=="Anakin Skywalker"
anakin=="Darth Vader"
theForceIsStrong==true
theForceIsStrong==false
```

</div>
<div class="repl">
<div class="lbl">Equality in an if (Scala 3.9.0 REPL)</div>

```scala
scala> var anakin = "Darth Vader"
var anakin: String = "Darth Vader"
scala> if anakin == "Darth Vader" then println("Welcome to the dark side!")
Welcome to the dark side!
scala> if anakin = "Darth Vader" then println("Welcome to the dark side!")
-- [E007] Type Mismatch Error: -------------------------------------------------
1 |if anakin = "Darth Vader" then println("Welcome to the dark side!")
  |   ^^^^^^^^^^^^^^^^^^^^^^
  |   Found:    Unit
  |   Required: Boolean
scala> val sith = "Darth " + "Vader"
val sith: String = "Darth Vader"
scala> sith == anakin
val res1: Boolean = true
```

</div>
</div>

<ul class="eq">
<li>An assignment <code>=</code> has type <code>Unit</code>, so it is no condition (in C, <code>if (x = 5)</code> is a classic bug)</li>
<li><code>==</code> compares values (it calls <code>equals</code>): equal Strings are <code>==</code>, even as different objects</li>
</ul>

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 19px; margin: 0.2rem 0 0.4rem 0; }
section { font-size: 22px; }
.nlbl { font-size: 22px; font-weight: 700; color: #575e75; }
</style>

# Types in Assignment

<div class="columns" style="grid-template-columns: 1.3fr 0.7fr; align-items: start;">
<div>

- Data values have a type, like Int or String.
- In statically typed languages, the variable that should store this data value must match its type.
- In some programming languages, like Java, this type needs to be declared before assignment.

```scala
var padme: String = "Padme Amidala"
var age: Int = 26
```

- In Scala, this type is often inferred by the compiler
- and can be omitted

```scala
var padme = "Padme Amidala"
var age = 26
```

</div>
<div style="margin-top: 4rem;">
<div class="nlbl">Java</div>

```java
String padme = "Padme Amidala";
int age = 26;
```

</div>
</div>

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 20px; margin: 0.2rem 0 0.4rem 0; }
</style>

# Values and Variables

- Variables can be assigned a new value

```scala
var anakin: String = "Anakin Skywalker"
anakin = "Darth Vader"
```

- But variables can be declared as non-reassignable or constant. In Scala, these are called values

```scala
val pi = 3.14159
val luke = "Luke Skywalker"
```

- In functional programming, the re-assignment is avoided. It is regarded as a side-effect and makes code difficult to test and reason about.

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 18px; line-height: 1.25; margin: 0.2rem 0 0.3rem 0; }
section { font-size: 21px; }
li { margin: 0.1rem 0; }
</style>

# Scope

- The declaration of a variable is only visible within the block of code it is defined in. This is called the scope of a variable.
- A block of code is usually defined by brackets { … }

```scala
{
   val anakin = "Anakin Skywalker"
}
{
   val anakin = "Darth Vader"
}
```

- Variables on the top-most block are visible everywhere, this is called global scope.

```scala
val pi = 3.14159
```

- We should usually be very careful with global scope. It can interfere with other code, like libraries.

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 20px; }
</style>

# Shadowing

- Blocks of Code can be nested inside each other. Accordingly variables can be declared at different depth of the scope.
- If a variable of same name and type is declared on an inner nested scope, this is called Shadowing.

```scala
{
   val anakin = "Anakin Skywalker"
   {
       val anakin = "Darth Vader"
       println (anakin)
   }
   println (anakin)
}
```

- This can lead to difficult to find bugs and should generally be avoided.

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 18px; margin: 0.2rem 0 0.4rem 0; }
section { font-size: 21px; }
</style>

# Statements and Expressions

- **Statement:** A statement is a complete unit of code that performs an action but does not produce a value. It’s like a command that the program executes, often causing side effects (e.g., printing to the console, modifying a variable). Statements are typically executed for their effect rather than their result.

```scala
val meaningOfLife = 42; println(meaningOfLife)
```

- **Expression:** An expression is a piece of code that evaluates to a value. It can be used wherever a value is expected (e.g., in assignments, function arguments). Expressions may or may not cause side effects, but their primary purpose is to produce a result.

```scala
17+4
sin(x) * log(1 + x * x) + exp(x / pi)
theForceIsStrong==true
```

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 19px; margin: 0.2rem 0 0.4rem 0; }
section { font-size: 22px; }
li { margin: 0.1rem 0; }
</style>

# Statements and Expressions

- Expressions can be combined with Expressions or Statements. An Expression evaluates to a value, this can be compiled with another value, assigned to a variable, passed to a function or printed

```scala
val blackjack = 17+4
println(sin(x) * log(1 + x * x) + exp(x / pi))
```

- Note that Statements do not combine with Expressions or other Statements.
- Statements are only combined in sequence.
- In many languages, the sequence of Statements is separated by a semicolon (;)

```scala
val meaningOfLife = 42; println(meaningOfLife)
```

- In Scala, this is only necessary if used on the same line.

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 22px; }
</style>

# If Conditional

<div class="columns" style="grid-template-columns: 1.4fr 0.6fr; align-items: start;">
<div>

- If is a fundamental control structure and found in all programming languages.
- In Scala, its basic form is

```scala
if boolean_expression then statement
```

</div>
<img src="assets/se04-scratch-if-then.png" alt="Scratch block: if then" style="width: 150px;">
</div>

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 21px; margin: 0.2rem 0 0.4rem 0; }
</style>

# Syntax Alternatives

- Scala offers syntax alternatives.
- A style close to C or Java is

```scala
if (boolean_expression) { statement }
```

- The more modern version close to pseudo notations is

```scala
if boolean_expression then statement
```

- And you can mix these as you like.

```scala
if (boolean_expression) then { statement }
if (boolean_expression) then statement
```

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 20px; margin: 0.2rem 0 0.4rem 0; }
</style>

# if then else

<div class="columns" style="grid-template-columns: 1.6fr 0.4fr; align-items: start;">
<div>

- The if expression also has an else in Scala

```scala
if (boolean_expression) { statement } else { statement }
if boolean_expression then statement else statement
```

- This is often formatted over several lines

```scala
if boolean_expression
then statement
else statement
```

</div>
<img src="assets/se04-scratch-if-else.png" alt="Scratch block: if then else" style="width: 150px;">
</div>

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 20px; margin: 0.2rem 0 0.4rem 0; }
</style>

# If as expression

- In Scala, the if can also be used as an expression

```scala
if (boolean_expression) { expression } else { expression }
if boolean_expression then expression else expression
```

- The importance of this is that expressions can be composed

```scala
val result = if (boolean_expression)
then expression
else expression
(if boolean_expression then expression else expression)
  + (if boolean_expression then expression else expression)
```

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 20px; margin: 0.2rem 0 0.4rem 0; }
</style>

# If Conditional

- Here is a more practical example. First as a Statement

```scala
if (points  > 21) println("Busted!")
else if (points == 21) println("Blackjack!")
else println("Points: " + points)
```

- And as an expression.

```scala
val result = if (points  > 21) "Busted!"
else if (points == 21) "Blackjack!"
else "Points: " + points
println(result)
```

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 21px; }
</style>

# if without Parentheses

- Here is another example, here without parentheses

```scala
// if without parentheses as statement
if age >= 18
then println("Adult")
else println("Minor")
// if without parentheses as expression
val ageGroup = if age >= 18 then "Adult" else "Minor"
println(ageGroup)
```

---

# The Type of an if expression

- The if expression’s return type is the least upper bound of the types of the then and else branches.
- That is, the next common super type of the then branch and the else branch.
- The least upper bound of Int and Boolean is AnyVal.
- The least upper bound of Double and String is Matchable.
- So, in general it is advisable to always use an else branch when if is used as expression. And the type of the then and else branch should match.

---

<!-- _footer: "" -->

![bg contain](assets/se04-type-hierarchy-scala3.png)

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 14px; line-height: 1.25; margin: 0; padding: 8px 12px; }
section { font-size: 22px; }
.nlbl { font-size: 18px; font-weight: 700; color: #575e75; margin: 0.45rem 0 0.1rem 0; }
.nlbl.first { margin-top: 0; }
.code3 { display: grid; grid-template-columns: 1fr 1fr; gap: 0.6rem 1rem; }
</style>

# If in Functional Programming

<div class="columns" style="grid-template-columns: 1fr 1fr; align-items: start; gap: 1.2rem;">
<div>

- Most programming languages only offer if as a statement. Java has only the conditional operator `?:` as an expression, and it is rarely used.
- In the functional programming style, the expression is preferred.
- In general Scala is an expression-oriented language, Java is statement-oriented.

<div class="nlbl">Scala</div>

```scala
val points = 22
val result =
  if points > 21 then "Busted!"
  else if points == 21 then "Blackjack!"
  else s"Points: $points"
println(result)
```

</div>
<div>
<div class="nlbl first">C</div>

```c
if (points > 21) {
    printf("Busted!\n");
} else if (points == 21) {
    printf("Blackjack!\n");
} else {
    printf("Points: %d\n", points);
}
```

<div class="nlbl">Java</div>

```java
int points = 22;
if (points > 21) {
    System.out.println("Busted!");
} else if (points == 21) {
    System.out.println("Blackjack!");
} else {
    System.out.println("Points: " + points);
}
```

<div class="nlbl">Java (conditional operator ?:)</div>

```java
String result = points > 21 ? "Busted!" :
       points == 21 ? "Blackjack!" :
       "Points: " + points;
```

</div>
</div>

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 20px; margin: 0.2rem 0 0.4rem 0; }
section { font-size: 22px; }
li { margin: 0.1rem 0; }
</style>

# for loop

<div class="columns" style="grid-template-columns: 1.6fr 0.4fr; align-items: start;">
<div>

- Another fundamental control structure in all programming languages is the for loop.

```scala
for (i <- 0 until 10) println(i)
for (i <- 1 to 10) println(i)
```

- Note: read the <- arrow as “take i from the Range 1 to 10”
- For loops are often used to access the index of an Array.

```scala
val array = Array(1, 2, 3, 4, 5)
for (i <- 0 until array.length) println(array(i))
```

- Here, the for loop is used as a statement.

</div>
<img src="assets/se04-scratch-repeat.png" alt="Scratch block: repeat 10" style="width: 150px;">
</div>

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 18px; margin: 0.2rem 0 0.4rem 0; }
section { font-size: 22px; }
li { margin: 0.1rem 0; }
</style>

# More Features of for

- The for loop has a few more tricks up its sleeve.
- The general form is

```scala
for (generator) statement
```

- The generator can have a step size

```scala
for (i <- 0 until array.length by 2) println(array(i))
```

- The generator can also have a condition

```scala
for (i <- 0 until array.length if array(i) % 2 == 0)
    println(array(i))
```

- Or both

```scala
for (i <- 0 until array.length by 3 if array(i) % 2 == 0) println(array(i))
```

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 20px; margin: 0.2rem 0 0.4rem 0; }
section { font-size: 22px; }
</style>

# For as an Expression

- The for loop can also be used as an Expression. For this to work, every iteration has to return a single result. This is expressed with the keyword yield.
- The general form is

```scala
for (generator) yield expression
```

- The return type of the for loop now is a collection. The type of the collection depends on the collection used in the generator. If the generator does not have a suitable collection, the type is IndexedSeq or more specifically a Vector.

```scala
var vector: IndexedSeq[Int] = Vector()
vector = for (i <- 0 until array.length) yield i
```

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 19px; line-height: 1.3; }
</style>

# Step by and Condition

- Also as expression, step by and conditions can be used.

```scala
// for loop as an expression, using yield with a step
vector = for (i <- 0 until array.length by 2)
    yield i
// for loop using yield with a condition
vector = for (i <- 0 until array.length if array(i) % 2 == 0)
    yield i
// for loop using yield with a step and a condition
vector = for (i <- 0 until array.length by 3
    if array(i) % 2 == 0)
    yield i
```

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 19px; margin: 0.2rem 0 0.4rem 0; }
section { font-size: 22px; }
</style>

# For over a List

- In Scala, the Array is generally avoided. Instead the List is preferred. This becomes evident in the context of the for loop.
- Instead of iterating over an index, we directly iterate over the List.

```scala
val list: List[Int] = List(1, 2, 3, 4, 5)
val result3 : List[Int] = for (elem <- list) yield elem
val result4 : List[Int] =
   for (elem <- list if elem % 2 == 0) yield elem
```

- In this case, the resulting collection is a List, because we started with a List. But the compiler knows this, we can leave that out.

```scala
val result4 =
   for (elem <- list if elem % 2 == 0) yield elem
```

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 20px; margin: 0.2rem 0 0.4rem 0; }
section { font-size: 22px; }
</style>

# For over an Array

- Scala can also directly iterate over an Array, without explicitly using the index.

```scala
val array = Array(1, 2, 3, 4, 5)
val result5 : Array[Int] = for (elem <- array) yield elem
```

- In this case the result type is an Array. We can again leave out the type.

```scala
val result5 = for (elem <- array) yield elem
```

- Because we do not need an index anymore, but directly iterate over the elements of the collection, in Scala the List is preferred over the Array. Reading sequentially is exactly what it is built for.

---

<style scoped>
section { font-size: 22px; }
</style>

# Summary: Assignment, if and for

- Assignment, if conditions and for loops are fundamental building blocks of programming languages.
- **var allows re-assignment, val does not. val is preferred in FP.**
- **if can be used as a statement or an expression. In FP expressions are preferred.**
- **Also for can be used as a statement or an expression.**
- for can loop over a Range of the index of an Array.
- **A Range has to and until, as well as by operators.**
- **In Scala, for can also directly iterate over an Array or a List.**
- **It is often used as expression using yield.**
- Then the return type is the same as used in the generator.

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 21px; }
</style>

# foreach

- All collections have the function foreach. It serves much like a for loop and is very common.

```scala
scala> val v = Vector((1, 9), (2, 8), (3, 7), (4, 6), (5, 5))
val v: Vector[(Int, Int)] = Vector((1, 9), (2, 8), (3, 7), (4, 6), (5, 5))
scala> v.foreach((i, j) => println(s"$i, $j"))
1, 9
2, 8
3, 7
4, 6
5, 5
```

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 18px; line-height: 1.3; margin: 0.2rem 0 0.3rem 0; }
section { font-size: 22px; }
li { margin: 0.1rem 0; }
</style>

# map

- A typical way to express loops in FP is using map
- Map
  - Maps each element of a list to a new element of a list according to some function

```scala
scala> val n = (1 to 3).toList
val n: List[Int] = List(1, 2, 3)
scala> n.map(i => i * 3)
val res0: List[Int] = List(3, 6, 9)
scala> n.map(i => n.map(j => i * j))
val res1: List[List[Int]] = List(List(1, 2, 3), List(2, 4, 6), List(3, 6, 9))
```

- Flatmap
  - Produces a not-nested list (flat)

```scala
scala> n.flatMap(i => n.map(j => i * j))
val res2: List[Int] = List(1, 2, 3, 2, 4, 6, 3, 6, 9)
```

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 19px; line-height: 1.3; margin: 0.2rem 0 0.4rem 0; }
</style>

# match

<div class="columns" style="align-items: start;">
<div>

- Match is similar to switch but more general

```scala
def describe(x: Int) = x match
  case 1 => "one"
  case 2 => "two"
  case _ => "many"
```

</div>
<div>

- Variable renaming and guards

```scala
def describe(x: Int) = x match
  case n if n < 0  => s"$n is negative"
  case z if z == 0 => s"$z is zero"
  case p if p > 0  => s"$p is positive"
```

</div>
</div>

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 16px; line-height: 1.3; margin: 0.15rem 0 0.4rem 0; padding: 10px 14px; }
section { font-size: 21px; padding-left: 50px; padding-right: 50px; }
li { margin: 0.05rem 0; }
.cmp { display: grid; grid-template-columns: 1fr 1fr; gap: 0 1rem; align-items: start; margin-top: 0.4rem; }
.lbl { font-size: 18px; font-weight: 700; color: #575e75; }
.src { position: absolute; left: 50px; bottom: 82px; font-size: 14px; color: #888; }
</style>

# match on Types

- A type pattern `case s: String` tests the type **and** binds a typed variable: inside the case, `s` already is a `String`, no cast needed (unlike Java's `instanceof` + cast)
- `Matchable` is the root of all types that can be matched; with a union type, the compiler checks that all cases are covered

<div class="cmp">
<div>
<div class="lbl">Type tests</div>

```scala
def getClassAsString(x: Matchable): String = x match
  case s: String  => s"'$s' is a String"
  case i: Int     => "Int"
  case d: Double  => "Double"
  case l: List[?] => "List"
  case _          => "Unknown"

getClassAsString(1)              // Int
getClassAsString("hello")        // 'hello' is a String
getClassAsString(List(1, 2, 3))  // List
```

</div>
<div>
<div class="lbl">Exhaustive with a union type</div>

```scala
def describe(x: Int | String | Boolean): String =
  x match
    case i: Int    => s"Int, doubled: ${i * 2}"
    case s: String => s"String of length ${s.length}"
```

```text
[warn] match may not be exhaustive.
[warn]
[warn] It would fail on pattern case: true, false
```

</div>
</div>

<div class="src">Left: Scala 3 Book, "A Taste of Scala: Control Structures"; outputs and warning checked with Scala 3.9.0</div>

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 18px; line-height: 1.3; margin: 0.2rem 0 0.4rem 0; }
</style>

# Pattern Matching

- Lists can be taken apart by pattern matching

```scala
scala> val head :: tail = List(2, 5, 1).runtimeChecked
val head: Int = 2
val tail: List[Int] = List(5, 1)
```

- Isort with pattern matching

```scala
def isort(list: List[Int]): List[Int] = list match
  case Nil          => Nil
  case head :: tail => insert(head, isort(tail))

def insert(elem: Int, list: List[Int]): List[Int] = list match
  case Nil => List(elem)
  case head :: tail =>
    if elem <= head then elem :: list
    else head :: insert(elem, tail)
```

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 14px; line-height: 1.25; margin: 0; }
.nlbl { font-size: 18px; font-weight: 700; color: #575e75; margin: 0 0 0.15rem 0; }
</style>

# What does this Java code do?

<div class="nlbl">Java</div>

<div class="columns" style="align-items: start; gap: 1rem;">

```java
public class Roman
{
    public static class SymTab
    {
        char symbol;
        long value;
        public SymTab(char s, long v)
        {
            this.symbol=s; this.value=v;
        }
   };
   public static Roman.SymTab syms[]=
   {
        new Roman.SymTab('M',1000),
            new Roman.SymTab('D',500),
        new Roman.SymTab('C',100),
        new Roman.SymTab('L',50),
        new Roman.SymTab('X',10),
        new Roman.SymTab('V',5),
        new Roman.SymTab('I',1)
   };
```

```java
public static long toLong(String s) {
        long tot=0,max=0;
        char ch[]=s.toUpperCase().toCharArray();
        int i,p;
        for(p=ch.length-1;p>=0;p--)
        {
            for(i=0;i<syms.length;i++)
            {
                if(syms[i].symbol==ch[p])
                {
                    if(syms[i].value>=max)
                        tot+= (max = syms[i].value);
                    else
                        tot-= syms[i].value;
                }
            }
        }
        return tot;
   };
}
```

</div>

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 18px; line-height: 1.3; }
</style>

# An implementation in Scala using Lists

```scala
def roman(in: List[Char]): Int = in match {
   case 'I' :: 'V' :: rest => 4 + roman(rest)
   case 'I' :: 'X' :: rest => 9 + roman(rest)
   case 'I' :: rest => 1 + roman(rest)
   case 'V' :: rest => 5 + roman(rest)
   case 'X' :: 'L' :: rest => 40 + roman(rest)
   case 'X' :: 'C' :: rest => 90 + roman(rest)
   case 'X' :: rest => 10 + roman(rest)
   case 'L' :: rest => 50 + roman(rest)
   case 'C' :: 'D' :: rest => 400 + roman(rest)
   case 'C' :: 'M' :: rest => 900 + roman(rest)
   case 'C' :: rest => 100 + roman(rest)
   case 'D' :: rest => 500 + roman(rest)
   case 'M' :: rest => 1000 + roman(rest)
   case _ => 0
}
```

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 19px; line-height: 1.3; }
</style>

# Traits with Parameter

- Classes (or their constructor) can have Parameters. But Traits in Scala 2 could not. In Scala 3 now they can.
- Only the class that first extends the trait passes the arguments. A sub-trait cannot pass arguments.

```scala
trait Greeting(val name: String):
  def msg = s"Hello, $name!"
class C extends Greeting("Luke")           // the first class passes the argument
trait FormalGreeting extends Greeting      // a sub-trait passes no argument
class D extends C, FormalGreeting          // Greeting is already initialized by C
class E extends FormalGreeting, Greeting("Leia") // E must pass it itself
```

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 20px; line-height: 1.3; }
</style>

# Union Types

- Scala 3 allows a variable to have one of two (or several) types

```scala
case class UserName(name: String)
case class Email(address: String)
val id: UserName | Email = UserName("Marko")
case class Person(name:String, birthdate:Date) extends Ordered[Person]:
  def verify(id: UserName | Email): Boolean =
   id match
     case UserName(name) => lookupName(name)
     case Email(address) => lookupEmail(address)
```

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 19px; line-height: 1.3; }
section { font-size: 22px; }
</style>

# Intersection Types

- Likewise we can require a variable to have two (or more) types at the same time (usually traits). Intersection is very similar to “with” but it is commutative (the order of inheritance does not matter).

```scala
trait Camera:
   def takePhoto(): Unit = println("snap")
trait Phone:
   def makeCall(): Unit = println("ring")
def useSmartDevice(sp: Camera & Phone): Unit =
   sp.takePhoto()
   sp.makeCall()
class Smartphone extends Camera with Phone
useSmartDevice(new Smartphone)
```

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 24px; }
</style>

# Literal Types

- 1, 3.14, true and null are literals. Now they can also serve as Types.

```scala
val fieldSize : 1 | 4 | 9 = 9
```

---

<style scoped>
pre, code { font-variant-ligatures: none; font-feature-settings: "liga" 0, "calt" 0; }
pre { font-size: 21px; margin: 0.2rem 0 0.4rem 0; }
</style>

# ReadLine

- Scala has a ReadLine, but it requires an import

```scala
import scala.io.StdIn.readLine
```

- Then it can be used to read lines of input

```scala
print("Enter your first name: ")
val firstName = readLine()
print("Enter your last name: ")
val lastName = readLine()
println(s"Your name is $firstName $lastName")
```

---

<!-- _class: aufgabe -->

# Task 4: Build a Text UI

- Start building the core data structures of your game.
- Build a simple UI using text input and output.

---

<!-- _class: abschluss -->

# Questions?

## Thank you!

marko.boger@htwg-konstanz.de
