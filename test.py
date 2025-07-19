from interact import db, app
from interact.models import Seminar, Student, Group
from interact.lib.group_forming import GroupForming
from time import time

student_names =        ["Henk", "Tjeerd", "Karel", "Piet", "Jan", "Kees"]
student_scores =       [2, 1, 0, 1, 2, 0]
student_preparations = [4, 3, 3, 0, 1, 2]
student_motivations =  [3, 2, 5, 1, 2, 4]
nr_per_group = 2
gf_type = 3 # similarity grouping
user_id = 2 # the first normal user

with app.app_context():
    test = Seminar("Test_" + str(int(time())), len(student_names), user_id)
    test.active = True
    db.session.add(test)
    db.session.commit()

    students = []
    for i in range(len(student_names)):
        student = Student(student_names[i], test.id)
        student.preparation = student_preparations[i]
        student.motivation = student_motivations[i]
        student.score = student_scores[i]
        student.reached_gf = True
        students.append(student)
    db.session.add_all(students)
    db.session.commit()

    nr_groups = -(-len(students) // nr_per_group) # rounded-up integer division
    groups = [Group(test.id, n) for n in range(1, nr_groups+1)]
    db.session.add_all(groups)
    db.session.commit()
    gf = GroupForming(nr_per_group, students, groups)
    gf.divide(gf_type)
    students = gf.get_students()
    groups = gf.get_groups()
    db.session.commit()

    print("Group forming complete - please check results in database or app. Seminar name = " + test.name)