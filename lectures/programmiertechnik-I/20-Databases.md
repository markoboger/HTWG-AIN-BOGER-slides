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
# Lecture 20: Databases

<p class="small">Running example: saillog · git tag <code>v20-db</code> · branch <code>feature/20-db</code></p>

---

<!-- _class: inhalt -->

<style scoped>
section { font-size: 20px; }
</style>

# Goals

In this lecture you will learn

- why a single JSON file is not enough for real data
- the **repository pattern**: one trait, several implementations
- a **document store** (NoSQL style) built from our JSON file
- the **relational model**: tables, rows, keys, joins
- **SQL** basics: `CREATE`, `INSERT`, `SELECT`, `JOIN`, `GROUP BY`
- **functional relational mapping** with **ScalaSql** and SQLite
- how to test two implementations against each other

---

<!-- _class: kapitel -->

## 1
# Why a Database?

From files to data management

---

# The Problem with `logbook.json`

- Every change **reads and rewrites** the whole file
- Two programs saving at the same time → one change is **lost**
- A crash in the middle of `write` → a **broken** file
- "Nautical miles per boat in 2026" → load **everything** into memory
- What we want:
  - change small parts, safely (**transactions**)
  - ask questions without loading everything (**queries**)
  - several users at once (**concurrency**)

---

# Database Systems

- A **database management system** (DBMS) stores data and answers queries
- **Relational** (SQL): data in tables – PostgreSQL, MySQL, Oracle, **SQLite**
- **NoSQL**: everything else – documents (MongoDB), key-value (Redis), graphs (Neo4j)
- **SQLite**: a whole SQL database in **one file**, no server needed
  - in every phone, every browser, many desktop apps
  - perfect for learning and for small applications
- We will keep **both** worlds – behind one interface

---

<!-- _class: kapitel -->

## 2
# The Repository Pattern

One interface, many storages

---

# Repository: the Idea

- The rest of the program should **not care** where data lives
- A **repository** offers domain operations: "all boats", "add a trip"
- Storage details are hidden behind a **trait** (Lecture 17)

```text
          Lecture20 / web server (Lecture 21)
                        │
               LogbookRepository   ← trait
                ┌───────┴────────┐
      JsonFileRepository    SqlRepository
         logbook.json        logbook.db
```

---

# The Trait

```scala
trait LogbookRepository:
  def boats: List[Boat]
  def addBoat(boat: Boat): Unit
  def trips: List[Trip]
  def addTrip(trip: Trip): Unit

  def trip(id: Int): Option[Trip] = trips.find(_.id == id)
  def boat(id: Int): Option[Boat] = boats.find(_.id == id)
  def nextTripId: Int = trips.map(_.id).maxOption.getOrElse(0) + 1

  def nmPerBoat: Map[String, Double] =
    Stats.nmPerBoat(trips).map((id, nm) => boat(id).fold("?")(_.name) -> nm)
```

- Four **abstract** methods – every storage must implement them
- The rest has a **default** built on top – may be overridden

---

# Option Instead of null

```scala
def trip(id: Int): Option[Trip] = trips.find(_.id == id)
```

```scala
repo.trip(2).map(_.crew.map(_.name))    // Some(List(Marko, Anna))
repo.trip(99)                           // None
```

- "Not found" is a normal answer, not an error
- `Option` makes it visible in the type (Lecture 15)
- In Lecture 21 `None` becomes **HTTP 404**

---

<!-- _class: kapitel -->

## 3
# A Document Store

NoSQL with a JSON file

---

# Documents

- A **document store** saves whole objects as documents – usually JSON
- No fixed schema, nested data is natural: a trip **contains** its crew and track
- Our version: the whole logbook is **one** document

```scala
case class Logbook(boats: List[Boat], trips: List[Trip]) derives ReadWriter
```

- Real document databases (MongoDB, CouchDB) add indexes, queries and concurrency

---

# JsonFileRepository

```scala
class JsonFileRepository(file: os.Path) extends LogbookRepository:
  private def load: Logbook =
    if os.exists(file) then read[Logbook](os.read(file)) else Logbook(Nil, Nil)
  private def save(lb: Logbook): Unit = os.write.over(file, write(lb, indent = 2))

  def boats: List[Boat] = load.boats
  def trips: List[Trip] = load.trips
  def addBoat(boat: Boat): Unit = save(load.copy(boats = load.boats :+ boat))
  def addTrip(trip: Trip): Unit = save(load.copy(trips = load.trips :+ trip))
```

- Ten lines – reuses os-lib and uPickle from Lecture 19
- `copy`: a new immutable `Logbook` with one field changed

---

<!-- _class: kapitel -->

## 4
# The Relational Model

Tables, keys and SQL

---

# Tables

**boat_row**

| id | name | kind |
|---|---|---|
| 1 | Pirat | Dinghy |
| 2 | Lacustre | Keelboat |

**trip_row**

| id | boat_id | date | title | distance_nm |
|---|---|---|---|---|
| 1 | 1 | 2025-06-14 | Konstanz – Meersburg | 4.39 |
| 2 | 2 | 2026-07-02 | Evening round | 4.75 |

- `id`: **primary key**; `boat_id`: **foreign key** pointing to a boat

---

# Lists Become Tables

- A table cell holds a single value – no lists
- A trip has **many** track points and **many** crew members
- → separate tables that point back to the trip

| trip_id | idx | lat | lon | time |
|---|---|---|---|---|
| 1 | 0 | 47.6603 | 9.1758 | 2026-06-14T10:00:00Z |
| 1 | 1 | 47.6645 | 9.205 | 2026-06-14T10:20:00Z |

- This is called **normalisation**
- Contrast: the document store keeps the track **inside** the trip

---

# SQL: Creating Tables

```sql
CREATE TABLE IF NOT EXISTS boat_row (id INTEGER PRIMARY KEY, name TEXT, kind TEXT)
CREATE TABLE IF NOT EXISTS trip_row (id INTEGER PRIMARY KEY, boat_id INTEGER,
                                     date TEXT, title TEXT, distance_nm REAL)
CREATE TABLE IF NOT EXISTS point_row (trip_id INTEGER, idx INTEGER,
                                      lat REAL, lon REAL, time TEXT)
CREATE TABLE IF NOT EXISTS crew_row (trip_id INTEGER, name TEXT, role TEXT)
```

- **SQL** (Structured Query Language): the language of relational databases
- Types in SQLite: `INTEGER`, `REAL`, `TEXT`, `BLOB`
- Dates are stored as ISO text: `2026-06-14`

---

# SQL: Queries

```sql
INSERT INTO boat_row (id, name, kind) VALUES (1, 'Pirat', 'Dinghy');

SELECT name FROM boat_row WHERE kind = 'Dinghy';

SELECT boat_row.name, SUM(trip_row.distance_nm)
FROM trip_row JOIN boat_row ON trip_row.boat_id = boat_row.id
GROUP BY boat_row.name;
```

- `JOIN`: combine rows of two tables where the keys match
- `GROUP BY` + `SUM`: one result row per boat
- The database does the work – we only get the **answer**

---

# SQL as Strings: Dangerous

```scala
val sql = s"SELECT * FROM boat_row WHERE name = '$name'"
```

- What if `name` is `x' OR '1'='1` ? → **SQL injection**
- Typos in table or column names show up only at **runtime**
- Results come back as untyped rows – we convert them by hand
- Better: let the **compiler** check our queries

---

<!-- _class: kapitel -->

## 5
# ScalaSql

Functional relational mapping

---

# ScalaSql

- Library by Li Haoyi – queries written as **Scala collection operations**
- **Functional relational mapping**: tables are case classes, queries are values
- Type-checked by the compiler, SQL is generated

```scala
//> using dep com.lihaoyi::scalasql:0.3.2
//> using dep org.xerial:sqlite-jdbc:3.53.4.0
```

```scala
"com.lihaoyi" %% "scalasql"    % "0.3.2",
"org.xerial"  %  "sqlite-jdbc" % "3.53.4.0"      // Java library: single %
```

- ScalaSql 0.3.2 needs **Scala 3.6.2 or newer** – fine with 3.9.0

---

# Tables as Case Classes

```scala
case class BoatRow[T[_]](id: T[Int], name: T[String], kind: T[String])
object BoatRow extends Table[BoatRow]

case class TripRow[T[_]](id: T[Int], boatId: T[Int], date: T[String],
                         title: T[String], distanceNm: T[Double])
object TripRow extends Table[TripRow]
```

- `T[_]` is a **higher-kinded type parameter** (generics, Lecture 9/17)
  - in a query: `T` = `Expr` – a column expression
  - in a result: `T` = `Id` – a plain value
- Names are mapped: `TripRow` → `trip_row`, `boatId` → `boat_id`

---

# Connecting

```scala
class SqlRepository(url: String) extends LogbookRepository:
  private val ds = org.sqlite.SQLiteDataSource()
  ds.setUrl(url)
  private val client = DbClient.DataSource(ds, config = new Config {})
  client.transaction(db => Schema.ddl.foreach(db.updateRaw(_)))
```

- `jdbc:sqlite:logbook.db`: JDBC URL – SQLite database in a file
- `client.transaction { db => ... }`: all or nothing
- `updateRaw`: plain SQL for the `CREATE TABLE` statements

---

# Insert

```scala
def addBoat(b: Boat): Unit = client.transaction { db =>
  db.run(BoatRow.insert.columns(_.id := b.id, _.name := b.name, _.kind := b.kind.toString))
}
```

- `BoatRow.insert.columns(...)` builds an `INSERT` statement
- `_.name := b.name`: column gets a value – wrong type → compile error
- Values are passed as **parameters** – no SQL injection possible
- The enum is stored as text: `Dinghy`

---

# Select

```scala
def boats: List[Boat] = client.transaction { db =>
  db.run(BoatRow.select).map(r => Boat(r.id, r.name, BoatKind.valueOf(r.kind))).toList
}
```

```scala
db.run(BoatRow.select.filter(_.kind === "Dinghy").map(_.name))
```

- Looks like collection code (Lecture 12): `select`, `filter`, `map`, `sortBy`
- `===` instead of `==`: compares **in the database**
- Rows (`BoatRow[Id]`) are converted into domain objects (`Boat`)

---

# Reading a Trip with Its Lists

```scala
def trips: List[Trip] = client.transaction { db =>
  db.run(TripRow.select.sortBy(_.id)).map { r =>
    val crew = db.run(CrewRow.select.filter(_.tripId === r.id))
      .map(c => CrewMember(c.name, Role.valueOf(c.role)))
    val track = db.run(PointRow.select.filter(_.tripId === r.id).sortBy(_.idx))
      .map(p => TrackPoint(p.lat, p.lon, Instant.parse(p.time)))
    Trip(r.id, r.boatId, LocalDate.parse(r.date), r.title, crew.toList, track.toList)
  }.toList
}
```

- Three tables → one `Trip` again
- One query per trip: simple, but slow for many trips (the "N+1 problem")

---

# Join and Group By

```scala
override def nmPerBoat: Map[String, Double] = client.transaction { db =>
  db.run(
    TripRow.select
      .join(BoatRow)(_.boatId === _.id)
      .groupBy { case (_, boat) => boat.name } { rows => rows.sumBy(_._1.distanceNm) }
  ).toMap
}
```

- Overrides the default from the trait – now the **database** sums up
- `join` gives pairs `(trip, boat)`, `groupBy` + `sumBy` aggregate

---

# The Generated SQL

```scala
db.renderSql(
  TripRow.select.join(BoatRow)(_.boatId === _.id)
    .groupBy { case (_, boat) => boat.name } { rows => rows.sumBy(_._1.distanceNm) })
```

```sql
SELECT boat_row1.name AS res_0, SUM(trip_row0.distance_nm) AS res_1
FROM trip_row trip_row0
JOIN boat_row boat_row1 ON (trip_row0.boat_id = boat_row1.id)
GROUP BY boat_row1.name
```

- Exactly the SQL we wrote by hand – but checked by the compiler
- `sbt "runMain saillog.showSql"` prints it

---

<!-- _class: kapitel -->

## 6
# Two Implementations, One Program

Swapping the storage

---

# Using the Trait

```scala
def report(repo: LogbookRepository): Unit =
  println(s"  boats: ${repo.boats.map(_.name)}")
  println(s"  trips: ${repo.trips.map(t => s"${t.id} ${t.title} (${t.track.size} pts)")}")
  println(s"  nm per boat: ${repo.nmPerBoat}")
  println(s"  trip 2 crew: ${repo.trip(2).map(_.crew.map(_.name))}")
```

```scala
val repos = List(
  "JSON file" -> JsonFileRepository(os.pwd / "logbook.json"),
  "SQLite"    -> SqlRepository("jdbc:sqlite:logbook.db"))
for (name, repo) <- repos do
  SampleData.fill(repo, data)
  println(name)
  report(repo)
```

---

# Same Answers

```text
JSON file
  boats: List(Pirat, Lacustre)
  nm per boat: Map(Pirat -> 8.786607357403177, Lacustre -> 4.753595337995797)
  trip 2 crew: Some(List(Marko, Anna))
SQLite
  boats: List(Pirat, Lacustre)
  nm per boat: Map(Lacustre -> 4.753595337995797, Pirat -> 8.786607357403177)
  trip 2 crew: Some(List(Marko, Anna))
same trips in both: true
```

- `report` does not know which storage it uses – **polymorphism**
- Comparing both implementations is a cheap but strong **test**

---

# SQL or Documents?

| | Relational (SQLite) | Document (JSON) |
|---|---|---|
| Schema | fixed, checked | free |
| Nested data | split into tables | natural |
| Queries | powerful (`JOIN`, `GROUP BY`) | in your own code |
| Concurrency, transactions | built in | do it yourself |
| Setup | driver, schema | none |

- No winner – it depends on the data and the questions
- The repository trait lets us **postpone** the decision

---

<!-- _class: inhalt -->

<style scoped>
section { font-size: 20px; }
</style>

# Summary

- Files reach their limits: concurrency, crashes, queries
- **Repository pattern**: a trait with domain operations, storage hidden behind it
- Document store: the logbook as one JSON document
- Relational model: tables, primary and foreign keys, normalisation
- SQL: `CREATE`, `INSERT`, `SELECT`, `JOIN`, `GROUP BY` – never build SQL from strings
- **ScalaSql**: tables as case classes `T[_]`, queries as collection operations, SQL generated
- Two implementations, one program – compare them to test

---

<!-- _class: aufgabe -->

# Task

- Check out `v20-db` and run `sbt "runMain saillog.lecture20"`
- Add `nmPerSeason` to the trait with a default implementation; override it in `SqlRepository`
- Write `tripsOfBoat(boatId: Int): List[Trip]` – in SQL with `filter`
- Open `logbook.db` with the `sqlite3` tool and run the `JOIN` query by hand
- Bonus: read all track points with **one** query instead of one per trip

---

<!-- _class: abschluss -->

# Questions?

## Thank you!

marko.boger@htwg-konstanz.de
