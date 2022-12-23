import numpy as np
from copy import deepcopy
import time
import sys
import time
import tracemalloc

alpha = np.array([
    [0, 110, 48, 94],
    [110, 0, 118, 48],
    [48, 118, 0, 110],
    [94, 48, 110, 0]
])

delta = 30

character_dict = {
    'A': 0,
    'C': 1,
    'G': 2,
    'T': 3
}


def sequence_alignment_cost(a, b):
    # print(len(a), len(b))
    opt = []
    for i in range(len(a) + 1):
        row = []
        for j in range(len(b) + 1):
            row.append(0)
        opt.append(row)

    # initialize matrix
    for i in range(0, len(a) + 1):
        opt[i][0] = i * delta

    for j in range(0, len(b) + 1):
        opt[0][j] = j * delta

    # bottom up pass
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            char_1 = a[i - 1]
            char_2 = b[j - 1]

            ind_1 = character_dict[char_1]
            ind_2 = character_dict[char_2]

            opt[i][j] = min(opt[i][j - 1] + delta, opt[i - 1][j] + delta, opt[i - 1][j - 1] + alpha[ind_1, ind_2])

    # top down pass
    aligned_x = ""
    aligned_y = ""
    i = len(a)
    j = len(b)

    count = 0
    while i >= 1 or j >= 1:
        count += 1

        char_1 = a[i - 1]
        char_2 = b[j - 1]

        ind_1 = character_dict[char_1]
        ind_2 = character_dict[char_2]

        bottom_left = opt[i - 1][j - 1] + alpha[ind_1][ind_2]
        left = opt[i - 1][j] + delta
        bottom = opt[i][j - 1] + delta

        if bottom_left == opt[i][j]:
            aligned_x = a[i - 1] + aligned_x
            aligned_y = b[j - 1] + aligned_y
            i = i - 1
            j = j - 1
        elif bottom == opt[i][j]:
            aligned_x = '_' + aligned_x
            aligned_y = b[j - 1] + aligned_y
            j = j - 1
        elif left == opt[i][j]:
            aligned_x = a[i - 1] + aligned_x
            aligned_y = '_' + aligned_y
            i = i - 1

    return opt[len(a)][len(b)], aligned_x, aligned_y

def generate_input_string(path):
    first_ind = []
    second_ind = []
    first_str = ""
    second_str = ""

    with open(path, "r") as f:
        flag = False
        number_flag = False
        for l in f:
            l = l.replace("\n", "")
            if not l.isnumeric():
                if flag:
                    second_str = l
                    number_flag = True
                else:
                    first_str = l
                flag = True
            else:
                if number_flag:
                    second_ind.append(int(l))
                else:
                    first_ind.append(int(l))

    for ind in first_ind:
        first_str = first_str[0:ind + 1] + first_str + first_str[ind + 1:]

    for ind in second_ind:
        second_str = second_str[0:ind + 1] + second_str + second_str[ind + 1:]
    return first_str, second_str


if __name__ == "__main__":
    input_path = sys.argv[1]
    output_path = sys.argv[2]

    tracemalloc.start()
    sequence_1, sequence_2 = generate_input_string(input_path)
    start_time = time.time()
    cost, aligned_x, aligned_y = sequence_alignment_cost(sequence_1, sequence_2)
    end_time = time.time()
    time_taken = (end_time - start_time) * 1000
    snapshot = tracemalloc.take_snapshot()
    curr, peak = tracemalloc.get_traced_memory()
    
    with open(output_path, "w") as f:
        f.write(str(cost) + '\n')
        f.write(str(aligned_x) + '\n')
        f.write(str(aligned_y) + '\n')
        f.write(str(time_taken) + '\n')
        f.write(str(peak) + '\n')



