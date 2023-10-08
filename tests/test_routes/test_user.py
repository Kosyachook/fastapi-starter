
def test_create_user(client):
    data = {"email":"testuser@nofoobar.com","password":"testing2332"}
    response = client.post("/users",json=data)
    assert response.status_code == 201
    assert response.json()["email"] == "testuser@nofoobar.com"
    assert response.json()["is_active"] == True
