import sqlite3
from datetime import datetime

DB_NAME = "gastos.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS gastos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario_id TEXT,
            supermercado TEXT,
            monto REAL,
            fecha TEXT
        )
    """)
    conn.commit()
    conn.close()

def guardar_gasto(usuario_id: str, supermercado: str, monto: float):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    fecha_actual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO gastos (usuario_id, supermercado, monto, fecha)
        VALUES (?, ?, ?, ?)
    """, (usuario_id, supermercado, monto, fecha_actual))
    conn.commit()
    conn.close()
