from interact.teachers.models import Student, Group

class GroupForming():
    def __init__(self, students, groups):
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

    def divide_random(self):
        pass

    def divide_mixlevel(self):
        pass

    def divide_samelevel(self):
        pass

    def get_students(self):
        return self.students
    
    def get_groups(self):
        return self.groups