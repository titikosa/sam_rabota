import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app as flask_app
from database import init_db


@pytest.fixture
def app():
    flask_app.config["TESTING"] = True
    flask_app.config["DATABASE"] = ":memory:"
    with flask_app.app_context():
        init_db()
        yield flask_app


@pytest.fixture
def client(app):
    return app.test_client()


def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200


def test_add_recipe(client):
    response = client.post("/add", data={
        "title": "Тестовый суп",
        "ingredients": "Вода, соль",
        "instructions": "Вскипятить воду",
        "category": "супы",
        "cook_time": "10 минут"
    }, follow_redirects=True)
    assert response.status_code == 200
    assert "Тестовый суп".encode() in response.data


def test_search(client):
    client.post("/add", data={"title": "Борщ", "ingredients": "Свёкла", "instructions": "Варить", "category": "супы", "cook_time": ""})
    client.post("/add", data={"title": "Тирамису", "ingredients": "Маскарпоне", "instructions": "Смешать", "category": "десерты", "cook_time": ""})
    response = client.get("/?q=Борщ")
    assert "Борщ".encode() in response.data
    assert "Тирамису".encode() not in response.data


def test_recipe_not_found(client):
    response = client.get("/recipe/99999")
    assert response.status_code == 404


def test_empty_title_rejected(client):
    response = client.post("/add", data={
        "title": "",
        "ingredients": "Что-то",
        "instructions": "Как-то",
        "category": "другое",
        "cook_time": ""
    })
    assert response.status_code == 200
    assert "Название не может быть пустым".encode() in response.data