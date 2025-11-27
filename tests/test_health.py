def test_health_check(client):
    """
    Testa se a API está respondendo.
    Verifica se o endpoint /api/books retorna status 200.
    """
    response = client.get("/api/books")
    assert response.status_code == 200
    assert isinstance(response.json, dict)
    assert "books" in response.json
    assert isinstance(response.json["books"], list)
    assert "pagination" in response.json
