---
marp: true
theme: htwg
paginate: true
_paginate: false
footer: "![](../../themes/htwgin40.png)&nbsp;&nbsp;Prof. Dr. Marko Boger"
_footer: ""
---

![bg](../../themes/htwgin-titel.png)

## Programmiertechnik I
# Lecture 03: Programming Languages

How languages differ in abstraction level, paradigm, typing, execution model, and practical use.

<p class="small">Migrated from the Google Slides deck "PR-03-Languages". Dense visual slides intentionally keep the original slide imagery.</p>

---

# Most Popular Programming Languages

<div class="columns">
<div markdown="1">

- Programming languages change with industry trends, platforms, and ecosystems.
- Popularity is not the same as quality, but it often reflects demand and community size.
- We use this slide as an entry point into a bigger question:
  - Why are there so many languages?
  - What trade-offs do they make?
  - Which problems are they built for?

Video reference:

[Most Popular Programming Languages](https://www.youtube.com/watch?v=MTBuneHqLTM)

</div>
<div markdown="1">

<div class="visual-frame">
<img src="assets/languages/slide-02-popular-languages.png" alt="Most popular programming languages slide" />
</div>

</div>
</div>


---

# Layer

<img src="diagrams/slide-03-layer.drawio.svg"/>

---

# Example: Assembler and Machine Code

```asm
An example of a machine-language program
;
; The problem
; Read a series of numbers from memory
; beginning at x4000. Read until the
; number 0 is read. Count how many
; of the numbers are even and odd.
; Store the count of even numbers at
; x3200 and the number of odd numbers
; at x3201.

```

---

# Assembler Code

```asm
LD R1, x00F          ; load address of data
AND R4, R4, #0       ; set even-counter to 0
AND R5, R5, #0       ; set odd-counter to 0

x3003  LDR R2, R1, #0    ; load next number
       BRz x00C          ; branch to end if zero

       AND R3, R2, #1    ; check least significant bit
       BRz x009          ; branch if even
       ADD R5, R5, #1    ; increment odd-count
       BRnzp x00A

x3009  ADD R4, R4, #1    ; increment even-count
x300A  ADD R1, R1, #1    ; next value
       BRnzp x003

x300C  STI R4, x010      ; store even count
       STI R5, x011      ; store odd count
       HALT
```

Assembler is already more readable than pure bits, but it is still very close to the hardware model.

---

# Machine Code

```asm
0011 0000 0000 0000
0010 001 0 0000 1111
0101 100 100 1 00000
0101 101 101 1 00000
0110 010 001 000000
0000 010 0 0000 1100
0101 011 010 1 00001
0000 010 0 0000 1001
0001 101 101 1 00001
0000 111 0 0000 1010
0001 100 100 1 00001
0001 001 001 1 00001
0000 111 0 0000 0011
1011 100 0 0001 0000
1011 101 0 0001 0001
1111 0000 0010 0101
```

Machine code is precise and executable, but for humans it is extremely hard to understand, debug, and maintain.

---

# Example in C

```c
#include <stdio.h>

int main() {
    int numbers[] = {4, 7, 2, 9, 1, 6, 0};
    int even_count = 0;
    int odd_count = 0;
    int memory[2];
    int i = 0;

    while (numbers[i] != 0) {
        if (numbers[i] % 2 == 0) {
            even_count++;
        } else {
            odd_count++;
        }
        i++;
    }

    memory[0] = even_count;
    memory[1] = odd_count;
    printf("Even count: %d\n", memory[0]);
    printf("Odd count: %d\n", memory[1]);
}
```
---

# A Short Language History

![bg height:80%]<img src="diagrams/language-history.drawio.svg"/>

---

# Paradigm

A **paradigm** is a typical way of thinking about programs.

The three big families in this lecture are:

- **Procedural**
  - programs are organized as steps, commands, and routines
- **Object-oriented**
  - programs are organized around objects with state and behavior
- **Functional**
  - programs are organized around functions, expressions, and transformations

Most modern languages are not purely one paradigm.

---

# Paradigms

<div class="columns">
<div markdown="1">

The core difference is what we treat as the main building block:

- procedural: functions and control flow
- object-oriented: objects and methods
- functional: functions and expressions

Different paradigms encourage different program structure, testing style, and reasoning habits.

</div>
<div markdown="1">

<div class="visual-frame">
<img src="assets/languages/slide-10-paradigms.png" alt="Procedural and object-oriented paradigm comparison" />
</div>

</div>
</div>

---

# Platform

<div class="columns">
<div markdown="1">

Some languages are strongly tied to a platform:

- browser
- operating system
- virtual machine
- mobile ecosystem

Others are more portable and can target several platforms.

Platform matters because it influences:

- tooling
- distribution
- performance
- developer audience

</div>
<div markdown="1">

<div class="visual-frame">
<img src="assets/languages/slide-11-platform.png" alt="Platform slide" />
</div>

</div>
</div>

---

# Typing

Typing describes how a language treats values and their kinds.

**Static typing**

- the compiler checks types before running the program
- many mistakes are found early
- refactoring is usually safer

**Dynamic typing**

- types are checked while the program runs
- code can be concise and flexible
- some errors appear later

Neither side is magic. Each gives benefits and costs.

---

# Strong and Weak Typing

**Strong typing** means the language enforces clearer boundaries between types.

- fewer surprising implicit conversions
- less accidental mixing of incompatible values

**Weak typing** allows more implicit conversion.

This can feel convenient, but it may also create surprising behavior:

- `false + 7 = 7`
- `7 + true = 8`
- `"10" + 5 = "105"`

This is why typing is not only a theory topic. It changes daily programming experience.

---

# Typing Matrix

We can combine the two distinctions:

|                    | Strong typing | Weak typing |
|--------------------|---------------|-------------|
| Static typing      | e.g. Scala, Java, Rust | e.g. C with low-level pointer freedom |
| Dynamic typing     | e.g. Python | e.g. JavaScript in many everyday situations |

Important:

- the categories are useful teaching tools
- real languages are more nuanced than a simple matrix
- edge cases and language versions matter

---

# Execution

There are two broad execution models:

**Compiled**

- source code is translated first
- output may be machine code or bytecode
- many checks happen before execution

**Interpreted**

- the program is executed more directly by an interpreter
- checks often happen at runtime

In practice, modern runtimes mix ideas:

- bytecode
- JIT compilation
- virtual machines

---

# GPL and DSL

<div class="columns">
<div markdown="1">

**General-purpose languages (GPLs)** are designed for many different tasks.

Examples:

- Java
- Python
- Scala
- C

**Domain-specific languages (DSLs)** are tailored to a narrower problem space.

Examples:

- SQL for databases
- HTML/CSS for presentation
- MATLAB-like environments for numeric work

</div>
<div markdown="1">

<div class="visual-frame">
<img src="assets/languages/slide-16-gpl-dsl.png" alt="General-purpose and domain-specific languages" />
</div>

</div>
</div>

---

# Language Families

<div class="columns">
<div markdown="1">

Languages influence each other and form families.

Examples:

- the Lisp family
- the ML family
- the C family
- the JVM ecosystem

Knowing a language family helps you predict:

- syntax style
- type system ideas
- standard abstractions

</div>
<div markdown="1">

<div class="visual-frame">
<img src="assets/languages/slide-17-language-families.png" alt="Language families" />
</div>

</div>
</div>

---

# VM Languages

<div class="columns">
<div markdown="1">

A **virtual machine** is a runtime layer between the program and the operating system.

Benefits:

- portability
- runtime services
- tooling
- memory management

Two well-known ecosystems:

- **JVM**
- **.NET**

</div>
<div markdown="1">

<div class="visual-frame">
<img src="assets/languages/slide-18-vm-languages.png" alt="VM languages slide" />
</div>

</div>
</div>

---

# Dead, Alive, and Livelihood

<div class="columns">
<div markdown="1">

Languages can be judged in at least three different ways:

- **Dead**
  - rarely used in new projects
- **Alive**
  - active ecosystem, learning material, ongoing development
- **Livelihood**
  - enough demand that it can shape job opportunities

These are different questions.
A language may be academically interesting, industrially valuable, or both.

</div>
<div markdown="1">

<div class="visual-frame">
<img src="assets/languages/slide-19-dead-alive-livelihood.png" alt="Dead, alive, livelihood slide" />
</div>

</div>
</div>

---

# Set of Existing Programming Languages

<div class="columns">
<div markdown="1">

Language categories overlap.

For example:

- C is procedural
- Java adds object-orientation
- Scala adds strong functional support
- Haskell sits deeper in the functional space

This is why labels help, but they never tell the full story.

</div>
<div markdown="1">

<div class="visual-frame">
<img src="assets/languages/slide-20-set-of-languages.png" alt="Set of existing programming languages" />
</div>

</div>
</div>

---

# Jump Game

We use the same problem in several languages to compare style.

Problem statement:

- you start at the first array position
- each number tells you the maximum jump length from that position
- return `true` if you can reach the last index
- otherwise return `false`

Examples:

- `[2, 3, 1, 1, 4]` -> `true`
- `[3, 2, 1, 0, 4]` -> `false`

The algorithm stays similar, but the expression of the solution changes from language to language.

---

<div class="visual-center">
<img src="assets/languages/slide-22-c.png" alt="C language profile slide" style="max-width: 95%; max-height: 600px;" />
</div>

---

<div class="visual-center">
<img src="assets/languages/slide-23-cpp.png" alt="C++ language profile slide" style="max-width: 95%; max-height: 600px;" />
</div>

---

<div class="visual-center">
<img src="assets/languages/slide-24-java.png" alt="Java language profile slide" style="max-width: 95%; max-height: 600px;" />
</div>

---

<div class="visual-center">
<img src="assets/languages/slide-25-swift.png" alt="Swift language profile slide" style="max-width: 95%; max-height: 600px;" />
</div>

---

<div class="visual-center">
<img src="assets/languages/slide-26-javascript.png" alt="JavaScript language profile slide" style="max-width: 95%; max-height: 600px;" />
</div>

---

<div class="visual-center">
<img src="assets/languages/slide-27-rust.png" alt="Rust language profile slide" style="max-width: 95%; max-height: 600px;" />
</div>

---

<div class="visual-center">
<img src="assets/languages/slide-28-python.png" alt="Python language profile slide" style="max-width: 95%; max-height: 600px;" />
</div>

---

<div class="visual-center">
<img src="assets/languages/slide-29-scala-for.png" alt="Scala with for-comprehension slide" style="max-width: 95%; max-height: 600px;" />
</div>

---

<div class="visual-center">
<img src="assets/languages/slide-30-scala-recursion.png" alt="Scala recursion slide" style="max-width: 95%; max-height: 600px;" />
</div>

---

<div class="visual-center">
<img src="assets/languages/slide-31-scala-fold.png" alt="Scala fold slide" style="max-width: 95%; max-height: 600px;" />
</div>

---

# Closeness and Learnability

<div class="visual-center">
<img src="assets/languages/slide-32-closeness-learnability.png" alt="Closeness and learnability slide" style="max-width: 92%; max-height: 600px;" />
</div>

---

# Sprachen in AIN

<div class="visual-center">
<img src="assets/languages/slide-33-sprachen-ain.png" alt="Languages in AIN slide" style="max-width: 92%; max-height: 600px;" />
</div>

---

# Degree Paths

<div class="visual-center">
<img src="assets/languages/slide-34-roadmap.png" alt="Degree paths slide" style="max-width: 92%; max-height: 600px;" />
</div>

---

# Programming after Agile

Agile development increased the importance of:

- testability
- modularity
- fast feedback
- safe refactoring

The original deck argues that this strengthens the case for functional ideas:

- avoid unnecessary `void`
- avoid unnecessary `null`
- reduce hidden state
- prefer explicit effects

Scala is presented as a language that combines functional techniques with object orientation.

---

# Programming after Big Data

Big data systems need:

- parallelism
- distribution
- composition of transformations

That pushes us toward:

- associative operations
- algebraic thinking
- immutable data and pure transformations where possible

This is one reason functional programming became more influential again.
The deck also connects this trend to Spark and therefore to Scala.

---

# Programming after AI

If more code is generated automatically, then language design matters even more.

What becomes valuable:

- strong static typing
- modularity
- testability
- precise interfaces

The more code we create, review, and regenerate, the more we benefit from languages that make mistakes visible early.
