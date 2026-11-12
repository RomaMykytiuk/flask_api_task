
import random
import string

from main import app
from models import db, Group, Student, Course


COURSES = [
    ("Mathematics", "Mathematics and algebra"),
    ("Physics", "Physics fundamentals"),
    ("Chemistry", "Chemistry fundamentals"),
    ("Biology", "Biology fundamentals"),
    ("History", "World history"),
    ("Geography", "World geography"),
    ("English", "English language"),
    ("Computer Science", "Programming and computer science"),
    ("Literature", "World literature"),
    ("Economics", "Economics fundamentals")
]

FIRST_NAMES = [
    "James", "John", "Robert", "Michael", "David",
    "William", "Daniel", "Thomas", "Emma", "Olivia",
    "Sophia", "Emily", "Isabella", "Mia", "Charlotte"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones",
    "Garcia", "Miller", "Davis", "Wilson", "Taylor",
    "Anderson", "Thomas", "Jackson", "White", "Harris"
]


def generate_group_name():
    return (
        "".join(random.choices(string.ascii_uppercase, k=2))
        + "-"
        + "".join(random.choices(string.digits, k=2))
    )


def create_groups():
    existing_names = {group.name for group in Group.query.all()}

    while Group.query.count() + len(db.session.new) < 10:
        name = generate_group_name()

        if name not in existing_names:
            db.session.add(Group(name=name))
            existing_names.add(name)

    db.session.flush()


def create_courses():
    for name, description in COURSES:
        if not Course.query.filter_by(name=name).first():
            db.session.add(Course(name=name, description=description))

    db.session.flush()


def create_students():
    groups = Group.query.all()
    courses = Course.query.all()

    current_count = Student.query.count()

    for _ in range(max(0, 200 - current_count)):
        student = Student(
            first_name=random.choice(FIRST_NAMES),
            last_name=random.choice(LAST_NAMES),
            group=random.choice(groups)
        )

        student.courses = random.sample(
            courses,
            k=random.randint(1, 3)
        )

        db.session.add(student)

    db.session.flush()


def seed_database():
    with app.app_context():
        try:
            create_groups()
            create_courses()
            create_students()

            db.session.commit()

            print("Database seeded successfully!")
            print(f"Groups: {Group.query.count()}")
            print(f"Courses: {Course.query.count()}")
            print(f"Students: {Student.query.count()}")

        except Exception:
            db.session.rollback()
            raise


if __name__ == "__main__":
    seed_database()
