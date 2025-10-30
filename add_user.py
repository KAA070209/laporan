import mysql.connector
from werkzeug.security import generate_password_hash
from config import Config

def get_db_connection():
    return mysql.connector.connect(**Config.get_db_config())

def add_user():
    print("=== Tambah User Baru ===")
    username = input("Masukkan username: ").strip()
    password = input("Masukkan password: ").strip()
    nama = input("Masukkan nama lengkap: ").strip()
    role = input("Masukkan role (admin/user) [default=user]: ").strip() or "user"

    hashed_password = generate_password_hash(password)

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (username, password, nama_lengkap, role)
            VALUES (%s, %s, %s, %s)
        """, (username, hashed_password, nama, role))
        conn.commit()

        print(f"✅ User '{username}' berhasil ditambahkan dengan role '{role}'.")
    except mysql.connector.Error as err:
        print("❌ Gagal menambahkan user:", err)
    finally:
        conn.close()

if __name__ == "__main__":
    add_user()
