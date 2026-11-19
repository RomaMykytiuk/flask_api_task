
from models import db, Group, Student, Course


# Отримати всі групи
def get_all_groups():
    return Group.query.all()


# Отримати всіх студентів
def get_all_students():
    return Student.query.all()


# Отримати всі курси
def get_all_courses():
    return Course.query.all()


# Знайти студентів певної групи
def get_students_by_group(group_id):
    return Student.query.filter_by(group_id=group_id).all()


# Знайти курси певного студента
def get_student_courses(student_id):
    student = db.session.get(Student, student_id)
    return student.courses if student else []


# Порахувати кількість студентів у кожній групі
def get_students_count_by_group():
    return (
        db.session.query(Group.name, db.func.count(Student.id))
        .outerjoin(Student)
        .group_by(Group.id, Group.name)
        .all()
    )


# Знайти студентів без групи
def get_students_without_group():
    return Student.query.filter_by(group_id=None).all()
