
from main import app
from models import db, Group, Course, Student

from queries import (
    get_groups_with_student_count_at_most,
    get_students_by_course,
    add_new_student,
    delete_student_by_id,
    add_student_to_course,
    remove_student_from_course
)


with app.app_context():
    group = Group.query.first()
    course = Course.query.first()

    # 1. Групи з кількістю студентів до 30
    groups = get_groups_with_student_count_at_most(30)
    print("Груп до 30 студентів:", len(groups))

    # 2. Студенти певного курсу
    students = get_students_by_course(course.name)
    print(f"Студентів на курсі {course.name}:", len(students))

    # 3. Додати нового студента
    student = add_new_student("Query", "Test", group.id)
    print("ADD STUDENT:", student.id)

    student_id = student.id

    # 4. Додати студента до курсу
    result = add_student_to_course(student_id, course.id)
    print("ADD TO COURSE:", result)

    # 5. Видалити студента з курсу
    result = remove_student_from_course(student_id, course.id)
    print("REMOVE FROM COURSE:", result)

    # 6. Видалити студента
    result = delete_student_by_id(student_id)
    print("DELETE STUDENT:", result)

    print("Студентів у базі:", Student.query.count())
