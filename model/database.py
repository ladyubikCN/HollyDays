import sqlite3

class Database:

    def __init__(self, db_path="files/HollyDays.db"):
        self.db_path = db_path
        self._create_table()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _create_table(self):
        with self._connect() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS logos (
                    url TEXT PRIMARY KEY,
                    base64 TEXT
                )
            """)

    def get_logo(self, url):
        with self._connect() as conn:
            cursor = conn.execute(
                "SELECT base64 FROM logos WHERE url = ?",
                (url,)
            )
            row = cursor.fetchone()

        return row[0] if row else None

    def set_logo(self, url, base64):
        try:
            with self._connect() as conn:
                conn.execute("""
                    INSERT INTO logos (url, base64)
                    VALUES (?, ?)
                    ON CONFLICT(url) DO UPDATE SET base64 = excluded.base64
                """, (url, base64))
                conn.commit()
                print(f"DEBUG: Logo salvato con successo per {url}")
        except sqlite3.Error as e:
            print(f"ERRORE SQLITE: {e}")