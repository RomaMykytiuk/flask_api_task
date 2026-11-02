
from flask import Flask, jsonify
from sqlalchemy import text

from config import Config
from models import db, Group, Student, Course

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "message": "Flask SQL Task",
        "status": "success"
    })


@app.route("/test-db", methods=["GET"])
def test_database():
    try:
        result = db.session.execute(
            text("SELECT version()")
        )

        return jsonify({
            "status": "connected",
            "postgresql_version": result.scalar()
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "error_type": type(error).__name__,
            "message": str(error)
        }), 500


@app.route("/stats", methods=["GET"])
def stats():
    try:
        return jsonify({
            "groups": db.session.query(Group).count(),
            "students": db.session.query(Student).count(),
            "courses": db.session.query(Course).count()
        })

    except Exception as error:
        return jsonify({
            "status": "error",
            "error_type": type(error).__name__,
            "message": str(error)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)
