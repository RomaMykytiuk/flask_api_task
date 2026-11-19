
from flask import Flask, jsonify, request
from sqlalchemy import text

from config import Config
from models import db, Group, Student, Course
from crud import create_student, get_student, update_student, delete_student

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


def student_to_dict(student):
    return {
        "id": student.id,
        "first_name": student.first_name,
        "last_name": student.last_name,
        "group_id": student.group_id,
        "courses": [
            {"id": course.id, "name": course.name}
            for course in student.courses
        ]
    }


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Flask SQL Task",
        "status": "success"
    })


@app.route("/test-db", methods=["GET"])
def test_database():
    try:
        result = db.session.execute(text("SELECT version()"))
        return jsonify({
            "status": "connected",
            "postgresql_version": result.scalar()
        })
    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


@app.route("/stats", methods=["GET"])
def stats():
    try:
        return jsonify({
            "groups": Group.query.count(),
            "students": Student.query.count(),
            "courses": Course.query.count()
        })
    except Exception as error:
        return jsonify({
            "status": "error",
            "message": str(error)
        }), 500


# GET — усі студенти
@app.route("/students", methods=["GET"])
def get_students():
    students = Student.query.all()
    return jsonify([student_to_dict(s) for s in students])


# GET — студент за ID
@app.route("/students/<int:student_id>", methods=["GET"])
def get_student_by_id(student_id):
    student = get_student(student_id)

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student_to_dict(student))


# POST — створити студента
@app.route("/students", methods=["POST"])
def add_student():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON data is required"}), 400

    first_name = data.get("first_name")
    last_name = data.get("last_name")
    group_id = data.get("group_id")

    if not first_name or not last_name or group_id is None:
        return jsonify({
            "error": "first_name, last_name and group_id are required"
        }), 400

    group = db.session.get(Group, group_id)

    if group is None:
        return jsonify({"error": "Group not found"}), 404

    student = create_student(first_name, last_name, group_id)

    return jsonify(student_to_dict(student)), 201


# PUT — оновити студента
@app.route("/students/<int:student_id>", methods=["PUT"])
def edit_student(student_id):
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "JSON data is required"}), 400

    if "group_id" in data and data["group_id"] is not None:
        group = db.session.get(Group, data["group_id"])

        if group is None:
            return jsonify({"error": "Group not found"}), 404

    student = update_student(
        student_id,
        first_name=data.get("first_name"),
        last_name=data.get("last_name"),
        group_id=data.get("group_id")
    )

    if student is None:
        return jsonify({"error": "Student not found"}), 404

    return jsonify(student_to_dict(student))


# DELETE — видалити студента
@app.route("/students/<int:student_id>", methods=["DELETE"])
def remove_student(student_id):
    if not delete_student(student_id):
        return jsonify({"error": "Student not found"}), 404

    return jsonify({"message": "Student deleted successfully"})


if __name__ == "__main__":
    app.run(debug=True)
