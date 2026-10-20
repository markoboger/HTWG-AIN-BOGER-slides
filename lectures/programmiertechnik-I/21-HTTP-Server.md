---
marp: true
theme: htwg-pt1
paginate: true
footer: "![](../../themes/htwgin40.png)&nbsp;&nbsp;Prof. Dr. Marko Boger, Prof. Dr. Pascal Laube"
_footer: ""
---

![bg](../../themes/htwgin-titel.png)

### Prof. Dr. Marko Boger, Prof. Dr. Pascal Laube
## Programmiertechnik I
# Lecture 21: HTTP Server

<p class="small">Running example: saillog · git tag <code>v21-http</code> · branch <code>feature/21-http</code></p>

---

<!-- _class: inhalt -->

<style scoped>
section { font-size: 20px; }
</style>

# Goals

In this lecture you will learn

- how the **web** works: client, server, request, response
- the parts of **HTTP**: method, path, query, headers, body, status code
- what a **REST API** is and how to design one
- how to write an HTTP server in Scala with **Cask**
- how to return **JSON** and proper **status codes**
- how to **upload** a GPS track to the server
- how to test a server with **curl**

---

<!-- _class: kapitel -->

## 1
# How the Web Works

Clients, servers and HTTP

---

# Client and Server

- The logbook so far runs on **one** computer
- The crew wants to see trips on their **phones** and upload tracks
- → a **server** that keeps the data, **clients** that ask for it

```text
  phone / browser / curl                      saillog server
  ───────────────────────    request  ──▶    ─────────────────
                             ◀── response      LogbookRepository
                                               logbook.db
```

- The language they speak: **HTTP** (Hypertext Transfer Protocol)

---

# An HTTP Request

```text
POST /api/trips?boat=2&title=Upload&date=2026-09-20 HTTP/1.1
Host: localhost:8080
Content-Type: application/x-www-form-urlencoded
Content-Length: 515

<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" ...
```

- **Method**: what to do – `GET`, `POST`, `PUT`, `DELETE`
- **Path**: which resource – `/api/trips`
- **Query**: parameters after `?` – `boat=2&title=Upload`
- **Headers**: metadata, then an empty line, then the **body**

---

# An HTTP Response

```text
HTTP/1.1 201 Created
Content-Type: application/json
Content-Length: 42

{"id":4,"points":4,"nm":4.393303678701589}
```

| Code | Meaning |
|---|---|
| `200 OK` | here is what you asked for |
| `201 Created` | a new resource was created |
| `301` / `303` | look somewhere else (redirect) |
| `404 Not Found` | no such resource |
| `500 Internal Server Error` | the server failed |

---

# HTTP Methods

| Method | Meaning | Safe? | Body? |
|---|---|---|---|
| `GET` | read a resource | yes | no |
| `POST` | create something / send data | no | yes |
| `PUT` | replace a resource | no | yes |
| `DELETE` | remove a resource | no | no |

- **Safe**: does not change anything on the server
- Browsers send `GET` when you open a link and `POST` for most forms
- `GET` requests may be repeated, cached, bookmarked

---

# URLs, Hosts and Ports

```text
http://localhost:8080/api/trips?season=2026
└┬─┘   └───┬───┘ └┬─┘└────┬───┘ └────┬────┘
scheme    host   port    path       query
```

- **host**: which computer – `localhost` is your own machine
- **port**: which program on that computer – our server listens on **8080**
- Port 80 (`http`) and 443 (`https`) are the defaults browsers use
- `https`: the same HTTP, but encrypted (TLS)

---

<!-- _class: kapitel -->

## 2
# REST

Resources and URLs

---

# REST: Resources

- **REST** (Representational State Transfer): a style for web APIs
- Everything is a **resource** with a **URL**; the method says what to do
- Representation: usually **JSON**

| Request | Meaning |
|---|---|
| `GET /api/boats` | all boats |
| `GET /api/trips` | all trips |
| `GET /api/trips?season=2026` | trips of one season |
| `GET /api/trips/2` | one trip |
| `POST /api/trips?boat=..&title=..&date=..` | upload a track, create a trip |
| `GET /api/stats/nm-per-boat` | statistics |

---

# Designing URLs

- **Nouns**, not verbs: `/api/trips`, not `/api/getTrips`
- **Plural** for collections, an id for one element: `/api/trips/2`
- **Query parameters** for filters: `?season=2026`
- `/api` prefix: separates machine-readable JSON from the HTML pages (Lecture 22)
- The **status code** carries the outcome – not a field in the JSON

---

<!-- _class: kapitel -->

## 3
# Cask

A simple HTTP server for Scala

---

# Cask

- Micro web framework by Li Haoyi – same family as os-lib, uPickle, ScalaSql
- Inspired by Python's Flask: a route is an **annotated method**
- Runs on Undertow, a fast Java web server

```scala
//> using dep com.lihaoyi::cask:0.11.3
```

```scala
"com.lihaoyi" %% "cask" % "0.11.3"     // build.sbt
```

---

# Hello, Cask

```scala
//> using scala 3.9.0
//> using dep com.lihaoyi::cask:0.11.3

object Hello extends cask.MainRoutes:
  @cask.get("/")
  def hello() = "Hello, sailors!"

  @cask.get("/greet/:name")
  def greet(name: String) = s"Ahoy, $name!"

  initialize()
```

- `MainRoutes` provides a `main` method that starts the server on port **8080**
- `:name` in the path becomes a method **parameter**
- `initialize()` registers all annotated routes

---

# The saillog Server

```scala
object LogbookServer extends cask.MainRoutes:
  override def host = "0.0.0.0"
  override def port = 8080

  val repo: LogbookRepository = SqlRepository("jdbc:sqlite:logbook.db")
  if repo.boats.isEmpty then SampleData.fill(repo, os.pwd / "data")

  def json[T: Writer](value: T, status: Int = 200) =
    cask.Response(writeJs(value), statusCode = status)
```

- The server uses the **trait** – swap in `JsonFileRepository` and nothing else changes
- `json` helper: any value with a uPickle `Writer` → JSON response with a status
- `0.0.0.0`: reachable from other devices in the network, not only localhost

---

# GET Routes

```scala
@cask.get("/api/boats")
def boats() = json(repo.boats)

@cask.get("/api/trips")
def trips(season: Option[Int] = None) =
  json(repo.trips.filter(t => season.forall(_ == t.date.getYear)))
```

- Method parameters not in the path are **query parameters**
- `Option[Int] = None`: optional – `/api/trips` and `/api/trips?season=2026` both work
- Cask converts `"2026"` to `Int` – or answers `400 Bad Request`

---

# Not Found: 404

```scala
@cask.get("/api/trips/:id")
def trip(id: Int) = repo.trip(id) match
  case Some(t) => json(t)
  case None    => json(ujson.Obj("error" -> s"no trip $id"), 404)
```

```text
$ curl -i localhost:8080/api/trips/99
HTTP/1.1 404 Not Found
{"error":"no trip 99"}
```

- `Option` from the repository → status code in HTTP
- `ujson.Obj`: build JSON directly, without a case class

---

# Upload: POST with a Body

```scala
@cask.post("/api/trips")
def upload(boat: Int, title: String, date: String, format: String = "gpx",
           request: cask.Request) =
  val text = request.text()
  val track = if format == "csv" then Csv.parse(text.linesIterator.toSeq)
              else Gpx.parse(text)
  val trip = Trip(repo.nextTripId, boat, LocalDate.parse(date), title, Nil, track)
  repo.addTrip(trip)
  json(ujson.Obj("id" -> trip.id, "points" -> track.size,
                 "nm" -> Geo.distanceNm(track)), 201)
```

- `request: cask.Request` gives access to the raw body
- Parsers from Lecture 19, repository from Lecture 20 – **reused**, not rewritten

---

# Statistics

```scala
@cask.get("/api/stats/nm-per-boat")
def nmPerBoat() = json(repo.nmPerBoat)

initialize()
```

```text
$ curl localhost:8080/api/stats/nm-per-boat
{"Dock":13.540202695398975,"X99 Expresso":9.146899016697386}
```

- With SQLite behind it, the `JOIN … GROUP BY` from Lecture 20 runs in the database
- `Map[String, Double]` becomes a JSON object automatically

---

# JSON over HTTP

```text
$ curl -i localhost:8080/api/boats
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 92

[{"id":1,"name":"Dock","kind":"Motorboat"},{"id":2,"name":"X99 Expresso","kind":"Keelboat"}]
```

- `writeJs` produces a `ujson.Value` – Cask sends it with `Content-Type: application/json`
- The **same** `derives ReadWriter` as for the file in Lecture 19
- Any client – JavaScript, Python, a phone app – can read it

---

<!-- _class: kapitel -->

## 4
# Testing with curl

The command line HTTP client

---

# Starting the Server

```bash
git checkout v21-http
sbt "runMain saillog.web.LogbookServer"
```

- The server keeps running – stop it with `Ctrl+C`
- Open `http://localhost:8080/api/boats` in the browser: you see JSON
- For `POST` and headers we need a better client: **curl**
- Alternatives: the REST Client extension in VS Code, Postman, Bruno

---

# curl: GET

```text
$ curl localhost:8080/api/boats
[{"id":1,"name":"Dock","kind":"Motorboat"},{"id":2,"name":"X99 Expresso","kind":"Keelboat"}]

$ curl "localhost:8080/api/trips?season=2026"
[{"id":2,"boatId":2,"date":"2026-07-02","title":"Evening round","crew":[...
```

- `curl URL` sends a `GET` and prints the body
- `-i` shows status line and headers as well
- Quote URLs with `?` and `&` – otherwise the shell interprets them

---

# curl: Uploading a Track

```text
$ curl -X POST --data-binary @data/konstanz-meersburg.gpx \
    "localhost:8080/api/trips?boat=2&title=Upload&date=2026-09-20"
{"id":4,"points":4,"nm":4.393303678701589}

$ curl -X POST --data-binary @data/abendrunde.csv \
    "localhost:8080/api/trips?boat=1&title=CSV&date=2026-09-21&format=csv"
{"id":5,"points":3,"nm":4.753595337995797}
```

- `--data-binary @file`: send the file unchanged as the body
- The new trips appear in `GET /api/trips` – and in `logbook.db`

---

# What Can Go Wrong?

- Broken GPX (`kaputt.gpx`) → exception in `Gpx.parse` → **500**
  - better: `Gpx.read`-style `Try`, answer **400 Bad Request** with a message
- Unknown boat id → trip is stored anyway
  - better: check `repo.boat(boat)` first
- Missing parameter → Cask answers **400** by itself
- Logging every request helps to find problems (Lecture 16)

---

# Architecture at `v21-http`

```text
src/main/scala/saillog/
  model/  Model, Geo, Stats                    Lecture 19
  io/     Gpx, Csv, Json                       Lecture 19
  repo/   LogbookRepository, JsonFile…, Sql…   Lecture 20
  web/    LogbookServer                        Lecture 21
```

- Each layer only uses the layers **below** it
- The web layer is thin: parse the request, call the repository, write JSON
- Next: JSON is for programs – people want **pages**

---

<!-- _class: inhalt -->

<style scoped>
section { font-size: 20px; }
</style>

# Summary

- HTTP: request (method, path, query, headers, body) and response (status, headers, body)
- Status codes: `200`, `201`, `404`, `400`, `500`
- REST: resources with URLs, nouns and plurals, the method says what to do
- Cask: `object … extends cask.MainRoutes`, `@cask.get`, `@cask.post`, `initialize()`
- Path parameters `:id`, query parameters as method parameters, `Option` for optional ones
- JSON responses with uPickle, status codes with `cask.Response`
- Upload: raw body with `request.text()`, parsed by our Lecture 19 code
- Test with **curl**: `-i`, `-X POST`, `--data-binary @file`

---

<!-- _class: aufgabe -->

# Task

- Check out `v21-http`, start the server and try all curl commands of this lecture
- Add `GET /api/stats/nm-per-season`
- Make the upload answer `400` with an error message for broken files
- Add `GET /api/boats/:id` with a proper `404`
- Bonus: upload a track from your phone (same Wi-Fi, use the computer's IP address)

---

<!-- _class: abschluss -->

# Questions?

## Thank you!

marko.boger@htwg-konstanz.de
