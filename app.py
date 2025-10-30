from flask import Flask, request, jsonify, session, redirect, url_for, render_template, flash
import mysql.connector
from werkzeug.security import check_password_hash
from datetime import datetime
from config import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

# ================= KONEKSI DATABASE =================
def get_db_connection():
    return mysql.connector.connect(**Config.get_db_config())

# ================= LOGIN =================
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session['username'] = user['username']
            flash('Login berhasil! Selamat datang, ' + user['username'], 'success')
            return redirect(url_for('index'))
        else:
            flash('Username atau password salah!', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

# ================= LOGOUT =================
@app.route('/logout')
def logout():
    session.pop('username', None)
    flash('Anda telah logout.', 'info')
    return redirect(url_for('login'))

# ================= HALAMAN ADMIN =================
@app.route('/')
def index():
    if 'username' not in session:
        flash('Silakan login terlebih dahulu.', 'warning')
        return redirect(url_for('login'))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM keuangan ORDER BY tanggal ASC")
    data = cursor.fetchall()

    cursor.execute("SELECT SUM(masuk) AS total_masuk, SUM(keluar) AS total_keluar FROM keuangan")
    totals = cursor.fetchone()
    total_masuk = totals['total_masuk'] or 0
    total_keluar = totals['total_keluar'] or 0

    cursor.execute("SELECT saldo FROM keuangan ORDER BY id DESC LIMIT 1")
    last_row = cursor.fetchone()
    saldo_akhir = last_row['saldo'] if last_row else 0

    conn.close()

    return render_template(
        'index.html',
        data=data,
        total_masuk=total_masuk,
        total_keluar=total_keluar,
        saldo_akhir=saldo_akhir
    )

# ================= TAMBAH DATA =================
@app.route('/add', methods=['POST'])
def add_data():
    if 'username' not in session:
        flash('Anda harus login terlebih dahulu!', 'error')
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401

    data = request.get_json()
    tanggal = data.get('tanggal')
    keterangan = data.get('keterangan')
    masuk = int(data.get('masuk') or 0)
    keluar = int(data.get('keluar') or 0)

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT saldo FROM keuangan ORDER BY id DESC LIMIT 1")
    last_row = cursor.fetchone()
    saldo_terakhir = last_row['saldo'] if last_row else 0
    saldo_baru = saldo_terakhir + masuk - keluar

    cursor.execute("""
        INSERT INTO keuangan (tanggal, keterangan, masuk, keluar, saldo)
        VALUES (%s, %s, %s, %s, %s)
    """, (tanggal, keterangan, masuk, keluar, saldo_baru))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()

    flash('Data berhasil ditambahkan.', 'success')
    return jsonify({
        'status': 'success',
        'message': 'Data berhasil ditambahkan',
        'record': {
            'id': new_id,
            'tanggal': tanggal,
            'keterangan': keterangan,
            'masuk': masuk,
            'keluar': keluar,
            'saldo': saldo_baru
        }
    })

# ================= HAPUS DATA =================
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if 'username' not in session:
        flash('Anda harus login untuk menghapus data.', 'error')
        return jsonify({'status': 'error', 'message': 'Unauthorized'}), 401

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM keuangan WHERE id = %s", (id,))
    conn.commit()
    conn.close()

    flash('Data berhasil dihapus.', 'success')
    return jsonify({'status': 'success', 'message': 'Data berhasil dihapus'})

# ================= HALAMAN PUBLIK (READ ONLY) =================
@app.route('/laporan')
def laporan_publik():
    """Halaman publik laporan keuangan (tanpa login)."""
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM keuangan ORDER BY tanggal ASC")
    data = cursor.fetchall()

    cursor.execute("SELECT SUM(masuk) AS total_masuk, SUM(keluar) AS total_keluar FROM keuangan")
    totals = cursor.fetchone()
    total_masuk = totals['total_masuk'] or 0
    total_keluar = totals['total_keluar'] or 0

    cursor.execute("SELECT saldo FROM keuangan ORDER BY id DESC LIMIT 1")
    last_row = cursor.fetchone()
    saldo_akhir = last_row['saldo'] if last_row else 0

    conn.close()

    return render_template(
        'laporan_public.html',
        data=data,
        total_masuk=total_masuk,
        total_keluar=total_keluar,
        saldo_akhir=saldo_akhir,
        datetime=datetime
    )

# ================= RUN =================
if __name__ == '__main__':
    app.run(debug=True)
