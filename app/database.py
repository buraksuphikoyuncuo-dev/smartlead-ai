import sqlite3
from flask import g, current_app

def get_db():
    """Mevcut istek için veritabanı bağlantısı açar veya var olanı döner."""
    if 'db' not in g:
        db_path = current_app.config.get('DATABASE_URL', 'smartlead.db')
        g.db = sqlite3.connect(db_path)
        # Tablodan gelen verilerin isimleriyle (sütun adı) okunabilmesini sağlar
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    """İstek tamamlandığında bağlantıyı kapatır."""
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db(app):
    """Uygulama açılırken 'leads' tablosunu oluşturur (yoksa)."""
    with app.app_context():
        db = get_db()
        # id otomatik artar, isim ve telefon zorunludur
        db.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                isim TEXT NOT NULL,
                telefon TEXT NOT NULL,
                mesaj TEXT,
                tarih TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        db.commit()

def lead_ekle(isim, telefon, mesaj=""):
    """
    Yeni müşteri adayı kaydeder.
    SQL Injection açığını engellemek için ? yer tutucusu kullanılmıştır.
    """
    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO leads (isim, telefon, mesaj) VALUES (?, ?, ?)",
        (isim, telefon, mesaj)
    )
    db.commit()
    return cursor.lastrowid

def tum_leadler():
    """Kayıtlı tüm müşterileri en yeni tarihten en eskiye doğru getirir."""
    db = get_db()
    cursor = db.execute(
        "SELECT id, isim, telefon, mesaj, tarih FROM leads ORDER BY tarih DESC"
    )
    rows = cursor.fetchall()
    
    # Gelen veriyi standart Python sözlük listesine çeviriyoruz
    sonuclar = []
    for r in rows:
        sonuclar.append({
            "id": r["id"],
            "isim": r["isim"],
            "telefon": r["telefon"],
            "mesaj": r["mesaj"],
            "tarih": str(r["tarih"])
        })
    return sonuclar