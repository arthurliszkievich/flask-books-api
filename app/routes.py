import logging

from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app import db
from app.models import Book

bp = Blueprint("api", __name__, url_prefix="/api")
logger = logging.getLogger(__name__)


@bp.route("/books", methods=["GET"])
def get_books():
    """
    Lista todos os livros com paginação e filtros opcionais.

    Query params:
    - page: número da página (padrão: 1)
    - per_page: itens por página (padrão: 10, max: 100)
    - author: filtrar por autor (busca parcial)
    - genre: filtrar por gênero
    """
    try:
        # Paginação
        page = request.args.get("page", 1, type=int)
        per_page = min(request.args.get("per_page", 10, type=int), 100)

        # Construir query com filtros
        query = Book.query

        # Filtros opcionais
        if author := request.args.get("author"):
            query = query.filter(Book.author.ilike(f"%{author}%"))

        if genre := request.args.get("genre"):
            query = query.filter(Book.genre.ilike(f"%{genre}%"))

        # Executar query com paginação
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        return jsonify(
            {
                "books": [book.to_dict() for book in pagination.items],
                "pagination": {
                    "page": pagination.page,
                    "per_page": pagination.per_page,
                    "total_pages": pagination.pages,
                    "total_items": pagination.total,
                    "has_next": pagination.has_next,
                    "has_prev": pagination.has_prev,
                },
            }
        ), 200
    except Exception as e:
        logger.error(f"Error fetching books: {str(e)}")
        return jsonify({"error": "Failed to fetch books"}), 500


@bp.route("/books/<int:book_id>", methods=["GET"])
def get_book(book_id):
    """Busca um livro por ID"""
    book = Book.query.get_or_404(book_id)
    return jsonify(book.to_dict()), 200


@bp.route("/books", methods=["POST"])
def create_book():
    """
    Adiciona um novo livro.

    Campos obrigatórios:
    - title: string (max 200)
    - author: string (max 100)

    Campos opcionais:
    - isbn: string (13 caracteres)
    - genre: string (max 50)
    - publication_year: integer
    - description: text
    """
    try:
        data = request.get_json()

        # Validação básica
        if not data:
            return jsonify({"error": "Request body is required"}), 400

        if not data.get("title") or not isinstance(data.get("title"), str):
            return jsonify({"error": "Title is required and must be a string"}), 400

        if not data.get("author") or not isinstance(data.get("author"), str):
            return jsonify({"error": "Author is required and must be a string"}), 400

        # Validar comprimento
        if len(data["title"]) > 200:
            return jsonify({"error": "Title must be 200 characters or less"}), 400

        if len(data["author"]) > 100:
            return jsonify({"error": "Author must be 100 characters or less"}), 400

        # Validar ISBN se fornecido
        if isbn := data.get("isbn"):
            if not isinstance(isbn, str) or len(isbn) != 13:
                return jsonify({"error": "ISBN must be exactly 13 characters"}), 400

        # Validar ano de publicação
        if pub_year := data.get("publication_year"):
            if not isinstance(pub_year, int) or pub_year < 0 or pub_year > 9999:
                return jsonify({"error": "Invalid publication year"}), 400

        # Criar livro
        book = Book(
            title=data["title"].strip(),
            author=data["author"].strip(),
            isbn=data.get("isbn"),
            genre=data.get("genre"),
            publication_year=data.get("publication_year"),
            description=data.get("description"),
        )

        db.session.add(book)
        db.session.commit()

        logger.info(f"Book created: {book.id} - {book.title}")
        return jsonify(book.to_dict()), 201

    except IntegrityError as e:
        db.session.rollback()
        logger.error(f"Integrity error creating book: {str(e)}")
        return jsonify({"error": "Book with this ISBN already exists"}), 409
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error creating book: {str(e)}")
        return jsonify({"error": "Database error occurred"}), 500
    except Exception as e:
        db.session.rollback()
        logger.error(f"Unexpected error creating book: {str(e)}")
        return jsonify({"error": "Failed to create book"}), 500


@bp.route("/books/<int:book_id>", methods=["PUT"])
def update_book(book_id):
    """Atualiza um livro existente (atualização parcial)"""
    try:
        book = Book.query.get_or_404(book_id)
        data = request.get_json()

        if not data:
            return jsonify({"error": "Request body is required"}), 400

        # Validar e atualizar campos
        if "title" in data:
            if not data["title"] or len(data["title"]) > 200:
                return jsonify({"error": "Invalid title"}), 400
            book.title = data["title"].strip()

        if "author" in data:
            if not data["author"] or len(data["author"]) > 100:
                return jsonify({"error": "Invalid author"}), 400
            book.author = data["author"].strip()

        if "isbn" in data:
            if data["isbn"] and len(data["isbn"]) != 13:
                return jsonify({"error": "ISBN must be exactly 13 characters"}), 400
            book.isbn = data["isbn"]

        if "genre" in data:
            book.genre = data["genre"]

        if "publication_year" in data:
            if data["publication_year"] and (
                data["publication_year"] < 0 or data["publication_year"] > 9999
            ):
                return jsonify({"error": "Invalid publication year"}), 400
            book.publication_year = data["publication_year"]

        if "description" in data:
            book.description = data["description"]

        db.session.commit()
        logger.info(f"Book updated: {book.id} - {book.title}")

        return jsonify(book.to_dict()), 200

    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Book with this ISBN already exists"}), 409
    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Database error updating book: {str(e)}")
        return jsonify({"error": "Database error occurred"}), 500


@bp.route("/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    """Deleta um livro"""
    try:
        book = Book.query.get_or_404(book_id)
        title = book.title  # Guardar para o log

        db.session.delete(book)
        db.session.commit()

        logger.info(f"Book deleted: {book_id} - {title}")
        return jsonify({"message": "Book deleted successfully"}), 200

    except SQLAlchemyError as e:
        db.session.rollback()
        logger.error(f"Error deleting book {book_id}: {str(e)}")
        return jsonify({"error": "Failed to delete book"}), 500


@bp.route("/health", methods=["GET"])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200
