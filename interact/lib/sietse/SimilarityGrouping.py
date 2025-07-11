import numpy as np

TOPICS = ['A','B','C','D']
TOPIC_MAP = {t: [int(i == j) for j in range(len(TOPICS))] for i, t in enumerate(TOPICS)}

def pairwise_similarity(s1, s2):
    v1 = np.array([s1['motivation'], s1['preparation']] + TOPIC_MAP[s1['topic']])
    v2 = np.array([s2['motivation'], s2['preparation']] + TOPIC_MAP[s2['topic']])
    return -np.linalg.norm(v1 - v2)

def similarity_grouping(students, group_size=4, group_sizes=None, homogeneous=True):
    """
    Forms groups by similarity/dissimilarity, supporting either a fixed group_size (old) or a list of group_sizes (preferred).
    """
    n = len(students)
    sim = np.zeros((n, n))
    for i in range(n):
        for j in range(i+1, n):
            s = pairwise_similarity(students[i], students[j])
            sim[i, j] = s
            sim[j, i] = s

    unassigned = set(range(n))
    groups = []

    # Decide group sizes
    if group_sizes is not None:
        sizes = group_sizes.copy()
    else:
        n_full = n // group_size
        remainder = n % group_size
        sizes = [group_size] * n_full
        if remainder > 0:
            sizes.append(remainder)

    for sz in sizes:
        if not unassigned:
            break
        # Start with the pair with max/min similarity
        pairs = [(i, j, sim[i, j]) for i in unassigned for j in unassigned if i < j]
        if not pairs:
            leftover = list(unassigned)
            groups.append([students[idx] for idx in leftover])
            unassigned = set()
            break

        key = (lambda x: x[2]) if homogeneous else (lambda x: -x[2])
        i0, j0, _ = max(pairs, key=key)
        group_idxs = {i0, j0}
        unassigned.remove(i0)
        unassigned.remove(j0)

        while len(group_idxs) < sz and unassigned:
            scores = []
            for u in unassigned:
                avg_sim = np.mean([sim[u, g] for g in group_idxs])
                scores.append((u, avg_sim))
            u_pick, _ = max(scores, key=(lambda x: x[1]) if homogeneous else (lambda x: -x[1]))
            group_idxs.add(u_pick)
            unassigned.remove(u_pick)

        groups.append([students[i] for i in group_idxs])

    if unassigned:
        groups.append([students[i] for i in unassigned])

    return groups
