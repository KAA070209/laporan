import sys
import os

# Pastikan path ke project sudah benar
sys.path.insert(0, os.path.dirname(__file__))

from app import app as application  # Flask akan baca dari app.py
