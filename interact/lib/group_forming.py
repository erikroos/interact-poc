from random import shuffle
from math import sqrt

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
        elif method == 3:
            self.similarity_grouping()

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

    def pairwise_similarity(self, s1, s2):
        """
        Helper function for similarity_grouping (see below).
        Original version made by Sietse Boonstra (RUG) for his Master's thesis.
        """
        v1 = [s1.motivation, s1.preparation, s1.score]
        v2 = [s2.motivation, s2.preparation, s2.score]
        squared_diffs = [(a - b) ** 2 for a, b in zip(v1, v2)]
        distance = sqrt(sum(squared_diffs))
        return -distance

    def similarity_grouping(self, homogeneous=True):
        """
        Forms groups by similarity/dissimilarity.
        Original version made by Sietse Boonstra (RUG) for his Master's thesis.
        """
        n = len(self.students)
        sim = [[0 for _ in range(n)] for _ in range(n)]
        for i in range(n):
            for j in range(i+1, n):
                s = self.pairwise_similarity(self.students[i], self.students[j])
                sim[i][j] = s
                sim[j][i] = s

        unassigned = set(range(n))

        # Make group sizes
        n_full = n // self.nr_per_group
        remainder = n % self.nr_per_group
        sizes = [self.nr_per_group] * n_full
        if remainder > 0:
            sizes.append(remainder)

        temp_student_list = []

        for sz in sizes:
            if not unassigned:
                break
            
            # Make pairs from the yet unassigned students
            pairs = [(i, j, sim[i][j]) for i in unassigned for j in unassigned if i < j]
            if not pairs:
                leftover = list(unassigned)
                temp_student_list += [self.students[idx] for idx in leftover]
                unassigned = set()
                break
            # Start with the pair with max/min similarity
            i0, j0, _ = max(pairs, key=(lambda x: x[2]) if homogeneous else (lambda x: -x[2]))
            group_idxs = {i0, j0}
            unassigned.remove(i0)
            unassigned.remove(j0)
            # Add unassigned students with max/min similarity until group is full
            while len(group_idxs) < sz and unassigned:
                scores = []
                for u in unassigned:
                    values = [sim[u][g] for g in group_idxs]
                    avg_sim = sum(values) / len(values)
                    scores.append((u, avg_sim))
                u_pick, _ = max(scores, key=(lambda x: x[1]) if homogeneous else (lambda x: -x[1]))
                group_idxs.add(u_pick)
                unassigned.remove(u_pick)

            temp_student_list += [self.students[i] for i in group_idxs]

        # Done. Add any remaining students
        if unassigned:
            temp_student_list += [self.students[i] for i in unassigned]
        # Put the students, now in the right order, back into self.students.
        # put_students_in_groups() will take care of the division into groups (yes, there's some double work here).
        self.students = temp_student_list

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