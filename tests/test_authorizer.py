from fastapi import FastAPI
from fastapi.testclient import TestClient

from fastapi_key_auth.authorizer import AuthorizerMiddleware

app = FastAPI()
app.add_middleware(AuthorizerMiddleware, public_paths=["/health"])


@app.get("/ping")
async def ping():
    return {"ping": "pong"}


@app.get("/health")
async def health():
    return {"ok": True}


client = TestClient(app)


def test_unauthorized_no_api_key():
    response = client.get("/ping")
    assert response.status_code == 401
    assert response.text == "no api key"


def test_unauthorized_invalid_api_key():
    response = client.get("/ping", headers={"x-api-key": "baguette"})
    assert response.status_code == 401
    assert response.text == "invalid api key"


def test_authorized():
    response = client.get("/ping", headers={"x-api-key": "test"})

    assert response.status_code == 200
    assert response.json() == {"ping": "pong"}


def test_public_path():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"ok": True}
