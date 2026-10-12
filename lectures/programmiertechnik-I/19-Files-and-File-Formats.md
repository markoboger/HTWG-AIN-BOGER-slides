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
# Lecture 19: Files and File Formats

<p class="small">Running example: saillog · git tag <code>v19-files</code></p>

---

<!-- _class: inhalt -->

<style scoped>
section { font-size: 20px; }
</style>

# Goals

In this lecture you will learn

- the **running example** for the next six lectures: a sailing logbook, **saillog**
- how to model its domain with **case classes** and enums
- how to read, write and list files with **os-lib**
- the common **text formats**: CSV, JSON, YAML, XML – and when to use which
- how to **parse** CSV by hand and GPX (XML) with **scala-xml**
- how to save and load **JSON** with **uPickle**
- how to handle broken files with `Try` (Lecture 15)

---

<!-- _class: kapitel -->

## 1
# The Sailing Logbook

One example, six lectures

---

# saillog: What We Build

- A **logbook** for the trips (*Törns*) of HTWG's training boats on Lake Constance: the motorboat **Dock** and the keelboat **X99 Expresso**
- Boats, crew, trips – and for every trip a **GPS track**
- Six steps, one per lecture:

| Lecture | Step | Tag |
|---|---|---|
| 19 | read tracks from files, save as JSON | `v19-files` |
| 20 | store everything in a database | `v20-db` |
| 21 | offer it as a web service (REST) | `v21-http` |
| 22 | HTML pages for people | `v22-html` |
| 23 | make them look good with CSS | `v23-css` |
| 24 | type-safe HTML templates | `v24-templates` |

---

# Getting the Code

```bash
git clone <course repo>/saillog
cd saillog
git checkout v19-files
sbt "runMain saillog.lecture19"
```

- Every lecture has a **tag** – jump to any state with `git checkout`
- `git diff v19-files v20-db` shows exactly what changed (Lecture 11)
- Requirements: **JDK 17+**, **Scala 3.9.0**, sbt

---

# Branches: main, dev, feature

```text
*   Release v20-db                         (main, tag v20-db)
|\
| *   Merge feature/20-db into dev          (dev)
| |\
| | * Add SQLite repository with ScalaSql   (feature/20-db)
| | * Add LogbookRepository trait
| |/
* | Release v19-files                       (main, tag v19-files)
```

- `main`: only finished lecture states, each with a **tag**
- `dev`: integration branch; every lecture starts as `feature/NN-...` off `dev`
- Done → `git merge --no-ff` into `dev`, then `dev` into `main`, then `git tag`
- Feature branches stay: `git checkout feature/20-db` shows the small steps

---

# The Domain Model

```scala
enum BoatKind derives ReadWriter:
  case Motorboat, Keelboat, Catamaran

enum Role derives ReadWriter:
  case Skipper, Crew

case class Boat(id: Int, name: String, kind: BoatKind) derives ReadWriter
case class CrewMember(name: String, role: Role) derives ReadWriter
case class TrackPoint(lat: Double, lon: Double, time: Instant) derives ReadWriter

case class Trip(id: Int, boatId: Int, date: LocalDate, title: String,
                crew: List[CrewMember], track: List[TrackPoint]) derives ReadWriter
```

- Value objects and entities from Lecture 17
- `derives ReadWriter`: as in Lecture 17 – generates the JSON conversion (uPickle, later in this lecture)

---

# Distance: the Haversine Formula

```scala
object Geo:
  val EarthRadiusNm = 3440.065

  def haversineNm(a: TrackPoint, b: TrackPoint): Double =
    val dLat = math.toRadians(b.lat - a.lat)
    val dLon = math.toRadians(b.lon - a.lon)
    val h = math.pow(math.sin(dLat / 2), 2) +
      math.cos(math.toRadians(a.lat)) * math.cos(math.toRadians(b.lat)) *
      math.pow(math.sin(dLon / 2), 2)
    2 * EarthRadiusNm * math.asin(math.sqrt(h))

  def distanceNm(track: List[TrackPoint]): Double =
    track.zip(track.drop(1)).map(haversineNm).sum
```

- Great-circle distance in **nautical miles**; `track.zip(track.drop(1))`: neighbouring pairs

$$a = \sin^2\frac{\Delta\varphi}{2} + \cos\varphi_1\cos\varphi_2\sin^2\frac{\Delta\lambda}{2},\quad c = 2\,\operatorname{atan2}(\sqrt{a},\sqrt{1-a}),\quad d = R\cdot c$$

- $R$ = 3440.065 nm (Earth radius); the code uses the equivalent $c = 2\arcsin\sqrt{a}$

---

# Statistics with Collections

```scala
object Stats:
  def nmPerBoat(trips: List[Trip]): Map[Int, Double] =
    trips.groupMapReduce(_.boatId)(t => Geo.distanceNm(t.track))(_ + _)

  def nmPerSeason(trips: List[Trip]): Map[Int, Double] =
    trips.groupMapReduce(_.date.getYear)(t => Geo.distanceNm(t.track))(_ + _)

  def hours(t: Trip): Double =
    Duration.between(t.track.head.time, t.track.last.time).toSeconds / 3600.0

  def avgSpeedKn(t: Trip): Double = Geo.distanceNm(t.track) / hours(t)
```

- `groupMapReduce`: group, map each element, combine per group (Lecture 12)
- Speed in **knots** = nautical miles per hour

---

<!-- _class: kapitel -->

## 2
# Working with Files

os-lib

---

# Files: Why a Library?

- Java offers `java.io.File` and `java.nio.file.Files` – powerful, but verbose
- **os-lib** (Li Haoyi) wraps them in a small, Scala-friendly API
- Paths are **values** of type `os.Path`, not strings

```scala
//> using scala 3.9.0
//> using dep com.lihaoyi::os-lib:0.11.8
```

```scala
"com.lihaoyi" %% "os-lib" % "0.11.8"     // build.sbt
```

---

# Paths

```scala
val data = os.pwd / "data"              // current directory + "data"
val gpx  = data / "konstanz-meersburg.gpx"

gpx.last          // "konstanz-meersburg.gpx"
gpx.ext           // "gpx"
gpx / os.up       // back to data
os.home           // your home directory
```

- Separators differ: Unix/Linux/macOS `data/track.gpx`, Windows `data\track.gpx` – in a string literal `"data\\track.gpx"` (hence the double backslash)
- Hard-coded separators or `+` concatenation break on the other system – let the library build the path:

```scala
java.nio.file.Paths.get("data", "track.gpx")         // plain Java
"data" + java.io.File.separator + "track.gpx"        // works, but clumsy
os.pwd / "data" / "konstanz-meersburg.gpx"           // os-lib: right separator per OS
```

---

# Reading, Writing, Listing

```scala
os.read(gpx)                        // whole file as String
os.read.lines(csv)                  // IndexedSeq[String]
os.write.over(file, "text")         // create or overwrite
os.exists(file)                     // Boolean
os.remove(file)
os.list(data)                       // all entries of a directory
```

- One function per task, all in the `os` object
- `os.write` fails if the file exists – `os.write.over` replaces it
- Errors are **exceptions** → wrap in `Try` when the file may be broken

---

# Importing a Whole Folder

```scala
for file <- os.list(data).filter(f => f.ext == "gpx" || f.ext == "csv") do
  val track = if file.ext == "gpx" then Gpx.read(file) else Csv.read(file)
  track.fold(
    err => println(s"${file.last}: FAILED (${err.getMessage})"),
    pts => println(f"${file.last}: ${pts.size} points, ${Geo.distanceNm(pts)}%.2f nm"))
```

```text
abendrunde.csv: 3 points, 4.75 nm
kaputt.gpx: FAILED (For input string: "47,66")
konstanz-meersburg.gpx: 4 points, 4.39 nm
```

- `Gpx.read` and `Csv.read` return `Try[List[TrackPoint]]`
- `fold`: one function for `Failure`, one for `Success`

---

<!-- _class: kapitel -->

## 3
# File Formats

CSV, JSON, YAML and XML

---

# File Formats

When writing data to a file, it makes sense to use a standard format:

- **CSV** (Comma-Separated Values): tabular data, fields separated by commas. Simple, widely supported, no nesting
- **JSON** (JavaScript Object Notation): objects and arrays. Human-readable, nested data, the standard of the web
- **YAML** (YAML Ain't Markup Language): indentation-based, used for configuration files
- **XML** (Extensible Markup Language): tags define the structure. Verbose but flexible, can be validated against a grammar

---

# CSV

```text
time,lat,lon
2026-07-02T14:00:00Z,47.6603,9.1758
2026-07-02T14:30:00Z,47.6450,9.2300
2026-07-02T15:00:00Z,47.6603,9.1758
```

- The first row is the **header**, defining the columns
- Each following row is one record – here one **track point**
- Many GPS apps export tracks as CSV
- Pitfalls: commas inside values, `;` instead of `,`, decimal comma `47,66`

---

# Parsing CSV

```scala
object Csv:
  def parse(lines: Seq[String]): List[TrackPoint] =
    lines.drop(1).map(_.split(",")).collect {
      case Array(t, lat, lon) =>
        TrackPoint(lat.toDouble, lon.toDouble, Instant.parse(t))
    }.toList

  def read(file: os.Path): Try[List[TrackPoint]] = Try(parse(os.read.lines(file)))
```

- `drop(1)` skips the header
- `collect` with a **pattern** keeps only rows with exactly three fields (Lecture 9)
- `Try` turns a `NumberFormatException` into a `Failure` (Lecture 15)

---

# YAML

<div class="columns" style="grid-template-columns: 1fr 1fr; align-items: start;">
<div markdown="1">

```yaml
boats:
  - id: 1
    name: Dock
    kind: Motorboat
  - id: 2
    name: X99 Expresso
    kind: Keelboat
# a comment
season: 2026
```

</div>
<div markdown="1">

- **Indentation** (2 spaces) defines structure
- `key: value` pairs form maps
- `-` creates a sequence
- `#` is a comment
- Basic types: string, number, boolean, map, sequence
- Typical use: **configuration** (CI pipelines, Docker Compose)
- Not used in saillog

</div>
</div>

---

# JSON

```json
{
  "id": 1,
  "boatId": 1,
  "date": "2026-06-14",
  "title": "Konstanz – Meersburg",
  "crew": [ { "name": "Marko", "role": "Skipper" } ],
  "track": [ { "lat": 47.6603, "lon": 9.1758, "time": "2026-06-14T10:00:00Z" } ]
}
```

- Objects `{}` with key-value pairs, arrays `[]`
- Values: string, number, boolean, `null`, object, array
- The standard for **data exchange** on the web (Lecture 21)

---

# XML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<boats>
  <boat id="1">
    <name>Dock</name>
    <kind>Motorboat</kind>
  </boat>
</boats>
```

- **Tags** with opening and closing elements, nested as a tree
- **Attributes** inside the opening tag: `id="1"`
- The declaration `<?xml ...?>` names version and encoding
- Grammars (XSD) allow validation – used for large, automated processing

---

# GPX: GPS Tracks in XML

```xml
<gpx version="1.1" creator="saillog" xmlns="http://www.topografix.com/GPX/1/1">
  <trk><name>Konstanz – Meersburg</name><trkseg>
    <trkpt lat="47.6603" lon="9.1758"><time>2026-06-14T10:00:00Z</time></trkpt>
    <trkpt lat="47.6645" lon="9.2050"><time>2026-06-14T10:20:00Z</time></trkpt>
    <trkpt lat="47.6800" lon="9.2400"><time>2026-06-14T10:45:00Z</time></trkpt>
    <trkpt lat="47.6935" lon="9.2710"><time>2026-06-14T11:10:00Z</time></trkpt>
  </trkseg></trk>
</gpx>
```

- **GPX** = GPS Exchange Format, exported by every GPS device and app
- Position as **attributes**, time as **child element**
- File `data/konstanz-meersburg.gpx` in the repo

---

# Use Cases

| Format | Typical use | In saillog |
|---|---|---|
| CSV | spreadsheets, simple exports | track import |
| JSON | web APIs, data exchange, documents | logbook file, REST API |
| YAML | configuration | – |
| XML | documents, standards with a grammar | GPX tracks, HTML (Lecture 22) |

- You rarely choose freely: the **other side** (device, service, tool) decides
- Rule of thumb: **read** what you get, **write** JSON

---

<!-- _class: kapitel -->

## 4
# Parsing XML and JSON

scala-xml and uPickle

---

# scala-xml

- Until Scala 2.12, XML was part of the standard library
- Since then it is a **separate module** – also in Scala 3

```scala
//> using dep org.scala-lang.modules::scala-xml:2.5.0
```

```scala
"org.scala-lang.modules" %% "scala-xml" % "2.5.0"     // build.sbt
```

| Expression | Meaning |
|---|---|
| `XML.loadString(s)` | parse a string into a tree |
| `doc \\ "trkpt"` | all `trkpt` elements, at any depth |
| `p \ "time"` | direct children named `time` |
| `p \@ "lat"` | value of the attribute `lat` |

---

# Parsing GPX

```scala
object Gpx:
  def parse(xml: String): List[TrackPoint] =
    val doc = XML.loadString(xml)
    (doc \\ "trkpt").map { p =>
      TrackPoint((p \@ "lat").toDouble, (p \@ "lon").toDouble,
                 Instant.parse((p \ "time").text))
    }.toList

  def read(file: os.Path): Try[List[TrackPoint]] = Try(parse(os.read(file)))
```

- Eight lines for a real-world format
- We ignore everything we do not need: names, elevation, extensions
- `Instant.parse`: ISO-8601 timestamps such as `2026-06-14T10:00:00Z`

---

# Broken Files

```xml
<trkpt lat="47,66" lon="9.17"><time>2026-06-14T10:00:00Z</time></trkpt>
```

```scala
Gpx.read(data / "kaputt.gpx")
// Failure(java.lang.NumberFormatException: For input string: "47,66")
```

- Real files are often broken: decimal comma, missing `<time>`, cut off
- `Try` keeps the program running and tells us **which** file failed
- Never let one bad file crash the whole import

---

# uPickle: JSON for Case Classes

```scala
//> using dep com.lihaoyi::upickle:4.4.3
```

```scala
import upickle.default.*

case class Boat(id: Int, name: String, kind: BoatKind) derives ReadWriter

write(Boat(1, "Dock", BoatKind.Motorboat))
// {"id":1,"name":"Dock","kind":"Motorboat"}

read[Boat]("""{"id":1,"name":"Dock","kind":"Motorboat"}""")
// Boat(1,Dock,Motorboat)
```

- `derives ReadWriter` as introduced in Lecture 17 – here it pays off: no conversion code by hand
- Field names become JSON keys

---

# Types uPickle Does Not Know

```scala
given ReadWriter[Instant]   = readwriter[String].bimap(_.toString, Instant.parse)
given ReadWriter[LocalDate] = readwriter[String].bimap(_.toString, LocalDate.parse)
```

- uPickle has instances for numbers, strings, collections, `Option`, case classes …
- … but not for `java.time.Instant` or `LocalDate`
- `bimap`: reuse the `String` instance, convert **to** and **from** string
- A `given` instance for our own needs – as in Lecture 17 (`given`) and 18

---

# Saving and Loading the Logbook

```scala
object Json:
  def save(file: os.Path, trips: List[Trip]): Unit =
    os.write.over(file, write(trips, indent = 2))

  def load(file: os.Path): List[Trip] =
    read[List[Trip]](os.read(file))
```

```scala
Json.save(os.pwd / "logbook.json", trips)
val back = Json.load(os.pwd / "logbook.json")
println(s"JSON round trip ok: ${back == trips}")    // true
```

- **Round trip**: `read(write(x)) == x` – the best test for any format
- Case classes compare by value, so `==` checks every field

---

# The Whole Program

```scala
@main def lecture19(): Unit =
  // ... import all files (slide "Importing a Whole Folder") ...
  Json.save(os.pwd / "logbook.json", trips)
  val back = Json.load(os.pwd / "logbook.json")
  println(s"JSON round trip ok: ${back == trips}")
  println(f"nm per boat: ${Stats.nmPerBoat(trips)}")
  println(f"avg speed trip 1: ${Stats.avgSpeedKn(trips.head)}%.1f kn")
```

```text
JSON round trip ok: true
nm per boat: Map(1 -> 4.393303678701589, 2 -> 4.753595337995797)
avg speed trip 1: 3.8 kn
```

---

# Project Layout at `v19-files`

```text
saillog/
  build.sbt                 Scala 3.9.0, os-lib, upickle, scala-xml
  data/                     konstanz-meersburg.gpx, abendrunde.csv, kaputt.gpx
  src/main/scala/saillog/
    model/  Model.scala  Geo.scala  Stats.scala
    io/     Gpx.scala    Csv.scala  Json.scala
    Lecture19.scala
```

- `model`: the domain – knows nothing about files
- `io`: formats – knows the model, but not where data comes from
- Separation that pays off in the next lectures

---

# Outlook: Is a JSON File Enough?

- Every change **reads and rewrites** the whole `logbook.json`
- 10,000 trips? Two people saving at the same time?
- "Nautical miles per boat in 2026" – must load **everything**
- Next lecture: put the logbook into a **database** – behind an interface, so that the JSON file stays as one option

---

<!-- _class: inhalt -->

<style scoped>
section { font-size: 20px; }
</style>

# Summary

- saillog: boats, crew, trips with GPS tracks – our example until Lecture 24
- os-lib: `os.Path`, `os.read`, `os.write.over`, `os.list`
- Formats: **CSV** for tables, **JSON** for exchange, **YAML** for configuration, **XML** for documents and standards like GPX
- CSV by hand: `split` + pattern matching; XML with scala-xml: `\\`, `\`, `\@`
- uPickle: `derives ReadWriter`, own `given` for `Instant`, round trip test
- `Try` for broken files
- Haversine distance in nautical miles, statistics with `groupMapReduce`

---

<!-- _class: aufgabe -->

# Task

- Check out `v19-files` and run `sbt "runMain saillog.lecture19"`
- Export one of your own tracks (phone app, Strava, …) as GPX and add it to `data/`
- Write `Stats.longestTrip(trips: List[Trip]): Option[Trip]`
- Make the CSV parser accept `;` as separator as well
- Bonus: print the top speed between two neighbouring track points


---

<style scoped>
table { font-size: 0.72em; }
th, td { padding: 4px 12px; white-space: nowrap; }
</style>

# Project Ideas in This Style

Examples for your own project. Your own idea in the same style is just as welcome:

| # | Project | Domain model | File format |
|---|---|---|---|
| 1 | Calendar (recurring events) | `Calendar`, `Event`, `Recurrence` (enum) | iCalendar `.ics` |
| 2 | Appointments (consultation hours) | `Slot`, `Booking`, `Person` | CSV |
| 3 | CD collection | `Album`, `Artist`, `Track` | XML |
| 4 | Shared flat expenses (who owes whom) | `Flatmate`, `Expense`, `Share` | CSV |
| 5 | Gym log (machines, sets, reps) | `Machine`, `Exercise`, `WorkoutSet` | JSON |
| 6 | Recipe book | `Recipe`, `Ingredient`, `Unit` (enum) | YAML |
| 7 | Library (lending) | `Book`, `Member`, `Loan` | JSON |
| 8 | Vehicle logbook (rides, fuel) | `Vehicle`, `Ride`, `Refuel` | CSV |
| 9 | Phone book | `Contact`, `PhoneNumber`, `Address` | vCard `.vcf` or CSV |

- Same size for your own idea: 2–3 case classes, one import and one storage format

---

<!-- _class: abschluss -->

# Questions?

## Thank you!

marko.boger@htwg-konstanz.de
