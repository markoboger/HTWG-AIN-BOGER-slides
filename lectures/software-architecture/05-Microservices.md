---
marp: true
theme: htwg
paginate: true
_paginate: false
footer: "![](../../themes/htwgin40.png)&nbsp;&nbsp;Prof. Dr. Marko Boger"
_footer : ""
---

![bg](../../themes/htwgin-titel.png)

### Prof. Dr. Marko Boger
## Software Architecture 
# Lecture 05: Microservices

From monolith to independently deployable services.

<p class="small">Based on Martin Fowler / James Lewis, Spotify engineering publications, and AWS / Amazon material.</p>


---
# C4 Model, Structurizr

![](assets/L2_SessionRuntime.svg)

---

# SonarQube Analysis
![fit](assets/sonarqube.png)

---

# Learning Goals

By the end of today, students should be able to:

- explain why teams split monoliths into services
- describe the core characteristics of a microservice architecture
- recognize the operational costs that come with distribution
- compare platform support at Spotify and Amazon
- decide when microservices are justified and when they are overkill

---

# From Monolith to Services

<div class="columns">
<div markdown="1">

- a monolith is one deployable unit with one process boundary
- a microservice system is a suite of small, independently deployable services
- the goal is not "small code"
- the goal is better autonomy, deployability, and alignment with business capabilities

**Fowler's key point:** services become explicit boundaries in code, runtime, deployment, and team ownership.

</div>
<div markdown="1">

![w:100%](assets/microservices/fowler-figure-1.png)

</div>
</div>

---

# Why Teams Move Beyond the Monolith

<div class="columns">
<div markdown="1">

- one small change can require rebuilding and redeploying the whole application
- scaling is often coarse-grained: the whole system scales together
- module boundaries tend to erode over time
- large codebases make ownership and reasoning harder

Microservices try to reduce coupling between change cycles.

</div>
<div markdown="1">

![w:100%](assets/microservices/fowler-figure-1.png)

</div>
</div>

---

# Business Capabilities, Not Technology Layers

<div class="columns">
<div markdown="1">

- Fowler argues that service boundaries should follow business capabilities
- this means a team owns UI, logic, data, and operations for its area
- cross-functional teams reduce handovers between "frontend", "backend", and "database" silos

Typical service examples:

- ordering
- catalog
- payment
- recommendation
- notification

</div>
<div markdown="1">

![w:92%](assets/microservices/fowler-figure-2.png)

</div>
</div>

---

# Team Boundaries Reinforce Service Boundaries

<div class="columns">
<div markdown="1">

- Conway's Law matters: organizations design systems that mirror communication structures
- if one team owns one bounded area end-to-end, the architecture tends to become clearer
- this is why microservices are as much an organization design choice as a technical one

Architecture and team topology evolve together.

</div>
<div markdown="1">

![w:100%](assets/microservices/fowler-figure-3.png)

</div>
</div>

---

# Core Characteristics of Microservices

- independently deployable services
- organization around business capability
- smart endpoints and dumb pipes
- decentralized governance
- decentralized data management
- strong infrastructure automation
- explicit design for failure
- evolutionary design instead of big upfront decomposition

Microservices are less a framework and more a bundle of architectural and operational practices.

---

# Smart Endpoints, Dumb Pipes

- put business logic into the services, not into a central integration monster
- prefer simple communication styles:
  - HTTP APIs
  - asynchronous messaging
  - coarse-grained contracts
- avoid recreating a distributed monolith through chatty RPC calls

Good question for every API call:

**Is this a real service boundary, or did we just move in-process method calls over the network?**

---

# Each Service Owns Its Data

<div class="columns">
<div markdown="1">

- Fowler highlights decentralized data management as a major shift
- each service may own its own schema and even its own database technology
- this supports autonomy, but makes reporting and consistency harder

Consequences:

- no giant shared database as the integration hub
- more duplication of reference data
- eventual consistency becomes normal
- compensating actions become part of the design

</div>
<div markdown="1">

![w:100%](assets/microservices/fowler-figure-4.png)

</div>
</div>

---

# Infrastructure Automation Is Not Optional

<div class="columns">
<div markdown="1">

- a monolith can survive with a mediocre deployment process
- dozens of services cannot
- microservices require automation in:
  - build
  - test
  - deployment
  - provisioning
  - monitoring
  - rollback

Without platform support, teams drown in operational complexity.

</div>
<div markdown="1">

![w:100%](assets/microservices/fowler-figure-5.png)

</div>
</div>

---

# Operating Many Services Changes Everything

<div class="columns">
<div markdown="1">

- deployment topologies become more complex
- local debugging gets harder
- observability becomes a first-class requirement
- resilience patterns matter:
  - timeouts
  - retries
  - circuit breakers
  - bulkheads

Distributed systems fail in partial and surprising ways.

</div>
<div markdown="1">

![w:100%](assets/microservices/fowler-figure-6.png)

</div>
</div>

---

# The Hidden Costs

- network latency replaces local method calls
- failures become partial, asynchronous, and harder to reproduce
- testing needs contract, integration, and end-to-end layers
- data consistency becomes a business decision, not just a database setting
- developers need platform, logging, tracing, and deployment literacy

Microservices buy team autonomy by increasing system complexity.

---

# Spotify Example: Platform First

- Spotify built Backstage as an internal developer portal to reduce infrastructure fragmentation
- Backstage gives engineers one place to find service ownership, APIs, docs, templates, and tooling
- Spotify describes it as a central software catalog and abstraction layer over infrastructure
- published Spotify material highlights service discovery, software templates, documentation, and plugin-based workflows in one portal

Why this matters:

- microservices multiply cognitive load
- platform engineering is how large organizations keep service sprawl manageable

---

# Spotify Infrastructure Lessons

- self-service service creation matters
- ownership metadata matters
- discoverability matters
- a plugin platform matters because one tool never covers everything

Published Spotify examples emphasize:

- automated templates for creating new services
- a centralized catalog of software components and APIs
- TechDocs and catalog metadata to make ownership explicit
- a common developer portal instead of tribal knowledge

For us, the lesson is simple:

**Microservices scale better when platform capabilities scale first.**

---

# Amazon Example: Services and Two-Pizza Teams

- Amazon describes a move from tightly coupled systems toward a vast network of standalone services
- their organizational counterpart was the two-pizza team: small autonomous teams with end-to-end ownership
- each team focuses on a single service or offering, stays close to customers, and owns operations as well as delivery
- AWS material connects this directly to speed, agility, and experimentation

Architecture decision:

- split systems so that teams can move independently

Organization decision:

- give those teams single-threaded ownership

---

# Amazon Infrastructure Lessons

- "you build it, you run it" requires strong operational engineering
- Amazon's Builders' Library highlights practices for large-scale operation:
  - very high deployment automation
  - resilience patterns such as shuffle sharding
  - fault isolation
  - gradual rollout
  - deep metrics and observability

Amazon has publicly described software delivery at a scale of more than 150 million deployments per year across Amazon builders.

Microservices were not the whole answer at Amazon.

They were paired with:

- autonomous teams
- engineering guardrails
- operational excellence
- strong internal platforms

---

# Netflix Example: Simian Army

<div class="columns">
<div markdown="1">

- Netflix used the **Simian Army** as a family of automated tools for testing resilience, security, and operational discipline
- each "monkey" attacks a different weakness in a distributed system
- the goal is not chaos for its own sake
- the goal is to expose fragile assumptions before real incidents do

Why this matters for microservices:

- many services depend on networks, instances, regions, and cloud policies
- resilience has to be exercised continuously, not only described in diagrams
- architecture quality shows up when the system is stressed

</div>
<div markdown="1">

![w:100%](assets/simian-army/simian-army-family.webp)

</div>
</div>

---

# Chaos Monkey

<div class="columns">
<div markdown="1">

- **Purpose:** randomly shut down production instances
- this teaches teams to expect machine failure as a normal event
- services must recover through redundancy, health checks, and automatic replacement

Teaching point:

- if one server disappears and the service collapses, the architecture was not resilient enough

</div>
<div markdown="1">

![w:78%](assets/simian-army/chaos-monkey.webp)

</div>
</div>

---

# Janitor Monkey

<div class="columns">
<div markdown="1">

- **Purpose:** identify and remove unused cloud resources
- examples include stale snapshots, unattached volumes, and other abandoned infrastructure
- this reduces waste, cost, and confusion in large cloud environments

Operational lesson:

- good architecture includes cleanup discipline, not only service design

</div>
<div markdown="1">

![w:82%](assets/simian-army/janitor-monkey.png)

</div>
</div>

---

# Conformity Monkey

<div class="columns">
<div markdown="1">

- **Purpose:** find instances that do not follow engineering standards
- examples include wrong instance types, missing metadata, or configurations that violate best practices
- this helps teams stay autonomous without abandoning shared rules

Architectural lesson:

- autonomy works better when standards are checked automatically

</div>
<div markdown="1">

![w:82%](assets/simian-army/conformity-monkey.webp)

</div>
</div>

---

# Doctor Monkey

<div class="columns">
<div markdown="1">

- **Purpose:** detect unhealthy instances and take action before they cause bigger failures
- signals can include failed health checks, bad metrics, or repeated unhealthy behavior
- the idea is to treat unhealthy nodes as replaceable, not precious

Microservice lesson:

- fast recovery is usually better than manual rescue of every single machine

</div>
<div markdown="1">

![w:78%](assets/simian-army/doctor-monkey.webp)

</div>
</div>

---

# Security Monkey

<div class="columns">
<div markdown="1">

- **Purpose:** detect security violations and dangerous cloud configurations
- examples include overly open firewall rules, weak IAM policies, and exposed resources
- security becomes a continuous automated check instead of an occasional review

Architectural lesson:

- in microservice systems, security has to scale with platform automation

</div>
<div markdown="1">

![w:78%](assets/simian-army/security-monkey.webp)

</div>
</div>

---

# Latency Monkey

<div class="columns">
<div markdown="1">

- **Purpose:** simulate slow networks and delayed service responses
- this tests timeouts, retries, fallbacks, and graceful degradation
- many production incidents begin with slowness before they become full outages

Microservice lesson:

- strong service design handles slow dependencies, not only dead ones

</div>
<div markdown="1">

![w:82%](assets/simian-army/latency-monkey.webp)

</div>
</div>

---

# Chaos Gorilla

<div class="columns">
<div markdown="1">

- **Purpose:** simulate the failure of an entire availability zone
- this is much more severe than losing a single instance
- services must keep working by shifting traffic and capacity to healthy zones

Microservice lesson:

- resilience must be designed at the infrastructure level, not just inside one service

</div>
<div markdown="1">

![w:78%](assets/simian-army/chaos-gorilla.webp)

</div>
</div>

---

# Chaos Kong

<div class="columns">
<div markdown="1">

- **Purpose:** simulate the loss of an entire cloud region
- this forces teams to think about disaster recovery, replication, and multi-region failover
- it is a much more demanding resilience test than zone-level failure

Architectural lesson:

- true resilience is proven when a whole region can disappear and the business still operates

</div>
<div markdown="1">

![w:78%](assets/simian-army/chaos-kong.webp)

</div>
</div>

---

# Published Snapshots: Spotify vs. Netflix

- these numbers are **published snapshots**, not live dashboards
- they come from different years, because the companies do not disclose the same metrics at the same time

| Metric | Spotify | Netflix |
| --- | --- | --- |
| Teams | **280+ engineering teams**  | **~30 engineering teams**  |
| Team size | **6-12 people** | |
| Team locations | **50+ squads across 4 cities**  | **U.S. and Poland** |
| Services total | **2,000+ backend services**  | **>500 microservices**  |
| Services per team |  **7 backend services per team** | **16+ microservices per team** |

Takeaway:


<p class="small">Sources: Backstage announcement (March 16, 2020), Spotify engineering culture snapshot (2014), Netflix QCon San Francisco talk by Sudhir Tonse / Nitesh Kant (2014), Netflix careers / office pages, and Netflix Poland engineering hub announcement (January 10, 2023).</p>

---

# When Microservices Make Sense

- multiple teams need to deliver independently
- different parts of the system scale differently
- domains are clear enough to separate responsibly
- deployment frequency is high
- the organization can invest in platform engineering and observability

Good fit:

- large products
- long-lived systems
- organizations with multiple product teams

---

# When a Monolith Is Better

- the product is early and still searching for its domain boundaries
- one team can still understand the whole system
- operations capacity is limited
- deployment is infrequent
- transactional consistency is more important than independent releases

Rule of thumb:

**A well-structured monolith is often the right starting point.**

---

# Migration Guidance

1. start from business capabilities, not from classes or packages
2. improve modularity inside the monolith first
3. extract only where a boundary is already painful and clear
4. automate build, test, deploy, logging, and tracing before large-scale extraction
5. keep service interfaces coarse-grained
6. expect organizational change, not just code movement

Microservices are a socio-technical refactoring.

---

# Takeaways

- microservices are about independent deployability and bounded ownership
- team structure and system structure shape each other
- decentralized data and automation are core parts of the model
- Spotify shows the value of internal platform tooling
- Amazon shows the value of small autonomous teams plus operational discipline
- use microservices when the benefits of autonomy outweigh the cost of distribution

---

# Sources

- Martin Fowler / James Lewis: <https://martinfowler.com/articles/microservices.html>
- Spotify Engineering, "How We Use Backstage at Spotify": <https://engineering.atspotify.com/2020/04/how-we-use-backstage-at-spotify>
- Spotify Engineering, "Supercharged Developer Portals": <https://engineering.atspotify.com/2024/04/supercharged-developer-portals/>
- Backstage docs, "The Spotify Story": <https://backstage.io/docs/overview/background>
- AWS Executive Insights, "Amazon's Two Pizza Teams": <https://aws.amazon.com/executive-insights/content/amazon-two-pizza-team/>
- AWS, "The Amazon Builders' Library": <https://aws.amazon.com/builders-library/>
