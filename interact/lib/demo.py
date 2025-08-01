from interact import db, app
from interact.models import Seminar, Student, Slide, Answer

def populate_for_demo(user_id, nr_students_at_gf=5):
    student_names = ["Henk", "Tjeerd", "Karel", "Piet", "Jan", "Kees"]
    student_scores =       [2, 1, 0, 1, 2, 0]
    student_preparations = [4, 3, 3, 0, 1, 2]
    student_motivations =  [3, 2, 5, 1, 2, 4]

    with app.app_context():
        test = Seminar("Test", 6, user_id)
        test.active = True
        db.session.add(test)
        db.session.commit()

        slide1 = Slide(1, "Welkom", 1, test.id, "Welkom bij dit werkcollege")
        db.session.add(slide1)
        db.session.commit()

        slide2 = Slide(0, "Wat is 1+1?", 2, test.id)
        db.session.add(slide2)
        db.session.commit()
        answers = []
        answers.append(Answer("1", False, slide2.id))
        answers.append(Answer("2", True, slide2.id))
        answers.append(Answer("3", False, slide2.id))
        db.session.add_all(answers)
        db.session.commit()

        slide3 = Slide(0, "Wat is de tweede letter van het alfabet?", 3, test.id)
        db.session.add(slide3)
        db.session.commit()
        answers = []
        answers.append(Answer("A", False, slide3.id))
        answers.append(Answer("B", True, slide3.id))
        answers.append(Answer("C", False, slide3.id))
        db.session.add_all(answers)
        db.session.commit()

        slide4 = Slide(2, "Groepsvorming", 4, test.id)
        slide4.gf_type = 3 # similarity grouping
        slide4.gf_nr_per_group = 3
        db.session.add(slide4)
        db.session.commit()

        slide5 = Slide(1, "Bedankt", 5, test.id, "Tot ziens bij het volgende werkcollege")
        db.session.add(slide5)
        db.session.commit()

        students = []
        for i in range(6):
            student = Student(student_names[i], test.id)
            if i < nr_students_at_gf:
                student.current_slide = 4
                student.joined = True
                student.score = student_scores[i]
                student.preparation = student_preparations[i]
                student.motivation = student_motivations[i]
                student.reached_gf = True
            students.append(student)
        db.session.add_all(students)
        db.session.commit()