def test_health_check(client):
    """
    Testa se a API está respondendo.
    Verifica se o endpoint /api/books retorna status 200.
    """
    response = client.get("/api/books")
    assert response.status_code == 200
    assert isinstance(response.json, list)
