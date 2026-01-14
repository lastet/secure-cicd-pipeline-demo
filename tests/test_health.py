from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_ok():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}

def test_hello_default():
    r = client.get("/hello")
    assert r.status_code == 200
    assert r.json()["message"] == "hello, mr unicorn"

def test_hello_custom():
    r = client.get("/hello?name=anya")
    assert r.status_code == 200
    assert r.json()["message"] == "hello, world"
