"""
SQLite version of the player cards database
"""

import sqlite3


class SqliteDatabase:
    def __init__(self, dev_mode: bool = True) -> None:
        self.DEV_MODE = dev_mode
        self._conn = sqlite3.connect(":memory:")
        self._cursor = self._conn.cursor()
        self._cursor.execute(
            "CREATE TABLE mycards (id integer PRIMARY KEY AUTOINCREMENT, color text, number text, special boolean)"
        )

    def add_card(self, color: str, number: str, special: bool) -> None:
        self._cursor.execute(
            f"INSERT INTO mycards (color, number, special) VALUES ('{color}', '{number}', {special})"
        )
        self._conn.commit()

    def get_cards_by_color(self, color: str) -> list:
        self._cursor.execute(f"SELECT * FROM mycards WHERE color = '{color}'")
        return self._cursor.fetchall()

    def get_cards_all(self) -> list:
        self._cursor.execute("SELECT * FROM mycards")
        return self._cursor.fetchall()

    def get_cards_matching_no_special(self, color: str, number: str) -> list:
        self._cursor.execute(
            f"SELECT * FROM mycards WHERE special = 0 AND (color = '{color}' OR number = '{number}')"
        )
        return self._cursor.fetchall()

    def get_cards_special(self) -> list:
        self._cursor.execute(f"SELECT * FROM mycards WHERE special = 1")
        return self._cursor.fetchall()

    def delete_card_by_id(self, _id: int) -> None:
        self._cursor.execute(f"DELETE FROM mycards WHERE id = {_id}")
        self._conn.commit()

    def close(self) -> None:
        self._conn.close()
