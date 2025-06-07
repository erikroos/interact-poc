from random import shuffle

class GroupForming():
    def __init__(self, nr_per_group, students, groups):
        self.nr_per_group = nr_per_group
        self.students = students
        self.groups = groups

    def divide(self, method):
        if method == 0:
            self.divide_random()
        elif method == 1:
            self.divide_mixlevel()
        elif method == 2:
            self.divide_samelevel()
        else: # fallback is random
            self.divide_random()
        self.put_students_in_groups()

    def divide_random(self):
        shuffle(self.students)
        
    def divide_mixlevel(self):
        sorted_students = sorted(self.students, key=lambda s: s.score)
        alternating_sorted = []
        while sorted_students:
            alternating_sorted.append(sorted_students.pop())
            if sorted_students:
                alternating_sorted.append(sorted_students.pop(0))
        self.students = alternating_sorted

    def divide_samelevel(self):
        self.students.sort(key=lambda s: s.score)

    def put_students_in_groups(self):
        group_index = 0
        student_index = 0
        for _ in range(len(self.groups)):
            for _ in range(self.nr_per_group):
                self.students[student_index].group_id = self.groups[group_index].id
                student_index += 1
                if student_index == len(self.students):
                    break
            group_index += 1

    def get_students(self):
        return self.students
    
    def get_groups(self):
        return self.groups