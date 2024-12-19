import sqlite3

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self.id = id
        self.title = title
        self.content = content
        self.author_id = author_id
        self.magazine_id = magazine_id

        # Insert the article into the database
        self._insert_into_database()

    def _insert_into_database(self):
        """Method to insert the article into the database."""
        conn = sqlite3.connect('magazine.db')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS articles
                          (id INTEGER PRIMARY KEY, title TEXT, content TEXT, author_id INTEGER, magazine_id INTEGER)''')

        cursor.execute('''
            INSERT INTO articles (id, title, content, author_id, magazine_id) 
            VALUES (?, ?, ?, ?, ?)
        ''', (self.id, self.title, self.content, self.author_id, self.magazine_id))

        conn.commit()
        conn.close()

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if isinstance(value, str) and 5 <= len(value) <= 50:
            self._title = value
        else:
            raise ValueError("Title must be a string between 5 and 50 characters.")

    @property
    def content(self):
        return self._content

    @content.setter
    def content(self, value):
        if isinstance(value, str) and len(value) > 0:
            self._content = value
        else:
            raise ValueError("Content must be a non-empty string.")

    def __repr__(self):
        return f'<Article {self.title}>'

    # Get the author of the article
    def get_author(self):
        from .author import Author 
        return Author.get_by_id(self.author_id)

    # Get the magazine of the article
    def get_magazine(self):
        return Magazine.get_by_id(self.magazine_id)

    # Property to get the article's author
    @property
    def author(self):
        return self.get_author()

    # Property to get the article's magazine
    @property
    def magazine(self):
        from .magazine import Magazine  
        return self.get_magazine()
