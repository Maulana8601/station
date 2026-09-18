import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
import pymysql
import pymysql.cursors

# ======================================================
# Inisialisasi Aplikasi Flask
# ======================================================
app = Flask(__name__)

# Secret key untuk mengamankan Flask session (keranjang belanja)
app.secret_key = os.environ.get('SECRET_KEY', 'rahasia_ecommerce_flask_2026_devops')

# ======================================================
# Konfigurasi Database MySQL
# ======================================================
# Nilai default diambil dari environment variable jika ada, 
# atau menggunakan nilai default lokal untuk kemudahan pemula.
MYSQL_HOST = os.environ.get('MYSQL_HOST', 'localhost')
MYSQL_USER = os.environ.get('MYSQL_USER', 'root')
MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD', '')
MYSQL_DATABASE = os.environ.get('MYSQL_DATABASE', 'ecommerce_db')
MYSQL_PORT = int(os.environ.get('MYSQL_PORT', 3306))

def get_db_connection():
    """
    Fungsi helper untuk membuka koneksi ke database MySQL.
    Menggunakan pymysql.cursors.DictCursor agar hasil query berupa Python Dictionary.
    """
    return pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQL_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE,
        port=MYSQL_PORT,
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

# ======================================================
# Custom Jinja2 Filters
# ======================================================
@app.template_filter('rupiah')
def format_rupiah(value):
    """Filter Jinja2 untuk mengubah angka menjadi format mata uang Rupiah (contoh: Rp 15.500.000)"""
    try:
        val = float(value)
        return f"Rp {val:,.0f}".replace(",", ".")
    except (ValueError, TypeError):
        return "Rp 0"

@app.template_filter('sum_cart_qty')
def sum_cart_qty(cart_dict):
    """Filter Jinja2 untuk menghitung total jumlah item di keranjang session"""
    if not cart_dict or not isinstance(cart_dict, dict):
        return 0
    return sum(int(qty) for qty in cart_dict.values())


# ======================================================
# Routes Aplikasi
# ======================================================

@app.route('/')
def index():
    """
    1. Halaman Home
    Menampilkan daftar produk dari database MySQL dalam bentuk Card Bootstrap.
    """
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Query aman untuk mengambil semua produk
            cursor.execute("SELECT * FROM products ORDER BY id DESC")
            products = cursor.fetchall()
        conn.close()
    except Exception as e:
        flash(f"Gagal terhubung ke database MySQL: {str(e)}", "danger")
        products = []

    return render_template('index.html', products=products)


@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """
    2. Halaman Detail Produk
    Menampilkan rincian informasi spesifik 1 produk berdasarkan ID.
    """
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Parameterized Query untuk mencegah SQL Injection
            cursor.execute("SELECT * FROM products WHERE id = %s", (product_id,))
            product = cursor.fetchone()
        conn.close()

        if not product:
            flash("Produk tidak ditemukan!", "warning")
            return redirect(url_for('index'))

        return render_template('product_detail.html', product=product)

    except Exception as e:
        flash(f"Terjadi kesalahan database: {str(e)}", "danger")
        return redirect(url_for('index'))


@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    """
    Menambahkan produk ke keranjang belanja (Flask Session).
    """
    product_id = request.form.get('product_id')
    quantity = int(request.form.get('quantity', 1))

    if not product_id:
        flash("Produk tidak valid!", "danger")
        return redirect(url_for('index'))

    # Inisialisasi keranjang di session jika belum ada
    if 'cart' not in session:
        session['cart'] = {}

    cart = session['cart']

    # Tambahkan atau perbarui jumlah produk di keranjang
    product_id_str = str(product_id)
    if product_id_str in cart:
        cart[product_id_str] += quantity
    else:
        cart[product_id_str] = quantity

    session['cart'] = cart
    session.modified = True  # Beritahu Flask bahwa session berubah

    flash("Produk berhasil ditambahkan ke keranjang!", "success")
    return redirect(url_for('cart'))


@app.route('/cart')
def cart():
    """
    3. Halaman Keranjang Belanja
    Menampilkan seluruh item produk yang disimpan di dalam session.
    """
    cart = session.get('cart', {})
    cart_items = []
    grand_total = 0
    total_items = 0

    if cart:
        try:
            conn = get_db_connection()
            with conn.cursor() as cursor:
                # Ambil detail produk berdasarkan ID yang ada di keranjang
                product_ids = list(cart.keys())
                format_strings = ','.join(['%s'] * len(product_ids))
                cursor.execute(f"SELECT * FROM products WHERE id IN ({format_strings})", tuple(product_ids))
                products = cursor.fetchall()
                
                # Buat dictionary produk untuk lookup cepat
                products_dict = {str(p['id']): p for p in products}

                for pid_str, qty in cart.items():
                    if pid_str in products_dict:
                        prod = products_dict[pid_str]
                        subtotal = float(prod['price']) * qty
                        grand_total += subtotal
                        total_items += qty
                        cart_items.append({
                            'product': prod,
                            'quantity': qty,
                            'subtotal': subtotal
                        })
            conn.close()
        except Exception as e:
            flash(f"Gagal memuat keranjang dari database: {str(e)}", "danger")

    return render_template('cart.html', cart_items=cart_items, grand_total=grand_total, total_items=total_items)


@app.route('/cart/update', methods=['POST'])
def update_cart():
    """
    Perbarui jumlah produk di keranjang belanja.
    """
    product_id = str(request.form.get('product_id'))
    quantity = int(request.form.get('quantity', 1))

    if 'cart' in session and product_id in session['cart']:
        if quantity > 0:
            session['cart'][product_id] = quantity
            flash("Jumlah produk berhasil diperbarui.", "success")
        else:
            session['cart'].pop(product_id, None)
            flash("Produk dihapus dari keranjang.", "info")
        
        session.modified = True

    return redirect(url_for('cart'))


@app.route('/cart/delete', methods=['POST'])
def delete_from_cart():
    """
    Menghapus produk tertentu dari keranjang belanja.
    """
    product_id = str(request.form.get('product_id'))

    if 'cart' in session and product_id in session['cart']:
        session['cart'].pop(product_id, None)
        session.modified = True
        flash("Produk berhasil dihapus dari keranjang.", "success")

    return redirect(url_for('cart'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    """
    4. Halaman Checkout Pesanan
    GET : Menampilkan form pemesan dan ringkasan keranjang.
    POST: Menyimpan data pesanan ke database MySQL (tabel orders & order_items).
    """
    cart = session.get('cart', {})
    
    if not cart:
        flash("Keranjang belanja Anda masih kosong!", "warning")
        return redirect(url_for('cart'))

    # Ambil item keranjang dari DB
    cart_items = []
    grand_total = 0

    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            product_ids = list(cart.keys())
            format_strings = ','.join(['%s'] * len(product_ids))
            cursor.execute(f"SELECT * FROM products WHERE id IN ({format_strings})", tuple(product_ids))
            products = cursor.fetchall()
            products_dict = {str(p['id']): p for p in products}

            for pid_str, qty in cart.items():
                if pid_str in products_dict:
                    prod = products_dict[pid_str]
                    subtotal = float(prod['price']) * qty
                    grand_total += subtotal
                    cart_items.append({
                        'product': prod,
                        'quantity': qty,
                        'subtotal': subtotal
                    })

        if request.method == 'POST':
            # Tangkap data form dari pengguna
            customer_name = request.form.get('customer_name')
            customer_email = request.form.get('customer_email')
            customer_phone = request.form.get('customer_phone')
            customer_address = request.form.get('customer_address')

            # Simpan data pesanan utama ke tabel `orders`
            with conn.cursor() as cursor:
                sql_order = """
                    INSERT INTO orders (customer_name, customer_email, customer_phone, customer_address, total_price)
                    VALUES (%s, %s, %s, %s, %s)
                """
                cursor.execute(sql_order, (customer_name, customer_email, customer_phone, customer_address, grand_total))
                order_id = cursor.lastrowid

                # Simpan item-item pesanan ke tabel `order_items`
                sql_item = """
                    INSERT INTO order_items (order_id, product_id, quantity, price)
                    VALUES (%s, %s, %s, %s)
                """
                for item in cart_items:
                    cursor.execute(sql_item, (order_id, item['product']['id'], item['quantity'], item['product']['price']))

            conn.close()

            # Kosongkan keranjang session setelah pesanan dibuat
            session.pop('cart', None)
            session.modified = True

            flash("Pesanan Anda berhasil dibuat!", "success")
            return redirect(url_for('order_success', order_id=order_id))

        conn.close()

    except Exception as e:
        flash(f"Terjadi kesalahan saat memproses checkout: {str(e)}", "danger")
        return redirect(url_for('cart'))

    return render_template('checkout.html', cart_items=cart_items, grand_total=grand_total)


@app.route('/success/<int:order_id>')
def order_success(order_id):
    """
    Halaman konfirmasi pesanan berhasil.
    """
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # Ambil data pesanan utama
            cursor.execute("SELECT * FROM orders WHERE id = %s", (order_id,))
            order = cursor.fetchone()

            if not order:
                flash("Pesanan tidak ditemukan!", "warning")
                conn.close()
                return redirect(url_for('index'))

            # Ambil rincian item pesanan bergabung dengan tabel products
            sql_items = """
                SELECT oi.*, p.name as product_name 
                FROM order_items oi 
                JOIN products p ON oi.product_id = p.id 
                WHERE oi.order_id = %s
            """
            cursor.execute(sql_items, (order_id,))
            order_items = cursor.fetchall()
            
        conn.close()
        return render_template('success.html', order=order, order_items=order_items)

    except Exception as e:
        flash(f"Gagal mengambil detail pesanan: {str(e)}", "danger")
        return redirect(url_for('index'))


# ======================================================
# Main Runner Application
# ======================================================
if __name__ == '__main__':
    # Aplikasi berjalan secara lokal di port 5000
    print("Menjalankan aplikasi Flask E-Commerce di http://localhost:5000 ...")
    app.run(host='0.0.0.0', port=5000, debug=True)
