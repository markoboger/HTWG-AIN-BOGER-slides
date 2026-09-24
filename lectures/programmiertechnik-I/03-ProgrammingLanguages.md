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

# Example in BASIC: Lunar Lander (1/2)

<style scoped>pre { font-size: 0.55em; }</style>

```basic
10 REM *** LUNAR LANDER ***
20 REM EXAMPLE FOR THE FIRST-SEMESTER LECTURE
30 REM H = HEIGHT IN METERS
40 REM V = VELOCITY IN M/S (POSITIVE = DOWNWARD)
50 REM F = FUEL, B = BURN (THRUST), T = TIME IN SECONDS
60 REM G = GRAVITY (EACH SECOND V GROWS BY G)
70 REM --- INITIAL VALUES ---
80 LET H = 500
90 LET V = 50
100 LET F = 250
110 LET T = 0
120 LET G = 5
130 PRINT "LUNAR LANDING: TOUCH DOWN AT 5 M/S OR LESS!"
140 PRINT "EACH TURN IS ONE SECOND. BURN 0 TO 30."
150 PRINT "EVERY 2 UNITS OF BURN SLOW YOU BY 1 M/S."
160 PRINT
170 REM --- MAIN LOOP: STATUS DISPLAY ---
180 PRINT "TIME"; T; "  HEIGHT"; H; "  SPEED"; V; "  FUEL"; F
190 IF F > 0 THEN 240
200 PRINT "OUT OF FUEL - FREE FALL!"
210 LET B = 0
220 GOTO 330
230 REM --- READ THE BURN ---
240 PRINT "BURN";
250 INPUT B
260 IF B < 0 THEN 290
270 IF B > 30 THEN 290
280 GOTO 310
290 PRINT "INVALID! PLEASE ENTER A VALUE FROM 0 TO 30."
300 GOTO 240
310 IF B <= F THEN 330
320 LET B = F
```

---

# Example in BASIC: Lunar Lander (2/2)

<style scoped>pre { font-size: 0.55em; }</style>

```basic
330 REM --- PHYSICS: ONE SECOND PASSES ---
340 LET F = F - B
350 LET W = V
360 LET V = V + G - B / 2
370 LET H = H - (W + V) / 2
380 LET T = T + 1
390 IF H > 0 THEN 180
400 REM --- TOUCHDOWN: WIN OR LOSE ---
410 PRINT
420 PRINT "TOUCHDOWN AFTER"; T; "SECONDS AT"; V; "M/S."
430 IF V <= 5 THEN 490
440 IF V <= 15 THEN 470
450 PRINT "CRASH! YOU JUST MADE A NEW CRATER."
460 GOTO 520
470 PRINT "HARD LANDING. THE SHIP IS DAMAGED."
480 GOTO 520
490 PRINT "PERFECT LANDING! CONGRATULATIONS, COMMANDER."
500 PRINT "FUEL LEFT:"; F
510 REM --- PLAY AGAIN? ---
520 PRINT
530 PRINT "PLAY AGAIN (1 = YES, 0 = NO)";
540 INPUT A
550 IF A = 1 THEN 80
560 PRINT "END OF MISSION."
570 END
```

BASIC (Dartmouth, 1964) is already a high-level language, but control flow still works with line numbers and GOTO jumps, much like the branches in assembler.

---

# Lunar Lander: The Arcade Game (Atari, 1979)

<style scoped>
.video-link { position: relative; display: inline-block; line-height: 0; }
.video-link img { height: 430px; width: auto; border-radius: 12px; box-shadow: 0 10px 28px rgba(0, 0, 0, 0.18); }
.video-link .play { position: absolute; left: 50%; top: 50%; width: 96px; height: 96px; margin: -48px 0 0 -48px; border-radius: 50%; background: rgba(0, 155, 145, 0.8); border: 3px solid rgba(255, 255, 255, 0.9); box-sizing: border-box; }
.video-link .play::after { content: ""; position: absolute; left: 35px; top: 25px; border-style: solid; border-width: 20px 0 20px 32px; border-color: transparent transparent transparent #ffffff; }
</style>

<div class="visual-center">
<a class="video-link" href="https://www.youtube.com/embed/McAhSoAEbhM?start=0&end=60"><img src="assets/languages/lunar-lander-atari-1979.jpg" alt="Lunar Lander (Atari, 1979) arcade gameplay video" /><span class="play"></span></a>
</div>

Watch the first minute: [youtube.com/embed/McAhSoAEbhM](https://www.youtube.com/embed/McAhSoAEbhM?start=0&end=60) — Atari's 1979 arcade version: same idea as our BASIC program (fuel, height, speed), now with vector graphics.

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
