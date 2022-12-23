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


def base_case(X, Y):
    # loop through all characters in y and find the one with the lowest mismatch cost
    min_cost = delta * 2
    for i in range(len(Y)):
        char_1 = X[0]
        char_2 = Y[i]
        ind_1 = character_dict[char_1]
        ind_2 = character_dict[char_2]

        if alpha[ind_1, ind_2] < min_cost:

            min_cost = alpha[ind_1, ind_2]

            aligned_y = Y

            # put X[0] in min index, all other indices are gaps
            aligned_x = ""
            for j in range(i):
                aligned_x = aligned_x + '_'
            aligned_x = aligned_x + X[0]
            # print(i+2, len(Y))
            for j in range(i + 1, len(Y)):
                aligned_x = aligned_x + "_"

    # if the lowest cost is two gaps, put a gap before y
    if min_cost == delta * 2:
        aligned_x = X[0]
        for i in range(len(Y)):
            aligned_x = aligned_x + "_"

        aligned_y = "_" + Y

    return aligned_x, aligned_y


def gaps(s):
    res = ""
    for i in range(len(s)):
        res = res + "_"
    return res


def calculate_alignment_cost(X, Y):
    cost = 0
    for i in range(len(X)):
        if X[i] == "_" or Y[i] == "_":
            cost = cost + delta
        else:
            ind_1 = character_dict[X[i]]
            ind_2 = character_dict[Y[i]]
            cost = cost + alpha[ind_1, ind_2]
    return cost

def memory_efficient_sequence_alignment(X, Y):
    # base cases
    if len(X) == 0:
        return gaps(Y), Y

    if len(Y) == 0:
        return X, gaps(X)

    if len(X) == 1:
        res = base_case(X, Y)
        # print("res: " + str(res))
        return res

    if len(Y) == 1:
        res = base_case(Y, X)
        # print("res: " + str(res))
        return res[1], res[0]

    k = len(X) // 2 - 1

    Xl = X[0:k + 1]
    Xr = X[k + 1:len(X)]

    prev_col_l = np.zeros((len(Y) + 1, ))
    for j in range(0, len(Y) + 1):
        prev_col_l[j] = j * delta
    col_l = np.zeros((len(Y) + 1,))
    col_l[0] = delta

    for i in range(1, len(Xl) + 1):
        col_l = np.zeros((len(Y) + 1,))
        col_l[0] = delta * i

        for j in range(1, len(Y) + 1):
            char_1 = Xl[i - 1]
            char_2 = Y[j - 1]

            ind_1 = character_dict[char_1]
            ind_2 = character_dict[char_2]

            col_l[j] = min(prev_col_l[j - 1] + alpha[ind_1, ind_2], prev_col_l[j] + delta, col_l[j - 1] + delta)

        prev_col_l = col_l

    # reverse string

    Xr_copy = deepcopy(Xr)
    Xr_copy = Xr_copy[::-1]

    Y_copy = deepcopy(Y)
    Y_copy = Y_copy[::-1]

    prev_col_r = np.zeros((len(Y_copy) + 1, ))
    for j in range(0, len(Y_copy) + 1):
        prev_col_r[j] = j * delta

    col_r = np.zeros((len(Y_copy) + 1,))
    col_r[0] = delta
    for i in range(1, len(Xr_copy) + 1):
        col_r = np.zeros((len(Y_copy) + 1,))
        col_r[0] = delta * i
        for j in range(1, len(Y_copy) + 1):
            char_1 = Xr_copy[i - 1]
            char_2 = Y_copy[j - 1]

            ind_1 = character_dict[char_1]
            ind_2 = character_dict[char_2]

            col_r[j] = min(prev_col_r[j - 1] + alpha[ind_1, ind_2], prev_col_r[j] + delta, col_r[j - 1] + delta)

        prev_col_r = col_r

    sums = np.zeros(len(Y) + 1)
    for i in range(len(Y) + 1):
        sums[i] = col_l[i] + col_r[len(Y) - i]

    min_val = np.inf
    min_ind = None

    for i in range(len(Y) + 1):
        if sums[i] < min_val:
            min_val = sums[i]
            min_ind = i

    prev_col_l = None
    col_l = None
    prev_col_r = None
    col_r = None

    aligned_xl, aligned_yl = memory_efficient_sequence_alignment(Xl, Y[0:min_ind])
    aligned_xr, aligned_yr = memory_efficient_sequence_alignment(Xr, Y[min_ind:])

    return aligned_xl + aligned_xr, aligned_yl + aligned_yr

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
    aligned_x, aligned_y = memory_efficient_sequence_alignment(sequence_1, sequence_2)
    cost = calculate_alignment_cost(aligned_x, aligned_y)
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



