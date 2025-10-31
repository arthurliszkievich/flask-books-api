from flask import Blueprint, jsonify, request

from app import db
from app.models import Book

bp = Blueprint("api", __name__, url_prefix="/api")


@bp.route("/books", methods=["GET"])
def get_books():
    """Lista todos os livros"""
    books = Book.query.all()
    return jsonify([book.to_dict() for book in books]), 200


@bp.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    """Busca um livro por ID"""
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict()), 200


@bp.route("/books", methods=["POST"])
def create_book():
    """Adiciona um novo livro"""
    data = request.get_json()

    if not data or not data.get("title") or not data.get("author"):
        return jsonify({"error": "Title and author are required"}), 400

    book = Book(
        title=data.get("title"),
        author=data.get("author"),
        isbn=data.get("isbn"),
        genre=data.get("genre"),
        publication_year=data.get("publication_year"),
        description=data.get("description"),
    )

    db.session.add(book)
    db.session.commit()

    return jsonify(book.to_dict()), 201


@bp.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    """Atualiza um livro existente"""
    book = Book.query.get_or_404(book_id)
    data = request.get_json()

    if "title" in data:
        book.title = data["title"]
    if "author" in data:
        book.author = data["author"]
    if "isbn" in data:
        book.isbn = data["isbn"]
    if "genre" in data:
        book.genre = data["genre"]
    if "publication_year" in data:
        book.publication_year = data["publication_year"]
    if "description" in data:
        book.description = data["description"]

    db.session.commit()

    return jsonify(book.to_dict()), 200


@bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    """Deleta um livro"""
    book = Book.query.get_or_404(book_id)
    db.session.delete(book)
    db.session.commit()

    return jsonify({"message": "Book deleted successfully"}), 200


@bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200
