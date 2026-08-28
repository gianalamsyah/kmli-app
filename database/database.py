import sys
import shutil
import sqlite3
from pathlib import Path


def _persistent_database_dir():
    """
    Lokasi folder database yang PERMANEN.

    Saat dijalankan sebagai .exe (PyInstaller --onefile), __file__ berada
    di folder temp yang dihapus setiap aplikasi ditutup, jadi tidak boleh
    dipakai untuk menyimpan data. Sebagai gantinya kita pakai folder
    tempat file .exe berada (sys.executable).

    Saat dijalankan sebagai script python biasa (development), tetap
    pakai folder ini seperti semula.
    """

    if getattr(sys, "frozen", False):
        # Berjalan sebagai .exe hasil PyInstaller
        return Path(sys.executable).parent / "database"

    return Path(__file__).parent


def _bundled_template_db():
    """
    Lokasi database template yang ikut dibundle di dalam .exe
    (hanya ada saat frozen, dipakai sebagai isi awal jika database
    permanen belum ada).
    """

    if hasattr(sys, "_MEIPASS"):
        return Path(sys._MEIPASS) / "database" / "db_kmli.db"

    return None


class DatabaseManager:

    def __init__(self):

        # Folder database (permanen, di sebelah .exe)
        database_dir = _persistent_database_dir()
        database_dir.mkdir(parents=True, exist_ok=True)

        # File database
        self.db_path = database_dir / "db_kmli.db"

        # Jika database permanen belum ada, salin dari template bawaan
        if not self.db_path.exists():
            template = _bundled_template_db()
            if template is not None and template.exists():
                shutil.copy(template, self.db_path)

        # Connection
        self.conn = None

        # Connect
        self.connect()

        # Create table jika belum ada
        self.create_tables()

    # =====================================================
    # CONNECT
    # =====================================================

    def connect(self):

        if self.conn is None:
            self.conn = sqlite3.connect(self.db_path)
            print(f"[DATABASE] Connected : {self.db_path}")

    def is_connected(self):
        return self.conn is not None

    # =====================================================
    # CREATE TABLE
    # =====================================================

    def create_tables(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tbl_slalom (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                nama_team TEXT NOT NULL,

                no_urut INTEGER NOT NULL,

                universitas TEXT NOT NULL,

                elapsed_time REAL NOT NULL,

                speed REAL NOT NULL,

                status TEXT NOT NULL
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tbl_lap (

                id INTEGER PRIMARY KEY AUTOINCREMENT,

                nama_team TEXT NOT NULL,

                no_urut INTEGER NOT NULL,

                universitas TEXT NOT NULL,

                lap1 REAL NOT NULL,

                lap2 REAL NOT NULL,

                lap3 REAL NOT NULL,

                lap4 REAL NOT NULL,

                lap5 REAL NOT NULL,

                total_time REAL NOT NULL,

                status TEXT NOT NULL
            )
        """)

        # =====================================================
        # BRAKE
        # =====================================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_brake (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nama_team TEXT NOT NULL,
            no_urut TEXT NOT NULL,
            universitas TEXT NOT NULL,

            entry_speed REAL NOT NULL,
            brake_speed REAL NOT NULL,
            deceleration REAL NOT NULL,
            acceleration REAL,

            status TEXT NOT NULL
        )
        """)

        # =====================================================
        # HILL
        # =====================================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS tbl_hill (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            nama_team TEXT NOT NULL,
            no_urut TEXT NOT NULL,
            universitas TEXT NOT NULL,

            massa REAL NOT NULL,
            waktu REAL NOT NULL,
            kecepatan REAL NOT NULL,
            daya REAL NOT NULL,

            status TEXT NOT NULL
        )
        """)

        # =====================================================
        # MIGRATION BRAKE
        # =====================================================
        # Database lama mungkin belum memiliki kolom acceleration.
        cursor.execute("PRAGMA table_info(tbl_brake)")
        brake_columns = {
            row[1]
            for row in cursor.fetchall()
        }

        if "acceleration" not in brake_columns:
            cursor.execute(
                "ALTER TABLE tbl_brake ADD COLUMN acceleration REAL"
            )

        self.conn.commit()

    # =====================================================
    # CLOSE
    # =====================================================

    def close(self):

        if self.conn:

            self.conn.close()
            self.conn = None

    def save_slalom(
        self,
        nama_team,
        no_urut,
        universitas,
        elapsed_time,
        speed,
        status
    ):

        sql = """
            INSERT INTO tbl_slalom
            (
                nama_team,
                no_urut,
                universitas,
                elapsed_time,
                speed,
                status
            )
            VALUES
            (?, ?, ?, ?, ?, ?)
        """

        cursor = self.conn.cursor()

        cursor.execute(
            sql,
            (
                nama_team,
                no_urut,
                universitas,
                elapsed_time,
                speed,
                status
            )
        )

        self.conn.commit()

    # =====================================================
    # GET SLALOM
    # =====================================================

    def get_slalom(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                no_urut,
                nama_team,
                universitas,
                elapsed_time,
                speed,
                status
            FROM tbl_slalom
            ORDER BY id ASC
        """)

        return cursor.fetchall()

    # =====================================================
    # SAVE BRAKE
    # =====================================================

    def save_brake(
        self,
        nama_team,
        no_urut,
        universitas,
        acceleration,
        deceleration,
        status
    ):

        cursor = self.conn.cursor()

        # entry_speed dan brake_speed dipertahankan untuk
        # kompatibilitas database lama, tetapi tidak lagi
        # digunakan/diekspor.
        cursor.execute("""
            INSERT INTO tbl_brake (
                nama_team,
                no_urut,
                universitas,
                entry_speed,
                brake_speed,
                deceleration,
                acceleration,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            nama_team,
            no_urut,
            universitas,
            0.0,
            0.0,
            deceleration,
            acceleration,
            status
        ))

        self.conn.commit()

    # =====================================================
    # GET BRAKE
    # =====================================================

    def get_brake(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                no_urut,
                nama_team,
                universitas,
                acceleration,
                deceleration,
                status
            FROM tbl_brake
            ORDER BY id ASC
        """)

        return cursor.fetchall()

    # =====================================================
    # GET LAP
    # =====================================================

    def get_lap(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                no_urut,
                nama_team,
                universitas,
                lap1,
                lap2,
                total_time,
                status
            FROM tbl_lap
            ORDER BY id ASC
        """)

        return cursor.fetchall()

    # =====================================================
    # GET HILL
    # =====================================================

    def get_hill(self):

        cursor = self.conn.cursor()

        cursor.execute("""
            SELECT
                no_urut,
                nama_team,
                universitas,
                massa,
                waktu,
                kecepatan,
                daya,
                status
            FROM tbl_hill
            ORDER BY id ASC
        """)

        return cursor.fetchall()

    # =====================================================
    # SAVE HILL
    # =====================================================

    def save_hill(
        self,
        nama_team,
        no_urut,
        universitas,
        massa,
        waktu,
        kecepatan,
        daya,
        status
    ):

        cursor = self.conn.cursor()

        cursor.execute("""
            INSERT INTO tbl_hill (
                nama_team,
                no_urut,
                universitas,
                massa,
                waktu,
                kecepatan,
                daya,
                status
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            nama_team,
            no_urut,
            universitas,
            massa,
            waktu,
            kecepatan,
            daya,
            status
        ))

        self.conn.commit()

    # =====================================================
    # SAVE LAP
    # =====================================================

    def save_lap(
        self,
        nama_team,
        no_urut,
        universitas,
        lap1,
        lap2,
        total_time,
        status
    ):

        sql = """
            INSERT INTO tbl_lap
            (
                nama_team,
                no_urut,
                universitas,
                lap1,
                lap2,
                lap3,
                lap4,
                lap5,
                total_time,
                status
            )
            VALUES
            (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor = self.conn.cursor()

        cursor.execute(
            sql,
            (
                nama_team,
                no_urut,
                universitas,
                lap1,
                lap2,
                0.0,
                0.0,
                0.0,
                total_time,
                status
            )
        )

        self.conn.commit()
