import sqlite3
import os
from flask import current_app, g


def get_db():
    """Mevcut istek için veritabanı bağlantısı döndürür."""
    if "db" not in g:
        os.makedirs("instance", exist_ok=True)
        g.db = sqlite3.connect(
            current_app.config["DATABASE_PATH"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db


def close_db(e=None):
    """İstek bitince bağlantıyı kapatır."""
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    """Uygulama ilk çalıştığında tabloları oluşturur."""
    os.makedirs("instance", exist_ok=True)
    db = sqlite3.connect(current_app.config["DATABASE_PATH"])

    db.execute("""
        CREATE TABLE IF NOT EXISTS scans (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            url         TEXT NOT NULL,
            kvkk_score  REAL,
            gdpr_score  REAL,
            risk_level  TEXT,
            llm_suggestions TEXT,
            created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    db.execute("""
        CREATE TABLE IF NOT EXISTS scan_items (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            scan_id     INTEGER NOT NULL,
            category    TEXT,
            item_key    TEXT,
            item_label  TEXT,
            status      INTEGER DEFAULT 0,
            FOREIGN KEY (scan_id) REFERENCES scans(id)
        )
    """)

    db.commit()
    db.close()
