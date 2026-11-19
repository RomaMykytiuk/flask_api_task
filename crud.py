
from models import db, Student


# CREATE — створити студента
def create_student(first_name, last_name, group_id):
    student = Student(
        first_name=first_name,
        last_name=last_name,
        group_id=group_id
    )
    db.session.add(student)
    db.session.commit()
    return student


# READ — отримати студента за ID
def get_student(student_id):
    return db.session.get(Student, student_id)


# UPDATE — оновити дані студента
def update_student(student_id, first_name=None, last_name=None, group_id=None):
    student = get_student(student_id)

    if student is None:
        return None

    if first_name is not None:
        student.first_name = first_name

    if last_name is not None:
        student.last_name = last_name

    if group_id is not None:
        student.group_id = group_id

    db.session.commit()
    return student


# DELETE — видалити студента
def delete_student(student_id):
    student = get_student(student_id)

    if student is None:
        return False

    db.session.delete(student)
    db.session.commit()
    return True
