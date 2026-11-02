
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


student_courses = db.Table(
    "student_courses",
    db.Column(
        "student_id",
        db.Integer,
        db.ForeignKey("students.id", ondelete="CASCADE"),
        primary_key=True
    ),
    db.Column(
        "course_id",
        db.Integer,
        db.ForeignKey("courses.id", ondelete="CASCADE"),
        primary_key=True
    )
)


class Group(db.Model):
    __tablename__ = "groups"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(5), unique=True, nullable=False)

    students = db.relationship("Student", back_populates="group")


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    group_id = db.Column(
        db.Integer,
        db.ForeignKey("groups.id", ondelete="SET NULL"),
        nullable=True
    )
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    group = db.relationship("Group", back_populates="students")

    courses = db.relationship(
        "Course",
        secondary=student_courses,
        back_populates="students"
    )


class Course(db.Model):
    __tablename__ = "courses"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)

    students = db.relationship(
        "Student",
        secondary=student_courses,
        back_populates="courses"
    )
