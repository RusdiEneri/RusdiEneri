# Nuruddin Rusydi Ilham

`BACKEND ENGINEERING / NETWORK INFRASTRUCTURE`

Backend developer and network engineer based in Tuban, East Java, Indonesia. Focused on building high-throughput backend services, optimizing relational databases, implementing protocol-level tools, and maintaining resilient Linux infrastructure.

[Portfolio](https://www.mangrusdi.my.id/) &bull; [GitHub](https://github.com/RusdiEneri) &bull; [LinkedIn](https://www.linkedin.com/in/rusdieneri) &bull; [Email](mailto:nuruddinrusydiilham@gmail.com) &bull; [Bahasa Indonesia](./README.id.md)

---

### Overview

I design and build backend services that prioritize low latency, explicit protocol handling, and verifiable reliability. My work centers on practical software engineering: structuring modular RESTful APIs with PHP (Laravel) and Node.js, engineering protocol-level utilities in Go, and formulating optimization algorithms in Python. I avoid framework bloat and unnecessary abstraction layers in favor of predictable runtime performance and clean data models.

My software development and infrastructure work reinforce each other. Experience managing Linux servers, configuring Nginx reverse proxies, and operating network perimeters informs how I architect applications for production. Whether isolating services inside Docker containers, hardening DNS resolvers against unwanted telemetry, or automating recurring pipelines with GitHub Actions, I build systems designed to operate reliably under real-world conditions.

---

### Selected Work

#### wa-full-pfp &bull; Protocol Engineering & Privacy Utility
A high-performance web tool that updates WhatsApp profile pictures at full resolution without forced square cropping, preserving original aspect ratios and image fidelity.

* **Technical implementation:** Communicates directly with WhatsApp Web binary protocols using the `whatsmeow` library in Go. Synchronizes QR-code connection state in real time over secure WebSockets.
* **Privacy architecture:** Enforces zero persistent data retention. Authentication sessions exist strictly in memory with automated session teardown upon task completion.
* **Stack:** Go (Golang), whatsmeow, WebSockets, HTML/CSS
* **Links:** [Repository](https://github.com/RusdiEneri/wa-full-pfp) &bull; [Live Demo](https://ppfull.mangrusdi.my.id)

#### J&T Express Shift Optimizer &bull; Heuristic Search & Operational Optimization
An automated scheduling platform built to eliminate shift conflicts and optimize staff allocation for logistics hub couriers under regulatory and operational constraints.

* **Technical implementation:** Formulates courier shift planning as a constraint satisfaction problem solved via a custom Genetic Algorithm. Employs tournament selection and adaptive crossover operators to achieve solution convergence in under 3 seconds.
* **Operational impact:** Replaces hours of error-prone manual scheduling with automated schedule generation and interactive roster visualization.
* **Stack:** Python, Streamlit, NumPy, Pandas
* **Links:** [Repository](https://github.com/RusdiEneri/jt-express-scheduling)

#### Cuanin &bull; Relational Data Modeling & Multi-Vendor Marketplace
A web-based preloved goods marketplace featuring structured product discovery, active price bargaining workflows, and direct seller dispatch.

* **Technical implementation:** Relies on ACID transaction management and MySQL row-level locking to safeguard inventory consistency during concurrent checkout attempts. Features indexed catalog queries that maintain sub-100ms response times.
* **Architecture:** Modular MVC architecture in Laravel with integrated WhatsApp seller routing and responsive server-rendered views.
* **Stack:** Laravel 12, PHP 8.2, MySQL, Tailwind CSS, Vite
* **Links:** [Repository](https://github.com/RusdiEneri/Cuanin)

#### MahasigMind &bull; Student Mental Health Consultation Platform
A Single Page Application providing structured emotional wellbeing tracking, reflective journaling, and student consultation access.

* **Technical implementation:** Built on Inertia.js to achieve SPA client interactivity with React 19 without separate REST serialization overhead. Features multi-tier role-based access control (RBAC) separating counselor, student, and administrator capabilities.
* **Data protection:** Encrypts clinical consultation logs and psychological records at the database tier.
* **Stack:** Laravel 11, React 19, Inertia.js, MySQL, Tailwind CSS
* **Links:** [Repository](https://github.com/RusdiEneri/MahasigMind)

---

### Technical Focus

| Area | Technologies & Disciplines |
| :--- | :--- |
| **Backend Engineering** | PHP (Laravel 11, Laravel 12), Go (Golang), Python, Node.js (Express), RESTful API design, WebSocket protocols |
| **Databases & Storage** | PostgreSQL, MySQL, SQLite, Redis, schema normalization, query indexing, ACID transaction handling |
| **Networking & Systems** | Linux (Debian, Ubuntu), Docker, Nginx reverse proxy, MikroTik RouterOS, DNS sinkholes (AdGuard Home) |
| **Automation & Tooling** | GitHub Actions CI/CD pipelines, Bash shell scripting, PowerShell environment automation |

---

### Current Focus

* Developing protocol-level network tools and background services in Go.
* Hardening local DNS infrastructure and curating privacy-focused domain filters via [blacklist-hosts](https://github.com/RusdiEneri/blacklist-hosts).
* Automating scheduled operational pipelines and external API telemetry monitors with GitHub Actions.

---

### Contact

* **Website:** [mangrusdi.my.id](https://www.mangrusdi.my.id/)
* **GitHub:** [github.com/RusdiEneri](https://github.com/RusdiEneri)
* **LinkedIn:** [linkedin.com/in/rusdieneri](https://www.linkedin.com/in/rusdieneri)
* **Email:** [nuruddinrusydiilham@gmail.com](mailto:nuruddinrusydiilham@gmail.com)
* **Location:** Tuban, East Java, Indonesia (UTC+7)
