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
# Lecture 01: Scratch

Visual programming as a gentle introduction to core programming concepts.

<p class="small">Proof of concept migrated from the Google Slides deck "PR-01-Scratch", slides 1-8.</p>

---

# What Is Scratch

<div class="columns">
<div markdown="1">

- Scratch is a **block-based visual programming language** developed by MIT.
- It is designed for beginners, but it is strong enough to teach central programming ideas.
- Students can build **games, animations, and interactive stories**.
- It is available online at `scratch.mit.edu` and also offline.

Why it matters for us:

- it reduces syntax friction
- it makes logic visible
- it gives immediate feedback

</div>
<div markdown="1">

```mermaid
mindmap
  root((Scratch))
    Block-based
    Visual
    Beginner-friendly
    Online and offline
    Creates
      Games
      Animations
      Stories
    Teaches
      Logic
      Events
      Variables
      Routines
```

</div>
</div>

---

# Why We Start With Scratch

<div class="columns">
<div markdown="1">

- **No syntax errors**: we focus on logic instead of punctuation.
- **Immediate feedback**: results appear directly on the stage.
- **Creative motivation**: students can build things that feel playful and personal.
- **Transfer value**: the ideas later reappear in Python, Java, and C#.
- **University relevance**: it trains problem-solving and computational thinking.

</div>
<div markdown="1">

```mermaid
flowchart TD
    A[Scratch] --> B[Focus on logic]
    A --> C[See results immediately]
    A --> D[Create playful projects]
    A --> E[Transfer concepts later]
    B --> F[Less syntax frustration]
    C --> G[Fast learning loop]
    D --> H[More engagement]
    E --> I[Preparation for text-based languages]
```

</div>
</div>

---

# The Scratch Environment

<div class="columns">
<div markdown="1">

- **Stage**: where the animation or game becomes visible
- **Sprites**: programmable characters or objects
- **Blocks palette**: the available building blocks
- **Scripts area**: where blocks are assembled into behavior
- **Backdrops and sounds**: media that shape the scene

</div>
<div markdown="1">

```mermaid
flowchart LR
    subgraph UI["Scratch Workspace"]
      P[Blocks Palette] --> S[Scripts Area]
      S --> T[Stage]
      B[Backdrops and Sounds] --> T
      R[Sprites] --> S
      R --> T
    end
```

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

```mermaid
flowchart LR
    A[Sprite] --> B[Owns scripts]
    A --> C[Owns variables]
    A --> D[Responds to events]
    B --> E[Behavior]
    C --> E
    D --> E
    E --> F[Visible object on the stage]
```

</div>
</div>

---

# Types of Blocks

<div class="columns">
<div markdown="1">

Scratch uses different categories of blocks:

1. **Effect blocks** change appearance or sound
2. **Event blocks** start behavior
3. **Control blocks** manage flow
4. **Function blocks** compute and return values

The categories are important because they reflect different roles in a program.

</div>
<div markdown="1">

```mermaid
flowchart TD
    A[Scratch Blocks]
    A --> B[Effect Blocks]
    A --> C[Event Blocks]
    A --> D[Control Blocks]
    A --> E[Function Blocks]
    B --> B1[Change what we see or hear]
    C --> C1[Start execution]
    D --> D1[Sequence, repeat, decide]
    E --> E1[Compute a value]
```

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

```mermaid
flowchart TD
    A[Control Structures]
    A --> B[wait]
    A --> C[repeat]
    A --> D[forever]
    A --> E[if then]
    A --> F[if then else]
    B --> B1[Delay execution]
    C --> C1[Fixed repetition]
    D --> D1[Loop without end]
    E --> E1[Conditional action]
    F --> F1[Conditional branching]
```

</div>
</div>

---

# Blocks Are Routines

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

```mermaid
flowchart TD
    R[Routine]
    R --> P[Procedure]
    R --> F[Function]
    R --> M[Method]
    P --> P1[Input possible]
    P --> P2[No output]
    F --> F1[Parameters]
    F --> F2[Returns a value]
    M --> M1[Belongs to an object]
    M --> M2[Object-specific behavior]
```

</div>
</div>

---

# Scratch Blocks and Routines

<div class="columns">
<div markdown="1">

What this means for Scratch:

- command-style blocks behave like **procedures**
- reporter blocks behave like **functions**
- sprite-specific behavior looks like a **method**

So when we work with Scratch blocks, we are already learning a more general programming idea:

**Programs are built from reusable routines.**

</div>
<div markdown="1">

```mermaid
flowchart LR
    A[Scratch Blocks] --> B[Command Blocks]
    A --> C[Reporter Blocks]
    A --> D[Sprite-specific Scripts]
    B --> E[Procedure-like]
    C --> F[Function-like]
    D --> G[Method-like]
    E --> H[Reusable routine concepts]
    F --> H
    G --> H
```

</div>
</div>
