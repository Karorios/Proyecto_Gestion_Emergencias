# database.py
import sqlite3
from datetime import datetime

DB_NAME = "emergencias.db"


def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emergencias (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT,
        direccion TEXT,
        telefono TEXT,
        emergencia TEXT,
        ambulancia TEXT,
        fecha_hora TEXT,
        estado TEXT
    )
    """)

    conn.commit()
    conn.close()


def guardar_reporte(emergencia, ambulancia):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO emergencias (nombre, direccion, telefono, emergencia, ambulancia, fecha_hora, estado)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        emergencia["nombre"],
        emergencia["direccion"],
        emergencia["telefono"],
        emergencia["emergencia"],
        ambulancia,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "Asignada"
    ))

    conn.commit()
    conn.close()
