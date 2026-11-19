
from main import app
from models import Group, Student
from crud import create_student, get_student, update_student, delete_student

with app.app_context():
    group = Group.query.first()

    # CREATE
    student = create_student("Test", "Student", group.id)
    student_id = student.id
    print("CREATE:", student.first_name, student.last_name)

    # READ
    student = get_student(student_id)
    print("READ:", student.id)

    # UPDATE
    student = update_student(student_id, first_name="Updated")
    print("UPDATE:", student.first_name)

    # DELETE
    result = delete_student(student_id)
    print("DELETE:", result)

    print("Студентів у базі:", Student.query.count())
