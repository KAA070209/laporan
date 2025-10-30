import os
from dotenv import load_dotenv

load_dotenv()

class Config:

    # Secret key untuk session Flask
    SECRET_KEY = os.environ.get("SECRET_KEY", "posyandu_anggrek14_secret")

    # Konfigurasi Database MySQL
    DB_HOST = os.environ.get("DB_HOST", "sgp.domcloud.co")
    DB_USER = os.environ.get("DB_USER", "laporan")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "kG-_CbsF_7Tw689Ou2")
    DB_NAME = os.environ.get("DB_NAME", "laporan_db")

    @staticmethod
    def get_db_config():
        """Mengembalikan konfigurasi database dalam bentuk dict untuk mysql.connector"""
        return {
            "host": Config.DB_HOST,
            "user": Config.DB_USER,
            "password": Config.DB_PASSWORD,
            "database": Config.DB_NAME
        }

    # Konfigurasi keamanan session
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"  # Bisa "Strict" jika HTTPS
    SESSION_COOKIE_SECURE = False    # Ubah ke True jika sudah pakai HTTPS
