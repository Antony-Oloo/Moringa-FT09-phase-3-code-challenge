import sqlite3


class Author:
    def __init__(self, id, name):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Author name must be a non-empty string.")
        self.id = id
        self._name = name  # Using a private attribute (_name) to prevent changes

        # Insert the author into the database
        self._insert_into_database()

    def _insert_into_database(self):
        """Method to insert the author into the database."""
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS authors
                          (id INTEGER PRIMARY KEY, name TEXT)''')

        cursor.execute('''
            INSERT INTO authors (id, name) 
            VALUES (?, ?)
        ''', (self.id, self._name))

        conn.commit()
        conn.close()

    @property
    def name(self):
        return self._name  # Getter for the name attribute

    def __repr__(self):
        return f'<Author {self.name}>'

    # Method to retrieve all articles written by this author
    def articles(self):
        from .article import Article
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM articles WHERE author_id = ?
        ''', (self.id,))

        rows = cursor.fetchall()
        conn.close()

        return [Article(row[0], row[1], row[2], row[3], row[4]) for row in rows]

    # Method to retrieve all magazines that this author has contributed to
    def magazines(self):
        from .magazine import Magazine
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        ''', (self.id,))

        rows = cursor.fetchall()
        conn.close()

        return [Magazine(row[0], row[1], row[2]) for row in rows]

    # Static method to get author by ID
    @staticmethod
    def get_by_id(id):
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM authors WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Author(row[0], row[1])
        return None
