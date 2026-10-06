import sqlite3


class LexiconStore:
    def __init__(self, path: str):
        self.connection = sqlite3.connect(path)
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS lexicon_terms (term TEXT NOT NULL, weight REAL NOT NULL, source TEXT)"
        )

    def close(self) -> None:
        self.connection.close()

    def get_tables(self, database, table_names=[]):
        cursor = self.connection.cursor()
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        if table_names:
            clause = ' OR '.join(["name LIKE '%%%(table)s%%'" % {'table': table} for table in table_names])
            query += ' AND (%s)' % clause
        cursor.execute(query)
        self.connection.commit()
        return [row[0] for row in cursor.fetchall()]
