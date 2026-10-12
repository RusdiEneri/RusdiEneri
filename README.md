<div align="center">

# Nuruddin Rusydi Ilham
`BACKEND ENGINEERING / NETWORK INFRASTRUCTURE`

Backend Developer & Network Engineer based in Tuban, East Java, Indonesia.<br>
Focused on building high-throughput backend services, optimizing relational databases,<br>
implementing protocol-level tools, and maintaining resilient Linux infrastructure.

<br>

<p>
  <a href="https://www.mangrusdi.my.id/"><img src="https://img.shields.io/badge/Portfolio-mangrusdi.my.id-b38b6d?style=flat-square&logo=googlechrome&logoColor=white" alt="Portfolio" /></a>
  <a href="https://github.com/RusdiEneri"><img src="https://img.shields.io/badge/GitHub-RusdiEneri-181818?style=flat-square&logo=github&logoColor=white" alt="GitHub" /></a>
  <a href="https://www.linkedin.com/in/rusdieneri"><img src="https://img.shields.io/badge/LinkedIn-rusdieneri-0077b5?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
  <a href="mailto:nuruddinrusydiilham@gmail.com"><img src="https://img.shields.io/badge/Email-Contact%20Direct-ea4335?style=flat-square&logo=gmail&logoColor=white" alt="Email" /></a>
  <a href="./README.id.md"><img src="https://img.shields.io/badge/Language-Bahasa%20Indonesia-262626?style=flat-square" alt="Bahasa Indonesia" /></a>
</p>

</div>

---

### ⚡ Telemetry & Activity

<div align="center">

<!-- Real-time Streak & Velocity Stats -->
<img src="./dist/stats.svg?v=1791787879" width="840" style="max-width: 100%;" alt="Rusdi's GitHub Telemetry & Stats" />

<br>
<br>

<!-- Annual Contribution Matrix in Signature Taupe Theme -->
<img src="./dist/contrib-heatmap.svg?v=1791787879" width="840" style="max-width: 100%;" alt="Rusdi's GitHub Contribution Heatmap" />

<br>
<br>

<!-- Developer Identity & System Architecture Specs -->
<img src="./dist/sys-info.svg?v=1791787879" width="840" style="max-width: 100%;" alt="System Architecture & Host Specs" />

</div>

---

### 🚀 Selected Work

<div align="center">
  <a href="https://github.com/RusdiEneri/wa-full-pfp">
    <img src="./dist/featured-wa-full-pfp.svg?v=1791787879" width="415" style="max-width: 100%;" alt="wa-full-pfp" />
  </a>
  <a href="https://github.com/RusdiEneri/jt-express-scheduling">
    <img src="./dist/featured-jt-scheduling.svg?v=1791787879" width="415" style="max-width: 100%;" alt="J&T Express Shift Optimizer" />
  </a>
  <br>
  <a href="https://github.com/RusdiEneri/Cuanin">
    <img src="./dist/featured-cuanin.svg?v=1791787879" width="415" style="max-width: 100%;" alt="Cuanin Marketplace" />
  </a>
  <a href="https://github.com/RusdiEneri/MahasigMind">
    <img src="./dist/featured-mahasigmind.svg?v=1791787879" width="415" style="max-width: 100%;" alt="MahasigMind" />
  </a>
</div>

<br>

#### wa-full-pfp &bull; Protocol Engineering & Privacy Utility
High-performance web utility that updates WhatsApp profile pictures at full resolution without forced square cropping, preserving original aspect ratios and image fidelity.
* **Technical implementation:** Communicates directly with WhatsApp Web binary protocols using `whatsmeow` in Go. Synchronizes QR-code connection state in real time over secure WebSockets.
* **Privacy architecture:** Enforces zero persistent data retention. Authentication sessions exist strictly in memory with automated session teardown upon task completion.
* **Stack:** Go (Golang), whatsmeow, WebSockets, HTML/CSS
* **Links:** [Repository](https://github.com/RusdiEneri/wa-full-pfp) &bull; [Live Demo](https://ppfull.mangrusdi.my.id)

#### J&T Express Shift Optimizer &bull; Heuristic Search & Operational Optimization
Automated courier scheduling platform built to eliminate shift conflicts and optimize staff allocation under operational constraints.
* **Technical implementation:** Formulates courier shift planning as a constraint satisfaction problem solved via a custom Genetic Algorithm. Employs tournament selection and adaptive crossover operators to achieve solution convergence in under 3 seconds.
* **Operational impact:** Replaces hours of error-prone manual scheduling with automated schedule generation and interactive roster visualization.
* **Stack:** Python, Streamlit, NumPy, Pandas
* **Links:** [Repository](https://github.com/RusdiEneri/jt-express-scheduling)

#### Cuanin &bull; Relational Data Modeling & Multi-Vendor Marketplace
Web-based preloved goods marketplace featuring structured product discovery, active price bargaining workflows, and direct seller dispatch.
* **Technical implementation:** Relies on ACID transaction management and MySQL row-level locking to safeguard inventory consistency during concurrent checkout attempts. Features indexed catalog queries that maintain sub-100ms response times.
* **Architecture:** Modular MVC architecture in Laravel with integrated WhatsApp seller routing and responsive server-rendered views.
* **Stack:** Laravel 12, PHP 8.2, MySQL, Tailwind CSS, Vite
* **Links:** [Repository](https://github.com/RusdiEneri/Cuanin)

#### MahasigMind &bull; Student Mental Health Consultation Platform
Single Page Application providing structured emotional wellbeing tracking, reflective journaling, and student consultation access.
* **Technical implementation:** Built on Inertia.js to achieve SPA client interactivity with React 19 without separate REST serialization overhead. Features multi-tier role-based access control (RBAC) separating counselor, student, and administrator capabilities.
* **Data protection:** Encrypts clinical consultation logs and psychological records at the database tier.
* **Stack:** Laravel 11, React 19, Inertia.js, MySQL, Tailwind CSS
* **Links:** [Repository](https://github.com/RusdiEneri/MahasigMind)

---

### 🛠️ Technical Focus

| Area | Technologies & Disciplines |
| :--- | :--- |
| **Backend Engineering** | Go (Golang), PHP (Laravel 11, Laravel 12), Python, Node.js (Express), RESTful API design, WebSocket protocols |
| **Databases & Storage** | PostgreSQL, MySQL, SQLite, Redis, schema normalization, query indexing, ACID transaction handling |
| **Networking & Systems** | Linux (Debian, Ubuntu), Docker, Nginx reverse proxy, MikroTik RouterOS, DNS sinkholes (AdGuard Home) |
| **Automation & Tooling** | GitHub Actions CI/CD pipelines, Bash shell scripting, PowerShell environment automation |

---

### 📌 Architecture Principles

* **Low Latency First:** Streamlining request lifecycles, eliminating query bottlenecks, and targeting sub-100ms response times.
* **Explicit Protocols:** Communicating directly with raw network layers, binary frames, and protobuf without bloated wrappers.
* **Zero Bloat & High Durability:** Avoiding unnecessary abstraction layers in favor of predictable runtime performance, standard libraries, and clean relational models.

---

### 🔭 Current Focus

* Developing protocol-level network tools and background services in Go.
* Hardening local DNS infrastructure and curating privacy-focused domain filters via [blacklist-hosts](https://github.com/RusdiEneri/blacklist-hosts).
* Automating scheduled operational pipelines and external API telemetry monitors with GitHub Actions.

---

### 📬 Contact & Connect

* **Website:** [mangrusdi.my.id](https://www.mangrusdi.my.id/)
* **GitHub:** [@RusdiEneri](https://github.com/RusdiEneri)
* **LinkedIn:** [in/rusdieneri](https://www.linkedin.com/in/rusdieneri)
* **Email:** [nuruddinrusydiilham@gmail.com](mailto:nuruddinrusydiilham@gmail.com)
* **Location:** Tuban, East Java, Indonesia (UTC+7)
