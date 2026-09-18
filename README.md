# TechStore - Python Flask E-Commerce

Aplikasi e-commerce sederhana berbasis **Python Flask**, **MySQL**, dan **Bootstrap 5**. Project ini dirancang untuk pembelajaran Python Flask dasar dan sebagai fondasi aplikasi yang nantinya akan dikembangkan bertahap untuk latihan **DevOps**.

---

## 📌 Fitur Utama Aplikasi

1. **Halaman Beranda (Home)**
   - Menampilkan katalog produk dalam bentuk Card Bootstrap 5.
   - Dilengkapi gambar produk, nama, deskripsi singkat, harga terformat (Rupiah), tombol *Lihat Detail*, dan tombol *Tambah ke Keranjang*.
   - Navbar responsif dengan counter badge keranjang interaktif.

2. **Halaman Detail Produk**
   - Rincian informasi spesifik produk.
   - Pilihan jumlah (kuantitas) barang yang ingin dibeli.
   - Tombol *Tambah ke Keranjang* dan tombol *Kembali*.

3. **Keranjang Belanja (Shopping Cart)**
   - Menyimpan item pilihan pengguna menggunakan **Flask Session**.
   - Menampilkan tabel daftar produk, harga, kuantitas yang bisa diubah, subtotal, dan tombol hapus produk.
   - Ringkasan total pembayaran dan tombol lanjut ke *Checkout*.

4. **Checkout & Konfirmasi Pesanan**
   - Form isian data pemesan (Nama Lengkap, Email, Nomor Telepon, Alamat Pengiriman).
   - Ringkasan pesanan lengkap.
   - Menyimpan data transaksi secara otomatis ke database MySQL (tabel `orders` dan `order_items`).
   - Halaman konfirmasi pesanan dengan ID Pesanan unik setelah transaksi berhasil.

---

## 🛠️ Teknologi yang Digunakan

* **Backend**: Python 3, Flask
* **Database**: MySQL (`PyMySQL` connector)
* **Frontend**: HTML5, Jinja2 Template Engine, Bootstrap 5 (CDN)
* **Styling**: Custom CSS (`static/css/style.css`), FontAwesome Icons

---

## 📂 Struktur Project

```text
station/
├── app.py                  # Aplikasi utama Flask (routing, koneksi database, session cart)
├── database.sql            # Script SQL pembuatan database `ecommerce_db`, tabel, & data produk contoh
├── requirements.txt        # Daftar dependency modul Python (Flask, PyMySQL)
├── READ.md                 # Dokumentasi lengkap project & panduan penggunaan
├── README.md               # Salinan standar markdown repository
├── static/
│   └── css/
│       └── style.css       # Custom stylesheet modern (cards, hover effects, rupiah tags)
└── templates/
    ├── base.html           # Master layout Bootstrap 5 (Navbar, Flash Messages, Footer)
    ├── index.html          # Halaman katalog produk beranda
    ├── product_detail.html # Halaman rincian produk
    ├── cart.html           # Halaman keranjang belanja
    ├── checkout.html       # Form pemesan & ringkasan pesanan
    └── success.html        # Halaman konfirmasi pesanan berhasil
```

---

## 🗄️ Skema Database (`database.sql`)

Database yang digunakan bernama `ecommerce_db` dengan struktur tabel sebagai berikut:

* **`products`**: `id`, `name`, `description`, `price`, `image`, `created_at`
* **`orders`**: `id`, `customer_name`, `customer_email`, `customer_phone`, `customer_address`, `total_price`, `created_at`
* **`order_items`**: `id`, `order_id` (FK -> `orders.id`), `product_id` (FK -> `products.id`), `quantity`, `price`

---

## 🚀 Cara Menjalankan & Mengakses Website

### 1. Install Dependency
Buka terminal pada folder project ini, lalu jalankan perintah:

```bash
pip3 install -r requirements.txt
```

### 2. Impor Database MySQL
Pastikan layanan (service) MySQL di komputer Anda telah berjalan. Impor file `database.sql` ke MySQL:

```bash
mysql -u root -p < database.sql
```
*(Masukkan password root MySQL Anda saat diminta. Jika tanpa password, cukup tekan Enter)*

### 3. Pengaturan Konfigurasi MySQL (Opsional)
Secara default, aplikasi mencoba terhubung ke `localhost` dengan user `root` dan password kosong. Jika MySQL Anda menggunakan password, atur via Environment Variable di terminal:

```bash
export MYSQL_HOST="localhost"
export MYSQL_USER="root"
export MYSQL_PASSWORD="password_mysql_anda"
export MYSQL_DATABASE="ecommerce_db"
```

### 4. Jalankan Aplikasi Flask
Jalankan file `app.py`:

```bash
python3 app.py
```

Terminal akan menampilkan log:
```text
Menjalankan aplikasi Flask E-Commerce di http://localhost:5000 ...
 * Serving Flask app 'app'
 * Debug mode: on
 * Running on http://127.0.0.1:5000
```

### 5. Akses Melalui Browser
Buka browser favorit Anda dan akses URL berikut:
👉 **[http://localhost:5000](http://localhost:5000)**

---

## 📄 Penjelasan Fungsi Setiap File

* **`app.py`**: Berisi seluruh logika Flask server, pendaftaran rute HTTP, parameterized query SQL yang aman, penanganan session keranjang belanja, serta custom Jinja filter `rupiah` dan `sum_cart_qty`.
* **`database.sql`**: Mengatur pembuatan database `ecommerce_db`, penentuan relasi Foreign Key antar tabel, dan penyediaan 6 data contoh produk awal.
* **`requirements.txt`**: File dependensi minimal yang dibutuhkan aplikasi (`Flask` dan `PyMySQL`).
* **`static/css/style.css`**: File stylesheet CSS untuk mempercantik komponen Bootstrap 5.
* **`templates/base.html`**: Layout dasar (induk) yang membungkus navbar, area pesan notifikasi (flash messages), serta footer.
* **`templates/index.html`**: Halaman utama katalog produk.
* **`templates/product_detail.html`**: Halaman rincian spesifikasi produk.
* **`templates/cart.html`**: Halaman pengelola keranjang belanja.
* **`templates/checkout.html`**: Form pengisian data pemesan.
* **`templates/success.html`**: Halaman bukti/konfirmasi pesanan berhasil.
