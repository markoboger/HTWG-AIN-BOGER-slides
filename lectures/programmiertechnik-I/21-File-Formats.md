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
# Lecture 21: File Formats

<p class="small">Migrated from the Google Slides deck "PR-21-FileFormats" ("21 - File Formats"). Vorlesung number in the course plan may be 20; the Present deck is numbered 21.</p>

---

<!-- _class: inhalt -->

# Goals

(Goals to fill)

---

<!-- _class: kapitel -->

## 1
# File Formats

CSV, YAML, JSON, and XML

---

<style scoped>
pre { font-size: 16px; }
</style>

# An example

Let's take a look at a simple data structure and data set.

```scala
case class Animal(Name: String, Species: String, Age: Int, Weight: Double)

val animals = List(
  Animal("Leo", "Lion", 5, 190),
  Animal("Bella", "Elephant", 12, 4000),
  Animal("Milo", "Parrot", 3, 0.5),
  Animal("Luna", "Tiger", 7, 250)
)
```

---

# File Formats

When writing data to a file, it can make sense to use a standard format. This could be:

- **CSV** (Comma-Separated Values): Plain text format storing tabular data, with fields separated by commas. Simple, widely supported, but lacks complex data structure support.
- **JSON** (JavaScript Object Notation): Lightweight, text-based format using key-value pairs and arrays. Human-readable, supports nested data, and is platform-independent.
- **YAML** (YAML Ain't Markup Language): Human-readable format with indentation-based structure. Supports complex data types and is often used for configuration files.
- **XML** (Extensible Markup Language): Text-based format using tags to define data structure. Verbose but flexible, used in web services and legacy systems.

---

# CSV

```text
Name,Species,Age,Weight
Leo,Lion,5,190
Bella,Elephant,12,4000
Milo,Parrot,3,0.5
Luna,Tiger,7,250
```

- The first row is the **header**, defining columns: Name, Species, Age, Weight
- Each subsequent row represents an animal with its corresponding values
- Fields are separated by commas

---

<style scoped>
section { font-size: 19px; }
pre { font-size: 14px; }
</style>

# YAML

<div class="columns" style="grid-template-columns: 1fr 1fr; align-items: start;">
<div markdown="1">

```yaml
animals:
  - Name: Leo
    Species: Lion
    Age: 5
    Weight: 190
  - Name: Bella
    Species: Elephant
    Age: 12
    Weight: 4000
  - Name: Milo
    Species: Parrot
    Age: 3
    Weight: 0.5
  - Name: Luna
    Species: Tiger
    Age: 7
    Weight: 250
```

</div>
<div markdown="1">

- YAML uses **indentation** (typically 2 spaces) to define structure
- The `animals` key contains a list (indicated by `-`) of animal entries
- Each animal is represented as a set of key-value pairs (Name, Species, Age, Weight)
- This format is human-readable and supports hierarchical data

</div>
</div>

---

# YAML – YAML Ain’t Markup Language

YAML is similar to XML or JSON.

- YAML is a very simple textual data format
- Basic types are String, Number, Boolean, Map, Sequence
- Key-value pairs, separated by colon: `key: value`
- Indentation with 2 spaces creates maps
- `-` creates a sequence
- `#` is a comment

---

<style scoped>
section { font-size: 17px; }
pre { font-size: 12.5px; }
</style>

# Example YAML file

<div class="columns" style="grid-template-columns: 1fr 1fr; align-items: start;">
<div markdown="1">

```yaml
# Scalar Data Types (strings, numbers, booleans, null)
animal_name: Tiger      # String (no quotes needed for simple strings)
age: 5                 # Integer
weight: 200.5          # Float
is_wild: true          # Boolean
owner: null            # Null value

# String with Special Characters (requires quotes)
habitat: "Savanna, Forest"  # String with comma, quoted to avoid parsing issues

# Multi-line String (using | for literal style)
description: |
  The tiger is a large carnivore,
  known for its distinctive orange coat
  with black stripes.
```

</div>
<div markdown="1">

```yaml
# Mapping (Key-Value Pairs)
lion:
  name: Simba          # String
  age: 3              # Integer
  is_leader: true     # Boolean
  territory: Pride Lands

# List (Sequence of Items)
pets:
  - Cat              # List item 1
  - Dog              # List item 2
  - Parrot           # List item 3

# Nested Structure (Mapping with List)
zoo:
  name: City Zoo
  animals:
    - species: Elephant
      weight: 6000.0
      diet: Herbivore
    - species: Penguin
      weight: 30.0
      diet: Carnivore
```

</div>
</div>

---

<style scoped>
section { font-size: 18px; }
pre { font-size: 13px; }
</style>

# JSON

<div class="columns" style="grid-template-columns: 1.1fr 0.9fr; align-items: start;">
<div markdown="1">

```json
{ "animals": [
    { "Name": "Leo",
      "Species": "Lion",
      "Age": 5,
      "Weight": 190
    },
    { "Name": "Bella",
      "Species": "Elephant",
      "Age": 12,
      "Weight": 4000
    },
    { "Name": "Milo",
      "Species": "Parrot",
      "Age": 3,
      "Weight": 0.5
    },
    { "Name": "Luna",
      "Species": "Tiger",
      "Age": 7,
      "Weight": 250
    }
  ]
}
```

</div>
<div markdown="1">

- JSON uses curly braces `{}` for objects and square brackets `[]` for arrays
- The `animals` key contains an array of objects, each representing an animal
- Each animal has key-value pairs for Name, Species, Age, and Weight
- JSON is compact, widely used in APIs, and machine-readable
- Save this in a `.json` file (e.g. `animals.json`) for use in applications that parse JSON

</div>
</div>

---

<style scoped>
section { font-size: 17px; }
pre { font-size: 12px; }
</style>

# XML

<div class="columns" style="grid-template-columns: 1.1fr 0.9fr; align-items: start;">
<div markdown="1">

```xml
<?xml version="1.0" encoding="UTF-8"?>
<animals>
    <animal>
        <Name>Leo</Name>
        <Species>Lion</Species>
        <Age>5</Age>
        <Weight>190</Weight>
    </animal>
    <animal>
        <Name>Bella</Name>
        <Species>Elephant</Species>
        <Age>12</Age>
        <Weight>4000</Weight>
    </animal>
    <animal>
        <Name>Milo</Name>
        <Species>Parrot</Species>
        <Age>3</Age>
        <Weight>0.5</Weight>
    </animal>
    <animal>
        <Name>Luna</Name>
        <Species>Tiger</Species>
        <Age>7</Age>
        <Weight>250</Weight>
    </animal>
</animals>
```

</div>
<div markdown="1">

- XML uses **tags** (e.g. `<animal>`, `<Name>`) to define data structure, with opening and closing tags for each element
- The root element is `<animals>`, containing multiple `<animal>` elements
- Each `<animal>` element includes sub-elements for Name, Species, Age, and Weight
- The `<?xml version="1.0" encoding="UTF-8"?>` declaration specifies the XML version and character encoding

</div>
</div>

---

# Use Cases

- **CSV** is often used to import and export to Spreadsheets
- **YAML** is optimised for human-readable configuration files
- **JSON** is designed to work well for data exchange, especially to the front end. JSON can directly be used in JavaScript
- **XML** is designed to work well for large data and automated processing. XML can have a grammar and can be validated against this grammar

---

<!-- _class: inhalt -->

<style scoped>
section { font-size: 23px; }
</style>

# Summary

- Standard formats help store structured data in files
- **CSV**: header row, tabular fields, spreadsheet import/export
- **YAML**: indentation-based, human-readable config; scalars, maps, sequences
- **JSON**: objects `{}` and arrays `[]`; common for data exchange / APIs
- **XML**: tagged tree structure with opening/closing elements
- Use cases differ by audience: spreadsheets, config, interchange, markup documents

---

<!-- _class: aufgabe -->

# Task

(Task to fill)

---

<!-- _class: abschluss -->

# Questions?

## Thank you!

marko.boger@htwg-konstanz.de
