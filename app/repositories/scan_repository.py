import sqlite3
from app.config import Config
from app.models.scan import Scan
from app.models.scan_item import ScanItem


def get_connection():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def save_scan(scan: Scan) -> int:
    """Taramayı kaydeder, oluşan ID'yi döndürür."""
    conn = get_connection()
    cursor = conn.execute(
        """INSERT INTO scans (url, kvkk_score, gdpr_score, risk_level, llm_suggestions)
           VALUES (?, ?, ?, ?, ?)""",
        (scan.url, scan.kvkk_score, scan.gdpr_score, scan.risk_level, scan.llm_suggestions)
    )
    conn.commit()
    scan_id = cursor.lastrowid
    conn.close()
    return scan_id


def save_scan_items(scan_id: int, items: list[ScanItem]):
    """Kontrol maddelerini kaydeder."""
    conn = get_connection()
    for item in items:
        conn.execute(
            """INSERT INTO scan_items (scan_id, category, item_key, item_label, status)
               VALUES (?, ?, ?, ?, ?)""",
            (scan_id, item.category, item.item_key, item.item_label, item.status)
        )
    conn.commit()
    conn.close()


def get_all_scans() -> list[Scan]:
    """Tüm taramaları en yeniden eskiye listeler."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM scans ORDER BY created_at DESC").fetchall()
    conn.close()
    return [Scan(**dict(row)) for row in rows]


def get_scan_by_id(scan_id: int) -> Scan | None:
    """ID'ye göre tek tarama getirir."""
    conn = get_connection()
    row = conn.execute("SELECT * FROM scans WHERE id = ?", (scan_id,)).fetchone()
    conn.close()
    return Scan(**dict(row)) if row else None


def get_scan_items_by_scan_id(scan_id: int) -> list[ScanItem]:
    """Taramaya ait kontrol maddelerini getirir."""
    conn = get_connection()
    rows = conn.execute("SELECT * FROM scan_items WHERE scan_id = ?", (scan_id,)).fetchall()
    conn.close()
    return [ScanItem(**dict(row)) for row in rows]
