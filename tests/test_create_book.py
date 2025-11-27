import json


def test_create_book(client):
    """
    Testa a criação de um livro via POST /api/books.
    Verifica se o livro é criado com sucesso e retorna status 201.
    """
    book_data = {
        "title": "1984",
        "author": "George Orwell",
        "isbn": "9780451524935",
        "genre": "Distopia",
        "publication_year": 1949,
        "description": "Um clássico da literatura distópica",
    }

    response = client.post(
        "/api/books", data=json.dumps(book_data), content_type="application/json"
    )

    assert response.status_code == 201
    data = response.json

    # Verifica se os campos foram salvos corretamente
    assert data["title"] == book_data["title"]
    assert data["author"] == book_data["author"]
    assert data["isbn"] == book_data["isbn"]
    assert data["genre"] == book_data["genre"]
    assert data["publication_year"] == book_data["publication_year"]
    assert data["description"] == book_data["description"]
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_book_missing_required_fields(client):
    """
    Testa a criação de um livro sem campos obrigatórios.
    Deve retornar erro 400.
    """
    book_data = {
        "title": "Livro sem autor"
        # Faltando author (campo obrigatório)
    }

    response = client.post(
        "/api/books", data=json.dumps(book_data), content_type="application/json"
    )

    assert response.status_code == 400
    assert "error" in response.json


def test_get_created_book(client):
    """
    Testa a recuperação de um livro criado.
    Cria um livro e depois busca ele por ID.
    """
    # Cria o livro
    book_data = {
        "title": "O Senhor dos Anéis",
        "author": "J.R.R. Tolkien",
        "isbn": "9780618640157",
    }

    create_response = client.post(
        "/api/books", data=json.dumps(book_data), content_type="application/json"
    )

    assert create_response.status_code == 201
    book_id = create_response.json["id"]

    # Busca o livro criado
    get_response = client.get(f"/api/books/{book_id}")

    assert get_response.status_code == 200
    data = get_response.json
    assert data["id"] == book_id
    assert data["title"] == book_data["title"]
    assert data["author"] == book_data["author"]
    assert data["isbn"] == book_data["isbn"]
