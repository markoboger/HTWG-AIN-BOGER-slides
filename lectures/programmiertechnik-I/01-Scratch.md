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
# Programmiertechnik I
Programming proficiency in the Age of AI

---

# Organization

- **Alternating lecturers**: this lecture is taught alternately by Prof. Dr. Marko Boger in the winter semester and Prof. Dr. Pascal Laube in the summer semester.
- **Materials**: all slides, files, and course materials are provided in **Moodle**.
- **Exercises**: Tutors (AIN Students 7. Semester) support and evaluate the exercises.
- **CodeTask**: CodeTask is a learning platform to support excercises and exams
- **Exams**: Exams are digital on the learning platform CodeTask
- **Grades**: Grades will be a mix of points collected throughout the semester and the final exam

---

# Prof. Dr. Marko Boger

- Room O205
- marko.boger@htwg-konstanz.de
- Office hours: Thursdays 11:30–13:00
- Dean of AIN, Software Engineering, Software Architecture

![bg right:40% contain](../../assets/marko-boger.jpg)

---

# Prof. Dr. Pascal Laube

- Room O205
- plaube@htwg-konstanz.de
- Office hours: by appointment via email
- Professor of Software Development and AI

![bg right:40% contain](../../assets/pascal-laube.jpg)

---

# About this Lecture Series

- [Moodle](https://moodle.htwg-konstanz.de/moodle/course/view.php?id=3194) as central infrastructure.
- Lectures are in presence.
- Lectures: Tuesdays 11:30–13:00 and Wednesdays 9:45–11:15, room G 240
- Exercises: Tuesdays in room O 008, 
  - group 2 (green) at 14:00–15:30, 
  - group 1 (blue) at 15:45–17:15
- Slides are in English, communication usually is in German.

---

<!-- _class: inhalt -->

<style scoped>
li { font-size: 0.8em; white-space: nowrap; }
</style>

# Main Goal of this Lecture

<p style="text-align:center; font-size:3em; font-weight:bold; margin-top:1.2em;">Programming proficiency</p>

- Introduction to programming for first-semester students of Applied Computer Science (AIN)
- The ability to read, write, and reason about code
- From visual programming with Scratch to general concepts: objects, routines, types, expressions, and scope
- Syntax, semantics, and type systems of programming lanugages
- Multiple paradigms: Procedural, Object-oriented, Functional
- Each lecture ends with a hands-on task to practice the new concepts

---

<!-- _class: inhalt -->

<style scoped>
.cols { display: grid; grid-template-columns: 1fr 1fr; column-gap: 3em; align-items: start; }
li { font-size: 0.9em; margin: 0; line-height: 1.35; }
li li { font-size: 1em; }
</style>

# Content of this Lecture

<div class="cols">
<div>

- Scratch
  - Introduction to concepts
  - First project - individual
- Scala
  - Languages and Paradigms
  - Number Types
  - Arrays and Lists
  - Control Structures
  - Tuple, Objects, Enums and Classes
  - Generic Types, Pattern Matching
  - Recursion

</div>
<div>

- Scala (continued)
  - Collections
  - Namespaces
  - LazyList
  - Second project - teams of two

- HTML, CSS

- Unity
  - C#
  - Third project - teams of two

</div>
</div>

---

<!-- _class: inhalt -->

# Content of this Lecture: Tools

- Scratch Editor
- Moodle
- CodeTask
- Scastie
- Command Line
- VS Code
- FMT
- Cursor
- Version Control


---

![bg](../../themes/htwgin-titel.png)
### Prof. Dr. Marko Boger, Prof. Dr. Pascal Laube
## Programmiertechnik I
# Lecture 01: Scratch

Visual programming as a gentle introduction to core programming concepts.

---

# What Is Scratch

- Scratch is a **block-based visual programming language** developed by MIT.
- It is designed for beginners, but it is strong enough to teach central programming ideas.
- Students can build **games, animations, and interactive stories**.
- It is available online at `scratch.mit.edu` and also offline.

Why it matters for us:

- it reduces syntax friction
- it makes logic visible
- it gives immediate feedback

---

# Why We Start With Scratch

- **No syntax errors**: we focus on logic instead of punctuation.
- **Immediate feedback**: results appear directly on the stage.
- **Creative motivation**: students can build things that feel playful and personal.
- **Transfer value**: the ideas later reappear in Scala and Unity.
- **University relevance**: it trains problem-solving and computational thinking.

---

<!-- _class: kapitel -->

# Basic Elements

Sprites, blocks and control structures

---

# The Scratch Environment

<div class="columns">
<div markdown="1">

- **Stage**: where the animation or game becomes visible
- **Sprites**: programmable characters or objects
- **Blocks palette**: the available building blocks
- **Scripts area**: where blocks are assembled into behavior
- **Backdrops and sounds**: media that shape the scene
- **Costumes tab**: draw a sprite's look (Pong: white rectangle, circle); the backdrop is the stage's picture (Pong: centre line)

</div>
<div markdown="1">

<div class="visual-frame">
<img src="assets/scratch-environment.png" alt="Scratch environment overview" />
</div>

</div>
</div>

---

# Sprites Are Objects

<div class="columns">
<div markdown="1">

- We will soon move to **object-oriented programming**.
- In Scratch, a sprite already behaves like a simple object.
- It has:
  - its own code
  - its own state
  - its own behavior on the stage

Core idea:

**A sprite is not only a picture. It is an executable thing.**

</div>
<div markdown="1">

<div class="visual-frame">
<img src="assets/sprites-are-objects.png" alt="Sprites mapped to objects" />
</div>

</div>
</div>

---

<style scoped>
.columns li { font-size: 0.78em !important; margin: 0 !important; line-height: 1.3 !important; }
</style>

# Types of Blocks

<div class="columns">
<div markdown="1">

Scratch groups its blocks into categories:

- **Motion**: move and turn sprites
- **Looks**: change appearance and speech bubbles
- **Sound**: play sounds and change volume
- **Events**: start scripts (green flag, key press, messages)
- **Control**: wait, loops, conditions, clones
- **Sensing**: react to input, touching, and timers
- **Operators**: arithmetic, comparisons, and logic
- **Variables**: variables and lists
- **My Blocks**: self-defined blocks

The categories are important because they reflect different roles in a program.

</div>
<div markdown="1">

<div class="visual-frame">
<img src="assets/types-of-blocks.png" alt="Scratch block categories" />
</div>

</div>
</div>

---

# Control Structures

<div class="columns">
<div markdown="1">

Control structures decide **when**, **how often**, and **under which condition** something happens.

Typical examples in Scratch:

- wait
- repeat
- forever
- if then
- if then else

These are the building blocks for algorithmic thinking.

</div>
<div markdown="1">

<div class="visual-pair">
<div class="visual-stack tight">
<div class="visual-frame"><img src="assets/control-wait.png" alt="Wait block" /></div>
<div class="visual-frame"><img src="assets/control-repeat.png" alt="Repeat block" /></div>
<div class="visual-frame"><img src="assets/control-forever.png" alt="Forever block" /></div>
</div>
<div class="visual-stack tight">
<div class="visual-frame"><img src="assets/control-if-then.png" alt="If then block" /></div>
<div class="visual-frame"><img src="assets/control-if-then-else.png" alt="If then else block" /></div>
</div>
</div>

</div>
</div>

---

# Coordinates and Direction

<div class="columns" style="grid-template-columns: auto 1fr; gap: 1.4rem; align-items: start; font-size: 18px;">
<div style="width: 500px;">
<img src="assets/stage-coordinates.png" alt="Stage 480 by 360 with (0, 0) in the centre and corners (±240, ±180); compass with directions 0 up, 90 right, 180 down, -90 left" style="width: 500px; margin: 0;">
<div style="display: flex; gap: 0.6rem; flex-wrap: wrap; margin-top: 0.6rem;">
<img src="assets/motion-go-to-xy.png" alt="go to x: 0 y: 0" style="width: 170px; margin: 0;">
<img src="assets/motion-point-direction.png" alt="point in direction 45" style="width: 170px; margin: 0;">
<img src="assets/motion-change-y.png" alt="change y by 8" style="width: 141px; margin: 0;">
</div>
</div>
<div markdown="1">

- The stage is **480 × 360** pixels, **(0, 0)** in the centre: x from -240 to 240, y from -180 to 180.
- `go to x: () y: ()` places a sprite; `change y by ()` moves up (+) or down (−); `x position` / `y position` report where it is.
- **Direction** in degrees: 90 = right, -90 = left, 0 = up, 180 = down; `move () steps` goes in the current direction.
- `if on edge, bounce` mirrors the direction at the stage edge.
- Mirroring by hand: `180 - direction` bounces off a horizontal surface, `0 - direction` off a vertical one (Pong paddles).

</div>
</div>

---

# Events and Parallel Scripts

<div class="columns" style="grid-template-columns: 1fr auto; gap: 1.6rem; align-items: start; font-size: 19px;">
<div markdown="1">

- Every script starts with a **hat block**: `when green flag clicked`, `when [key] key pressed`, `when I receive [msg]`.
- One green-flag click starts all flag scripts of all sprites **and of the stage** at the same time: they run **in parallel**.
- The stage can have scripts too, e.g. setting `score` to 0 at the start.
- `when key pressed` reacts with the keyboard repeat delay; for smooth movement check `key [w] pressed?` inside `forever`.

</div>
<div style="display: flex; flex-direction: column; gap: 0.7rem; width: 340px;">
<img src="assets/event-green-flag.png" alt="when green flag clicked" style="width: 156px; margin: 0;">
<img src="assets/event-key-pressed.png" alt="when space key pressed" style="width: 260px; margin: 0;">
<div style="font-size: 16px; color: #575e75;"><strong>Smooth movement:</strong></div>
<img src="assets/event-smooth-key-loop.png" alt="forever: if key w pressed then change y by 8" style="width: 328px; margin: 0;">
</div>
</div>

---

<!-- _class: kapitel -->

# Abstraction

Routines, functions, types, variables and scope

---

# Routines

<div class="columns">
<div markdown="1">

We use several names for reusable behavior:

- **Procedure**
  - may take input
  - has no return value
  - may have side effects
- **Function**
  - may take parameters
  - returns a value
- **Method**
  - a function or procedure that belongs to an object

The common abstraction is a **routine**.

</div>
<div markdown="1">

What this means for Scratch:

- command-style blocks behave like **procedures**
- reporter blocks behave like **functions**
- sprite-specific behavior looks like a **method**

So when we work with Scratch blocks, we are already learning a more general programming idea:

**Programs are built from reusable routines.**

</div>
</div>


---

# Function Blocks Have a Type

<div class="columns">
<div markdown="1">

Types are:

- **Numbers** `(round)`
  - only number input is allowed
- **Strings** `(round)`
  - numbers are converted to strings when necessary
- **Boolean** `(pointed)`

Function blocks are typed, and the shape already hints at what kind of value they produce.

</div>
<div markdown="1">

<div class="visual-pair">
<div class="visual-stack tight">
<div class="visual-frame"><img src="assets/function-type-round-number.png" alt="Round number block" /></div>
<div class="visual-frame"><img src="assets/function-type-string.png" alt="Round string block" /></div>
</div>
<div class="visual-frame"><img src="assets/function-type-boolean.png" alt="Boolean pointed block" /></div>
</div>

</div>
</div>

---

<style scoped>
/* all three block images share one scale (46 % of their natural pixel size) */
.columns { align-items: start; }
.columns img.same-scale { max-height: none; max-width: none; }
</style>

# Functions and Operators

<div class="columns">
<div markdown="1">

- Function blocks return a value.
- The value can be a **number**, a **string**, or a **boolean**.
- Operators are again constructed from function blocks.
- Some operators transform numbers or strings into boolean values.

This is the basis for building larger expressions from smaller parts.

</div>
<div markdown="1">

<div class="visual-stack tight">
<div class="visual-pair">
<div class="visual-frame"><img class="same-scale" style="width:180px" src="assets/function-example-reporter.png" alt="Reporter block example" /></div>
<div class="visual-frame"><img class="same-scale" style="width:208px" src="assets/function-example-operator.png" alt="Operator block example" /></div>
</div>
<div class="visual-center">
<div class="visual-frame"><img class="same-scale" style="width:232px" src="assets/function-example-boolean.png" alt="Boolean operator example" /></div>
</div>
</div>

</div>
</div>

---

# Expressions

<div class="columns">
<div markdown="1">

An **expression** combines numbers, variables, operations, or functions and can be evaluated to a value.

Expressions can also be nested.

- **Numeric expression**
  - contains only numbers
  - example: `3 + (5 * 2)`
- **Algebraic expression**
  - contains numbers and variables
  - example: `4x + 3`
- **Boolean expression**
  - uses logical operators such as `and`, `or`, and `not`
  - example: `A ^ (B | C)`

</div>
<div markdown="1">

<div class="visual-frame">
<img src="assets/expression-example.png" alt="Expression example from Scratch" />
</div>

</div>
</div>

---

# Variables

<div class="columns">
<div markdown="1">

- Variables can have a varying value.
- Variables can be:
  - defined
  - initialized
  - changed
  - incremented
  - shown on the stage as a **monitor** (checkbox), e.g. `score`
- Variables can have a **local** or **global** scope.

</div>
<div markdown="1">

<div class="visual-frame">
<img src="assets/variables-example.png" alt="Variable block example" />
</div>

<img src="assets/var-monitor.png" alt="Stage with the variable monitor score 3" style="width: 220px; margin: 0.6rem auto 0 auto; display: block;">

</div>
</div>

---

# Algebra

<div class="columns">
<div markdown="1">

**Algebra** is the branch of mathematics that works with variables and rules for manipulating them.

Key components:

- **Variables**: symbols for unknown or changing values
- **Constants**: fixed numeric values
- **Operations**: addition, subtraction, multiplication, division, and more
- **Expressions**: combinations such as `2x + 5`
- **Equations**: statements like `2x + 5 = 11`
- **Functions**: rules like `f(x) = x^2`

</div>
<div markdown="1">

Types of algebra:

- **Elementary algebra**: basic operations, linear and quadratic equations
- **Abstract algebra**: structures such as groups, rings, and fields
- **Linear algebra**: vectors, matrices, and transformations
- **Boolean algebra**: logic with binary values for computing

</div>
</div>

---

<style scoped>
.columns { align-items: start; }
</style>

# Boolean Algebra

<div class="columns">
<div markdown="1">

Boolean algebra is the algebra of **truth values**.

Instead of calculating with numbers such as `3` or `17`, we calculate with:

- `true`
- `false`

It is used whenever a program needs to make a decision.

Typical operators are:

- **and**
- **or**
- **not**

</div>
<div markdown="1">

Examples:

- `score > 10 and lives > 0`
- `touching edge or touching enemy`
- `not gameOver`

This matters in Scratch because conditions inside blocks such as **if**, **if else**, and **repeat until** are boolean expressions.

</div>
</div>

---

# First Game: Pong

<div style="display: flex; justify-content: space-between; align-items: flex-start; gap: 1.2rem; margin-top: 0.4rem; font-size: 18px; color: #575e75;">
<div style="display: flex; flex-direction: column; gap: 0.3rem;"><strong>Ball</strong>
<img src="assets/pong-ball.png" alt="Ball: when green flag clicked, go to x 0 y 0, point in direction 45, forever: move 8 steps, if on edge bounce, if touching Paddle then point in direction 180 minus direction" style="width: 286px; margin: 0 0 0.4rem 0;">
</div>
<div style="display: flex; flex-direction: column; gap: 0.3rem;"><strong>Paddle</strong>
<img src="assets/pong-paddle.png" alt="Paddle: when green flag clicked, forever: set x to mouse x" style="width: 193px; margin: 0 0 0.4rem 0;">
</div>
<div style="display: flex; flex-direction: column; gap: 0.3rem;"><strong>First collision check</strong>
<img src="assets/pong-touching.png" alt="touching Paddle?" style="width: 235px; margin: 0 0 0.4rem 0;">
<img src="assets/pong-stage.png" alt="Pong stage: ball bounces off the edge and the paddle" style="width: 256px; margin: 0 0 0.4rem 0;">
</div>
</div>

<p style="text-align: center; font-size: 24px; margin-top: 0.3rem;"><strong>A collision is just a condition checked in every loop.</strong></p>

---

# Messages

<div class="columns">
<div markdown="1">

- Messages are events that can be received and trigger execution.
- Messages can not have parameters.
- One script **sends** a message with `broadcast`.
- Another script **starts** when it matches that message with `when I receive`.
- `broadcast () and wait` continues only after all receiving scripts have finished (Pong: reset the ball, then go on).

This is how Scratch lets sprites coordinate behavior.

</div>
<div markdown="1">

<div class="scratch-block-stack">
  <div>
    <img src="assets/event-broadcast-block.png" alt="broadcast start game" style="width: 280px; margin: 0;">
    <div class="scratch-note">send a message to all sprites</div>
  </div>
  <div>
    <img src="assets/event-when-i-receive.png" alt="when I receive start game" style="width: 300px; margin: 0;">
    <div class="scratch-note">start this script when that message arrives</div>
  </div>
</div>

</div>
</div>

---

# Namespace

<div class="columns" style="grid-template-columns: 1fr auto; gap: 1.5rem; align-items: center; font-size: 20px;">
<div markdown="1">

Namespaces are an important concept in programming languages.

They help us manage:

- visibility
- scope

In Scratch, there are only two namespaces:

- the object or sprite
- the global namespace

A global namespace can be problematic, but it is common in scripting-oriented systems such as JavaScript.

</div>
<div>
<img src="assets/namespace-tree.png" alt="Namespace tree: global namespace contains the global variable score, the Stage, sprite Ball and sprite Paddle; Ball and Paddle each have their own local variable speed. Highlighted path: global › Ball › speed" style="width: 532px; margin: 0;">
</div>
</div>

---

# Visibility or Scope

<div class="columns" style="grid-template-columns: 1fr auto; gap: 1.5rem; align-items: center; font-size: 20px;">
<div markdown="1">

Variables have a visibility:

- **global**: available to all objects
- **local**: available only in the defining object

Messages are always sent globally as a broadcast.

This is a limitation.

We will later introduce namespaces to define visibility and scope in a much more fine-grained way.

</div>
<div>
<img src="assets/scope-matrix.png" alt="Access matrix: global variables and broadcast messages are available from the same script, other scripts of the sprite, the Stage and other sprites; local variables only from the same sprite, other sprites can only read them with the sensing block speed of Ball" style="width: 523px; margin: 0;">
</div>
</div>

---

# Project Ideas: Classic Arcade Games

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.2rem; margin-top: 0.4rem;">
<div style="background: #fff; border: 2px solid #d9e3f2; border-radius: 14px; padding: 0.6rem; display: flex; flex-direction: column; gap: 0.35rem;">
<img src="assets/retro-pong.png" alt="Own pixel-art illustration in the style of Pong" style="width: 100%; margin: 0; border-radius: 6px; image-rendering: pixelated;">
<div style="display: flex; justify-content: space-between; align-items: baseline;"><strong style="font-size: 21px; color: #222;">Pong</strong><span style="color: #ff8c1a; font-size: 18px; letter-spacing: 0.1em;">★☆☆</span></div>
<div style="font-size: 16px; color: #575e75;"><strong>Scratch:</strong> touching, bounce, score variable</div>
</div>
<div style="background: #fff; border: 2px solid #d9e3f2; border-radius: 14px; padding: 0.6rem; display: flex; flex-direction: column; gap: 0.35rem;">
<img src="assets/retro-breakout.png" alt="Own pixel-art illustration in the style of Breakout" style="width: 100%; margin: 0; border-radius: 6px; image-rendering: pixelated;">
<div style="display: flex; justify-content: space-between; align-items: baseline;"><strong style="font-size: 21px; color: #222;">Breakout</strong><span style="color: #ff8c1a; font-size: 18px; letter-spacing: 0.1em;">★☆☆</span></div>
<div style="font-size: 16px; color: #575e75;"><strong>Scratch:</strong> clones for bricks, touching, lives</div>
</div>
<div style="background: #fff; border: 2px solid #d9e3f2; border-radius: 14px; padding: 0.6rem; display: flex; flex-direction: column; gap: 0.35rem;">
<img src="assets/retro-lunar-lander.png" alt="Own pixel-art illustration in the style of Lunar Lander" style="width: 100%; margin: 0; border-radius: 6px; image-rendering: pixelated;">
<div style="display: flex; justify-content: space-between; align-items: baseline;"><strong style="font-size: 21px; color: #222;">Lunar Lander</strong><span style="color: #ff8c1a; font-size: 18px; letter-spacing: 0.1em;">★★☆</span></div>
<div style="font-size: 16px; color: #575e75;"><strong>Scratch:</strong> gravity via variables, key events, fuel</div>
</div>
</div>

<p style="text-align: center; font-size: 22px; margin-top: 0.9rem;"><strong>Build the core mechanic first, then add levels, sound, and polish.</strong></p>

---

# More Project Ideas

<div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.2rem; margin-top: 0.4rem;">
<div style="background: #fff; border: 2px solid #d9e3f2; border-radius: 14px; padding: 0.6rem; display: flex; flex-direction: column; gap: 0.35rem;">
<img src="assets/retro-space-invaders.png" alt="Own pixel-art illustration in the style of Space Invaders" style="width: 100%; margin: 0; border-radius: 6px; image-rendering: pixelated;">
<div style="display: flex; justify-content: space-between; align-items: baseline;"><strong style="font-size: 21px; color: #222;">Space Invaders</strong><span style="color: #ff8c1a; font-size: 18px; letter-spacing: 0.1em;">★★☆</span></div>
<div style="font-size: 16px; color: #575e75;"><strong>Scratch:</strong> clones for aliens and shots, broadcasts</div>
</div>
<div style="background: #fff; border: 2px solid #d9e3f2; border-radius: 14px; padding: 0.6rem; display: flex; flex-direction: column; gap: 0.35rem;">
<img src="assets/retro-asteroids.png" alt="Own pixel-art illustration in the style of Asteroids" style="width: 100%; margin: 0; border-radius: 6px; image-rendering: pixelated;">
<div style="display: flex; justify-content: space-between; align-items: baseline;"><strong style="font-size: 21px; color: #222;">Asteroids</strong><span style="color: #ff8c1a; font-size: 18px; letter-spacing: 0.1em;">★★★</span></div>
<div style="font-size: 16px; color: #575e75;"><strong>Scratch:</strong> direction and rotation, clones that split</div>
</div>
<div style="background: #fff; border: 2px solid #d9e3f2; border-radius: 14px; padding: 0.6rem; display: flex; flex-direction: column; gap: 0.35rem;">
<img src="assets/retro-climber.png" alt="Own pixel-art illustration in the style of Donkey Kong" style="width: 100%; margin: 0; border-radius: 6px; image-rendering: pixelated;">
<div style="display: flex; justify-content: space-between; align-items: baseline;"><strong style="font-size: 21px; color: #222;">Donkey Kong</strong><span style="color: #ff8c1a; font-size: 18px; letter-spacing: 0.1em;">★★★</span></div>
<div style="font-size: 16px; color: #575e75;"><strong>Scratch:</strong> clones for barrels, touching color for platforms, levels</div>
</div>
</div>

<p style="text-align: center; font-size: 22px; margin-top: 0.9rem;"><strong>All illustrations are our own pixel art, not screenshots of the original games.</strong></p>

---

# Finished Example: Pong.sb3

<div class="columns" style="grid-template-columns: auto 1fr; gap: 1.6rem; align-items: start; margin-top: 0.3rem;">
<div style="width: 430px;">
<img src="assets/pong-game-stage.png" alt="The finished Pong project running: black stage, dashed centre line, two white paddles, a ball, and the score monitors score left and score right" style="width: 430px; margin: 0; border-radius: 8px; border: 2px solid #d9e3f2;">
<div style="font-size: 16px; color: #575e75; margin-top: 0.4rem;">Open <strong>Pong.sb3</strong> and click the green flag.<br>Left paddle: <strong>W / S</strong> &middot; right paddle: <strong>&uarr; / &darr;</strong></div>
</div>
<div style="font-size: 18px;" markdown="1">

- **Sprites + stage:** Paddle Left, Paddle Right, Ball; the stage draws the centre line
- **Smooth movement:** `forever` + `if key pressed` for each paddle
- **Motion:** `move (speed) steps` and `if on edge, bounce`
- **Collision:** `touching` a paddle **and** the right direction, then `point in direction (0 - direction)`
- **Scoring:** global variables, checked via the ball's x position
- **Serve:** `broadcast new ball` resets the ball; every hit makes it faster

<img src="assets/pong-game-hit.png" alt="if touching Paddle Right and direction greater than 0 then point in direction 0 minus direction, change speed by 0.5" style="width: 440px; margin: 0.5rem 0 0 0;">

</div>
</div>

---

<!-- _class: inhalt -->

<style scoped>
section { font-size: 23px; }
</style>

# Summary

- Scratch is a block-based visual language (MIT) for learning core ideas without syntax noise
- Stage, sprites, blocks; sprites behave like simple objects with code and state
- Block categories, control structures, coordinates, events and parallel scripts
- Abstraction: blocks as procedures/functions; types (number, string, boolean); expressions
- Variables, algebra, and boolean algebra for conditions
- Messages (broadcast), namespace, and visibility/scope (global vs local)
- First game ideas (e.g. Pong) and classic arcade project suggestions

---

<!-- _class: aufgabe -->

# Task

Create a Scratch project.

It should contain:

- expressions
- variables
- messages

---

<!-- _class: abschluss -->

# Questions?

## Thank you!

marko.boger@htwg-konstanz.de
