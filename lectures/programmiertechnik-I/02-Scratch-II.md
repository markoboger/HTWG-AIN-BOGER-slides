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
# Lecture 02: Scratch II

Deepening the core programming concepts with Scratch.

---

# Prof. Dr. Marko Boger

- Room O205
- marko.boger@htwg-konstanz.de
- Office hours: Thursdays 11:30–13:00
- Dean of Studies, Applied Computer Science (AIN)

![bg right:40% contain](../../assets/marko-boger.jpg)

---

# Prof. Dr. Pascal Laube

- Room O205
- plaube@htwg-konstanz.de
- Office hours: by appointment via email
- Professor of Software Development

![bg right:40% contain](../../assets/pascal-laube.jpg)

---

# Tutors

Exercises are supported and evaluated by Tutors.

---

# Learning Goals

- Use clones to create repeated or dynamic game elements.
- Store and manage data with variables and lists.
- Organize larger projects with custom blocks and clear responsibilities.
- Model game flow with states such as start, play, pause, and game over.
- Debug Scratch projects systematically instead of guessing.

---

# Event-Driven Concurrency

- A Scratch project often runs many scripts at the same time.
- Events such as green flag, key press, broadcast, and clone start coordinate behavior.
- This means we must think about timing, ordering, and shared data.
- Good design keeps scripts small and gives each script one clear job.
- Broadcast messages help synchronize actions without tightly coupling sprites.

---

# Clones and Procedural Behavior

- Clones let one sprite create many temporary copies at runtime.
- Use them for bullets, enemies, falling objects, or particle effects.
- Each clone can react independently, but it still shares some design decisions with the original sprite.
- Always define how clones are created, updated, and deleted.
- If clones are not removed carefully, projects become slow and hard to control.

---

# Variables, Lists, and Data

- Variables store single values such as score, speed, health, or level.
- Lists store many values and are useful for inventories, questions, names, or wave patterns.
- Think carefully about scope: does this data belong to one sprite or to the whole game?
- Structured data makes larger projects easier to extend.
- When data changes unexpectedly, check every script that can write to it.

---

# Custom Blocks and Abstraction

- Custom blocks let us package repeated logic into named operations.
- They improve readability, reduce duplication, and make projects easier to debug.
- Use parameters so a block can work with different inputs.
- A good custom block communicates intent, for example: spawn enemy, reset level, or update HUD.
- Abstraction means hiding low-level detail so we can think at a higher level.

---

# Advanced Design Patterns

To be defined

---

# Game States and Screen Flow

<div class="columns">
<div markdown="1">

- Larger games should not mix menu logic, gameplay logic, and end screen logic in the same scripts.
- A state variable helps control which behaviors are active.
- Scripts should check the current state before they run expensive or visible actions.
- Broadcast messages can switch the game cleanly from one state to another.

</div>
<div markdown="1">

**Typical states:**

- menu
- playing
- paused
- game over
- victory

</div>
</div>

---

# Collision Detection Patterns

<div class="columns">
<div markdown="1">

- Scratch can detect collisions with touching sprite, color, or edge.
- Simple checks are enough for many projects, but they can still produce unexpected results.
- Fast-moving objects may skip over a target if movement steps are too large.
- One solution is to move in smaller steps or separate movement from collision response.

</div>
<div markdown="1">

**Common failure modes:**

- missed hits
- multiple triggers
- wrong sprite responds
- collision happens before state update

</div>
</div>

---

# Timing, Randomness, and Balance

<div class="columns">
<div markdown="1">

- Timers, wait blocks, and variable-based counters shape the rhythm of a game.
- Randomness can make a project feel alive, but too much randomness can feel unfair.
- Balance means tuning speed, spawn rate, score rewards, and difficulty progression.

</div>
<div markdown="1">

**Playtesting advice:**

- change one value at a time
- record what changed
- compare versions
- watch for fairness and pacing

</div>
</div>

---

# Debugging and Project Architecture

<div class="columns">
<div markdown="1">

- Debugging starts by reproducing the bug consistently.
- Check one script at a time and temporarily simplify the project.
- Display important variables on screen to observe hidden state.
- Use say blocks or temporary visual markers to confirm that events happen when expected.

</div>
<div markdown="1">

**Architecture principles:**

- assign clear sprite responsibilities
- separate setup, play, and cleanup
- use consistent names
- avoid hidden shared state

</div>
</div>

---

# Versioning

To be defined

---

# Sharing

To be defined

---

# Scratch and Unity

- Scratch
  - Project
- Unity
  - Project
  - C#

---

# Task

- Build a small advanced Scratch game or simulation.
- Your project should use clones, at least one list, custom blocks, and a clear game state model.
- Include one debugging strategy during development, such as visible variables or temporary tracing messages.
- Prepare to explain how your design avoids chaos when many scripts run at once.
- Focus on clarity, structure, and maintainability, not only on visual effects.
