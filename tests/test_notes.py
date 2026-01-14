from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_and_get_note():
    r = client.post("/notes", json={"text": "hello"})
    assert r.status_code == 201
    data = r.json()
    assert "id" in data
    assert data["text"] == "hello"

    note_id = data["id"]
    g = client.get(f"/notes/{note_id}")
    assert g.status_code == 200
    assert g.json()["text"] == "hello"

def test_list_notes():
    client.post("/notes", json={"text": "n1"})
    client.post("/notes", json={"text": "n2"})
    r = client.get("/notes")
    assert r.status_code == 200
    texts = [x["text"] for x in r.json()]
    assert "n1" in texts and "n2" in texts

def test_delete_note():
    r = client.post("/notes", json={"text": "to-delete"})
    note_id = r.json()["id"]
    d = client.delete(f"/notes/{note_id}")
    assert d.status_code == 204
    g = client.get(f"/notes/{note_id}")
    assert g.status_code == 404

def test_validation_rejects_empty():
    r = client.post("/notes", json={"text": ""})
    assert r.status_code == 422  # pydantic validation

def test_escapes_html_in_note_text():
    r = client.post("/notes", json={"text": "<script>alert(1)</script>"})
    assert r.status_code == 201
   
    assert r.json()["text"] == "&lt;script&gt;alert(1)&lt;/script&gt;"
