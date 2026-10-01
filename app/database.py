import sqlite3
import os
from flask import g, current_app

DB_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'smartlead.db')

def get_db():
    if 'db' not in g:
        # Config içinde varsa onu alır, yoksa doğrudan DB_FILE yolunu kullanır (KeyError vermez)
        db_path = current_app.config.get('DATABASE') or current_app.config.get('DATABASE_PATH') or DB_FILE
        g.db = sqlite3.connect(
            db_path,
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                eposta TEXT,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        # Tablo daha önceden eposta sütunu olmadan oluştuysa güvenle ekler
        try:
            db.execute('ALTER TABLE leads ADD COLUMN eposta TEXT')
        except sqlite3.OperationalError:
            pass
        db.commit()

def lead_ekle(isim, telefon, eposta="", feedback="", mesaj=""):
    db = get_db()
    not_icerik = feedback if feedback else mesaj
    cursor = db.execute(
        'INSERT INTO leads (isim, eposta, telefon, mesaj) VALUES (?, ?, ?, ?)',
        (isim, eposta, telefon, not_icerik)
    )
    db.commit()
    return cursor.lastrowid

def tum_leadler():
    db = get_db()
    cursor = db.execute('SELECT id, isim, eposta, telefon, mesaj, tarih FROM leads ORDER BY id DESC')
    satirlar = cursor.fetchall()
    return [
        {
            "id": row["id"],
            "isim": row["isim"],
            "eposta": row["eposta"] if "eposta" in row.keys() and row["eposta"] else "-",
            "telefon": row["telefon"],
            "feedback": row["mesaj"] if row["mesaj"] else "-",
            "mesaj": row["mesaj"] if row["mesaj"] else "-",
            "tarih": str(row["tarih"])
        }
        for row in satirlar
    ]