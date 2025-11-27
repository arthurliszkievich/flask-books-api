from datetime import datetime

from app import db


class Book(db.Model):
    __tablename__ = "books"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=True)
    genre = db.Column(db.String(50), nullable=True)
    publication_year = db.Column(db.Integer, nullable=True)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "isbn": self.isbn,
            "genre": self.genre,
            "publication_year": self.publication_year,
            "description": self.description,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None,
        }

    def __repr__(self):
        return f"<Book {self.title} by {self.author}>"

    @classmethod
    def find_by_isbn(cls, isbn: str):
        """Busca livro por ISBN"""
        return cls.query.filter_by(isbn=isbn).first()

    @classmethod
    def search(cls, query: str):
        """Busca livros por título ou autor"""
        search_pattern = f"%{query}%"
        return cls.query.filter(
            db.or_(cls.title.ilike(search_pattern), cls.author.ilike(search_pattern))
        ).all()

    @classmethod
    def get_by_genre(cls, genre: str):
        """Busca livros por gênero"""
        return cls.query.filter_by(genre=genre).all()

    def update_from_dict(self, data: dict):
        """Atualiza livro a partir de dicionário"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ["id", "created_at"]:
                setattr(self, key, value)
