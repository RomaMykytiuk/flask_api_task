
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


# Групи, у яких кількість студентів не перевищує задану
def get_groups_with_student_count_at_most(max_count):
    return (
        db.session.query(Group)
        .outerjoin(Student)
        .group_by(Group.id)
        .having(db.func.count(Student.id) <= max_count)
        .all()
    )


# Знайти студентів, записаних на курс із заданою назвою
def get_students_by_course(course_name):
    return (
        Student.query
        .join(Student.courses)
        .filter(Course.name == course_name)
        .all()
    )


# Додати нового студента
def add_new_student(first_name, last_name, group_id):
    group = db.session.get(Group, group_id)

    if group is None:
        return None

    student = Student(
        first_name=first_name,
        last_name=last_name,
        group_id=group_id
    )

    db.session.add(student)
    db.session.commit()
    return student


# Видалити студента за ID
def delete_student_by_id(student_id):
    student = db.session.get(Student, student_id)

    if student is None:
        return False

    db.session.delete(student)
    db.session.commit()
    return True


# Додати студента до курсу
def add_student_to_course(student_id, course_id):
    student = db.session.get(Student, student_id)
    course = db.session.get(Course, course_id)

    if student is None or course is None:
        return False

    if course not in student.courses:
        student.courses.append(course)
        db.session.commit()

    return True


# Видалити студента з одного курсу
def remove_student_from_course(student_id, course_id):
    student = db.session.get(Student, student_id)
    course = db.session.get(Course, course_id)

    if student is None or course is None:
        return False

    if course not in student.courses:
        return False

    student.courses.remove(course)
    db.session.commit()
    return True
