
from main import app
from queries import (
    get_all_groups,
    get_all_students,
    get_all_courses,
    get_students_by_group,
    get_student_courses,
    get_students_count_by_group,
    get_students_without_group
)

with app.app_context():
    groups = get_all_groups()
    students = get_all_students()
    courses = get_all_courses()

    print("Груп:", len(groups))
    print("Студентів:", len(students))
    print("Курсів:", len(courses))

    if groups:
        print("Студентів у першій групі:",
              len(get_students_by_group(groups[0].id)))

    if students:
        print("Курсів у першого студента:",
              len(get_student_courses(students[0].id)))

    print("Кількість студентів за групами:")
    for name, count in get_students_count_by_group():
        print(name, count)

    print("Студентів без групи:",
          len(get_students_without_group()))
