from pyfluka import vector
from random import uniform

a = lambda: uniform(-1, 1)
working = 0
not_working = 0
for i in range(int(1e5)):
    v1 = vector.Three(a(), a(), a())
    v2 = vector.Three(a(), a(), a())
    # print v1, v2
    mat = vector.rot_matrix_between_vectors(v1, v2)
    if not v2.parallel_to(mat.dot(v1)):
        not_working += 1
    else:
        working +=1
