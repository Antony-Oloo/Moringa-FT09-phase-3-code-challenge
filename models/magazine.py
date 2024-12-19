import sqlite3
#from models.author import Author
class Magazine:
    def __init__(self, id, name, category="General"):
        self._id = id
        self.name = name
        self.category = category

        # Insert the magazine into the database
        self._insert_into_database()

    def _insert_into_database(self):
        """Method to insert the magazine into the database."""
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS magazines
                          (id INTEGER PRIMARY KEY, name TEXT, category TEXT)''')

        cursor.execute('''
            INSERT INTO magazines (id, name, category) 
            VALUES (?, ?, ?)
        ''', (self._id, self.name, self.category))

        conn.commit()
        conn.close()

    @property
    def id(self):
        return self._id

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Category must be a non-empty string")
        self._category = value

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not (2 <= len(value) <= 16):
            raise ValueError("Name must be between 2 and 16 characters")
        self._name = value

    def __repr__(self):
        return f"<Magazine {self.name} - {self.category}>"

    # To retrieve the magazine from the database by id
    @staticmethod
    def get_by_id(id):
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM magazines WHERE id = ?', (id,))
        row = cursor.fetchone()
        conn.close()

        if row:
            return Magazine(row[0], row[1], row[2])
        return None

    # Get all articles for this magazine
    def articles(self):
        from .article import Article
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT * FROM articles WHERE magazine_id = ?
        ''', (self.id,))

        rows = cursor.fetchall()
        conn.close()

        return [Article(row[0], row[1], row[2], row[3], row[4]) for row in rows]

    # Get all authors contributing to this magazine
    def contributors(self):
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT DISTINCT a.* FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
        ''', (self.id,))

        rows = cursor.fetchall()
        conn.close()

        return [Author(row[0], row[1]) for row in rows]

    # Get all article titles for this magazine
    def article_titles(self):
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT title FROM articles WHERE magazine_id = ?
        ''', (self.id,))

        rows = cursor.fetchall()
        conn.close()

        if rows:
            return [row[0] for row in rows]
        return None

    # Get authors who have contributed more than 2 articles
    def contributing_authors(self):
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute('''
            SELECT a.id, a.name FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
            GROUP BY a.id
            HAVING COUNT(ar.id) > 2
        ''', (self.id,))

        rows = cursor.fetchall()
        conn.close()

        if rows:
            return [Author(row[0], row[1]) for row in rows]
        return None
