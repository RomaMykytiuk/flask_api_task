
import pytest

from main import app
from models import db, Group, Student


@pytest.fixture
def client():
    app.config["TESTING"] = True

    with app.test_client() as client:
        yield client


def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json["status"] == "success"


def test_stats(client):
    response = client.get("/stats")

    assert response.status_code == 200
    assert response.json["groups"] == 10
    assert response.json["students"] == 200
    assert response.json["courses"] == 10


def test_get_students(client):
    response = client.get("/students")

    assert response.status_code == 200
    assert len(response.json) == 200


def test_get_student(client):
    response = client.get("/students/1")

    assert response.status_code == 200
    assert response.json["id"] == 1


def test_student_not_found(client):
    response = client.get("/students/999999")

    assert response.status_code == 404


def test_create_student(client):
    with app.app_context():
        group = Group.query.first()
        group_id = group.id

    response = client.post(
        "/students",
        json={
            "first_name": "Pytest",
            "last_name": "Student",
            "group_id": group_id
        }
    )

    assert response.status_code == 201

    student_id = response.json["id"]

    with app.app_context():
        student = db.session.get(Student, student_id)
        assert student is not None

        db.session.delete(student)
        db.session.commit()


def test_create_student_without_data(client):
    response = client.post("/students", json={})

    assert response.status_code == 400


def test_delete_student_not_found(client):
    response = client.delete("/students/999999")

    assert response.status_code == 404
