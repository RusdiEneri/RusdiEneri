<div align="center">

# Nuruddin Rusydi Ilham
`REKAYASA BACKEND / INFRASTRUKTUR JARINGAN`

Backend Developer & Network Engineer yang berbasis di Tuban, Jawa Timur, Indonesia.<br>
Berfokus pada pembangunan layanan backend berkecepatan tinggi, optimasi basis data relasional,<br>
utilitas tingkat protokol, dan pemeliharaan infrastruktur Linux yang tangguh.

<br>

<p>
  <a href="https://www.mangrusdi.my.id/"><img src="https://img.shields.io/badge/Portofolio-mangrusdi.my.id-b38b6d?style=flat-square&logo=googlechrome&logoColor=white" alt="Portofolio" /></a>
  <a href="https://github.com/RusdiEneri"><img src="https://img.shields.io/badge/GitHub-RusdiEneri-181818?style=flat-square&logo=github&logoColor=white" alt="GitHub" /></a>
  <a href="https://www.linkedin.com/in/rusdieneri"><img src="https://img.shields.io/badge/LinkedIn-rusdieneri-0077b5?style=flat-square&logo=linkedin&logoColor=white" alt="LinkedIn" /></a>
  <a href="mailto:nuruddinrusydiilham@gmail.com"><img src="https://img.shields.io/badge/Email-Kontak%20Langsung-ea4335?style=flat-square&logo=gmail&logoColor=white" alt="Email" /></a>
  <a href="./README.md"><img src="https://img.shields.io/badge/Language-English-262626?style=flat-square" alt="English Version" /></a>
</p>

</div>

---

### ⚡ Telemetri & Aktivitas

<div align="center">

<!-- Statistik & Konsistensi Rekayasa -->
<img src="./dist/stats.svg?v=1791787879" width="840" style="max-width: 100%;" alt="Statistik dan Telemetri GitHub Rusdi" />

<br>
<br>

<!-- Matriks Kontribusi Tahunan Tema Warm Taupe -->
<img src="./dist/contrib-heatmap.svg?v=1791787879" width="840" style="max-width: 100%;" alt="Heatmap Kontribusi GitHub Rusdi" />

<br>
<br>

<!-- Identitas Pengembang & Spesifikasi Arsitektur Sistem -->
<img src="./dist/sys-info.svg?v=1791787879" width="840" style="max-width: 100%;" alt="Spesifikasi Arsitektur Sistem dan Host" />

</div>

---

### 🚀 Proyek Pilihan

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

#### wa-full-pfp &bull; Rekayasa Protokol & Utilitas Privasi
Aplikasi web berkinerja tinggi untuk memperbarui foto profil WhatsApp pada resolusi penuh tanpa pemotongan rasio paksa (no-crop), mempertahankan aspek rasio dan ketajaman gambar asli secara instan.
* **Implementasi teknis:** Berkomunikasi langsung dengan protokol biner WhatsApp Web memanfaatkan pustaka `whatsmeow` di Go. Sinkronisasi status tautan QR-code dilakukan secara real-time melalui jalur aman WebSockets.
* **Arsitektur privasi:** Menerapkan prinsip zero persistent data retention. Sesi otentikasi hanya tersimpan sementara di memori dengan mekanisme pembersihan sesi otomatis setelah tugas selesai.
* **Teknologi:** Go (Golang), whatsmeow, WebSockets, HTML/CSS
* **Tautan:** [Repositori](https://github.com/RusdiEneri/wa-full-pfp) &bull; [Demo Langsung](https://ppfull.mangrusdi.my.id)

#### J&T Express Shift Optimizer &bull; Pencarian Heuristik & Optimasi Operasional
Platform otomasi penjadwalan shift kerja kurir untuk mengeliminasi bentrok jadwal dan mengoptimalkan alokasi staf operasional logistik di bawah batasan regulasi shift kerja yang ketat.
* **Implementasi teknis:** Memodelkan masalah penjadwalan shift sebagai constraint satisfaction problem yang diselesaikan melalui Algoritma Genetika kustom. Menerapkan seleksi turnamen dan operator mutasi adaptif untuk mencapai konvergensi solusi dalam waktu di bawah 3 detik.
* **Dampak operasional:** Menggantikan perumusan jadwal manual yang memakan waktu berjam-jam menjadi penjadwalan otomatis yang instan disertai visualisasi matriks rotasi shift.
* **Teknologi:** Python, Streamlit, NumPy, Pandas
* **Tautan:** [Repositori](https://github.com/RusdiEneri/jt-express-scheduling)

#### Cuanin &bull; Pemodelan Data Relasional & Marketplace Multi-Vendor
Platform marketplace web untuk jual-beli barang preloved berkualitas dengan fitur katalog terstruktur, alur negosiasi harga interaktif, dan integrasi pemesanan langsung ke penjual via WhatsApp.
* **Implementasi teknis:** Mengandalkan manajemen transaksi ACID dan mekanisme row-level locking pada MySQL untuk menjaga konsistensi inventaris dari resiko race condition saat proses checkout bersamaan. Kueri katalog terindeks menghasilkan waktu respon di bawah 100 milidetik.
* **Arsitektur:** Pola MVC modular pada Laravel dengan penanganan checkout WhatsApp dan tampilan antarmuka terstruktur.
* **Teknologi:** Laravel 12, PHP 8.2, MySQL, Tailwind CSS, Vite
* **Tautan:** [Repositori](https://github.com/RusdiEneri/Cuanin)

#### MahasigMind &bull; Platform Konsultasi & Pemantauan Kesehatan Mental Mahasiswa
Aplikasi web Single Page Application (SPA) untuk pencatatan kesehatan emosional harian, jurnal reflektif, dan akses konsultasi psikologis bagi mahasiswa.
* **Implementasi teknis:** Dibangun di atas Inertia.js untuk menghadirkan interaktivitas SPA berbasis React 19 tanpa overhead serialisasi REST API terpisah. Dilengkapi sistem otorisasi multi-level (RBAC) yang memisahkan hak akses konselor, mahasiswa, dan administrator.
* **Perlindungan data:** Menerapkan enkripsi pada rekam data psikologis dan catatan konsultasi pada level basis data.
* **Teknologi:** Laravel 11, React 19, Inertia.js, MySQL, Tailwind CSS
* **Tautan:** [Repositori](https://github.com/RusdiEneri/MahasigMind)

---

### 🛠️ Fokus Teknis

| Bidang | Teknologi & Disiplin Rekayasa |
| :--- | :--- |
| **Rekayasa Backend** | Go (Golang), PHP (Laravel 11, Laravel 12), Python, Node.js (Express), perancangan RESTful API, protokol WebSocket |
| **Basis Data & Penyimpanan** | PostgreSQL, MySQL, SQLite, Redis, normalisasi skema, indexing query, penanganan transaksi ACID |
| **Jaringan & Sistem Operasi** | Linux (Debian, Ubuntu), Docker, reverse proxy Nginx, MikroTik RouterOS, DNS sinkhole (AdGuard Home) |
| **Otomasi & Perkakas Pengembang** | GitHub Actions CI/CD pipelines, Bash shell scripting, otomasi lingkungan kerja PowerShell |

---

### 📌 Prinsip Arsitektur

* **Prioritas Latensi Rendah:** Perampingan alur siklus permintaan, eliminasi hambatan kueri, dan target waktu respon di bawah 100ms.
* **Protokol Eksplisit:** Berkomunikasi langsung dengan lapisan jaringan mentah, bingkai data biner, dan protobuf tanpa lapisan abstraksi berlebih.
* **Zero Bloat & Ketahanan Tinggi:** Menghindari dependensi yang tidak esensial demi performa runtime yang dapat diprediksi, pustaka standar, dan model relasional yang bersih.

---

### 🔭 Eksplorasi Saat Ini

* Mengembangkan perkakas jaringan tingkat protokol dan background services menggunakan bahasa Go.
* Memperkuat pertahanan DNS lokal dan mengurasi blocklist domain pelacak privasi melalui [blacklist-hosts](https://github.com/RusdiEneri/blacklist-hosts).
* Mengotomatisasi pipeline operasional terjadwal dan pemantau telemetri API publik dengan GitHub Actions.

---

### 📬 Kontak & Kolaborasi

* **Situs Web:** [mangrusdi.my.id](https://www.mangrusdi.my.id/)
* **GitHub:** [@RusdiEneri](https://github.com/RusdiEneri)
* **LinkedIn:** [in/rusdieneri](https://www.linkedin.com/in/rusdieneri)
* **Email:** [nuruddinrusydiilham@gmail.com](mailto:nuruddinrusydiilham@gmail.com)
* **Domisili:** Tuban, Jawa Timur, Indonesia (UTC+7)
