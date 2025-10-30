import sys
import os
from dotenv import load_dotenv

# Pastikan path ke project sudah benar
BASE_DIR=0, os.path.dirname(__file__)
sys.path.insert(0, BASE_DIR)

load_dotenv(os.path.join(BASE_DIR, ".env"))

from app import app as application  # Flask akan baca dari app.py

