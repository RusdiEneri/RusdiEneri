# Nuruddin Rusydi Ilham

`REKAYASA BACKEND / INFRASTRUKTUR JARINGAN`

Backend developer dan network engineer yang berbasis di Tuban, Jawa Timur, Indonesia. Berfokus pada pembangunan layanan backend berkecepatan tinggi, optimasi basis data relasional, utilitas tingkat protokol, dan pemeliharaan infrastruktur Linux yang tangguh.

[Portofolio](https://www.mangrusdi.my.id/) &bull; [GitHub](https://github.com/RusdiEneri) &bull; [LinkedIn](https://www.linkedin.com/in/rusdieneri) &bull; [Email](mailto:nuruddinrusydiilham@gmail.com) &bull; [English Version](./README.md)

---

### Gambaran Umum

Saya merancang dan membangun layanan backend dengan memprioritaskan latensi rendah, penanganan protokol biner secara eksplisit, dan keandalan sistem yang dapat diuji. Fokus rekayasa saya berakar pada efisiensi perangkat lunak praktis: menyusun RESTful API modular dengan PHP (Laravel) dan Node.js, merekayasa perkakas level protokol menggunakan Go, serta menyusun algoritma optimasi komputasi dengan Python. Pendekatan ini menghindari ketergantungan berlebih pada abstraksi rumit demi menjaga performa runtime yang stabil dan integritas model data.

Pengembangan perangkat lunak dan rekayasa infrastruktur yang saya jalani saling melengkapi. Pengalaman mengelola server Linux, mengonfigurasi reverse proxy Nginx, dan memelihara perimeter jaringan lokal memberikan panduan konkret dalam merancang arsitektur aplikasi siap produksi. Mulai dari isolasi servis dalam kontainer Docker, pengerasan resolusi DNS lokal dari telemetri yang tidak diinginkan, hingga otomasi pipeline tugas terjadwal melalui GitHub Actions, setiap sistem dibangun untuk beroperasi secara konsisten di bawah beban operasional nyata.

---

### Proyek Pilihan

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

### Fokus Teknis

| Bidang | Teknologi & Disiplin Rekayasa |
| :--- | :--- |
| **Rekayasa Backend** | PHP (Laravel 11, Laravel 12), Go (Golang), Python, Node.js (Express), perancangan RESTful API, protokol WebSocket |
| **Basis Data & Penyimpanan** | PostgreSQL, MySQL, SQLite, Redis, normalisasi skema, indexing query, penanganan transaksi ACID |
| **Jaringan & Sistem Operasi** | Linux (Debian, Ubuntu), Docker, reverse proxy Nginx, MikroTik RouterOS, DNS sinkhole (AdGuard Home) |
| **Otomasi & Perkakas Pengembang** | GitHub Actions CI/CD pipelines, Bash shell scripting, otomasi lingkungan kerja PowerShell |

---

### Eksplorasi Saat Ini

* Mengembangkan perkakas jaringan tingkat protokol dan background services menggunakan bahasa Go.
* Memperkuat pertahanan DNS lokal dan mengurasi blocklist domain pelacak privasi melalui [blacklist-hosts](https://github.com/RusdiEneri/blacklist-hosts).
* Mengotomatisasi pipeline operasional terjadwal dan pemantau telemetri API publik dengan GitHub Actions.

---

### Kontak

* **Situs Web:** [mangrusdi.my.id](https://www.mangrusdi.my.id/)
* **GitHub:** [github.com/RusdiEneri](https://github.com/RusdiEneri)
* **LinkedIn:** [linkedin.com/in/rusdieneri](https://www.linkedin.com/in/rusdieneri)
* **Email:** [nuruddinrusydiilham@gmail.com](mailto:nuruddinrusydiilham@gmail.com)
* **Domisili:** Tuban, Jawa Timur, Indonesia (UTC+7)
