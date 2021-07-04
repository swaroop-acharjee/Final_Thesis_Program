from header import *

from numpy import (
    full,
    log as ln,
)

from math import (
    log,
    exp,
    pow,
)

from statistics import (
    variance,
    mean,
)

import pickle

for FILE in file_lst:
    C = [13.01, 45.01, 100.01, 115.01]  # Values of the initial Clusters
    FOLDER = f"Data\\{FILE}\\"

    FILE_OBJ = open(f"{FOLDER}img_{FILE}.dat", mode="rb")
    img_vol = pickle.load(FILE_OBJ)

    FILE_OBJ.close()

    global_u = full((N, Z, Y, X), 0.0)
    local_u = full((N, Z, Y, X), 0.0)
    type_2_u = full((N, Z, Y, X), 0.0)
    type_2_u_nrm = full((N, Z, Y, X), 0.0)

    # Calculating the initial values of the membership functions
    for i in range(N):
        for j in range(Z):
            for k in range(Y):
                for l in range(X):
                    temp = 0
                    numerator = (img_vol[j][k][l] - C[i]) ** 2
                    for r in range(N):
                        denominator = (img_vol[j][k][l] - C[r]) ** 2
                        temp += (numerator / denominator) ** p
                    local_u[i][j][k][l] = 1 / temp
                    global_u[i][j][k][l] = 1 / temp

    for _ in range(N_IT):
        # Calculation of the global membership functions
        for i in range(N):
            for j in range(Z):
                for k in range(Y):
                    for l in range(X):
                        distance = (C[i] - img_vol[j][k][l]) ** 2
                        ln_value = log(global_u[i][j][k][l] ** M)
                        numerator = abs(distance - ln_value - 1)

                        temp = 0
                        for r in range(N):
                            distance = (C[r] - img_vol[j][k][l]) ** 2
                            ln_value = log(global_u[r][j][k][l] ** M)
                            denominator = abs(distance - ln_value - 1)

                            temp += (numerator / denominator) ** p

                        global_u[i][j][k][l] = 1 / temp

        # Calculate the Local membership functions
        for i in range(N):
            for j in range(Z):
                for k in range(Y):
                    for l in range(X):
                        coordinates = find_neighbor(j, k, l, Z, Y, X)

                        f = likelihood(img_vol, local_u[i], coordinates)
                        d = mean_distance(img_vol, coordinates, C[i])

                        ln_value = log(local_u[i][j][k][l] ** M)
                        numerator = abs(f * d - ln_value - 1)

                        temp = 0
                        for r in range(N):
                            f = likelihood(img_vol, local_u[r], coordinates)
                            d = mean_distance(img_vol, coordinates, C[r])

                            ln_value = log(local_u[r][j][k][l] ** M)
                            denominator = abs(f * d - ln_value - 1)

                            temp += (numerator / denominator) ** p

                        local_u[i][j][k][l] = 1 / temp

        # Calculating the type-2 Fuzzy set
        for i in range(N):
            for j in range(Z):
                for k in range(Y):
                    for l in range(X):
                        coordinates = find_neighbor(j, k, l, Z, Y, X)

                        list_local_u = []
                        list_global_u = []

                        for x_j, x_k, x_l in coordinates:
                            list_local_u.append(local_u[i][x_j][x_k][x_l])
                            list_global_u.append(global_u[i][x_j][x_k][x_l])

                        sum_numerator = 0
                        sum_denominator = 0
                        for indx in range(len(list_local_u)):
                            sum_numerator += list_global_u[indx] * list_local_u[indx]
                            sum_denominator += list_local_u[indx]

                        type_2_u[i][j][k][l] = sum_numerator / sum_denominator

        # Normalization of the values
        for i in range(N):
            for j in range(Z):
                for k in range(Y):
                    for l in range(X):
                        su = 0
                        for r in range(N):
                            su += type_2_u[r][j][k][l]
                        type_2_u_nrm[i][j][k][l] = type_2_u[i][j][k][l] / su

        new_C = [0, 0, 0, 0]

        for i in range(N):
            numerator = 0
            denominator = 0

            for j in range(Z):
                for k in range(Y):
                    for l in range(X):
                        coordinates = find_neighbor(j, k, l, Z, Y, X)

                        f = likelihood(img_vol, local_u[i], coordinates)
                        a_mean = mean_pixels(img_vol, coordinates)

                        n_a = 0.4 * (global_u[i][j][k][l] ** M)
                        n_b = 0.3 * (local_u[i][j][k][l] ** M * f)
                        n_c = 0.3 * (type_2_u_nrm[i][j][k][l] ** M)

                        numerator += (
                            n_a * img_vol[j][k][l]
                            + n_b * a_mean
                            + n_c * img_vol[j][k][l]
                        )
                        denominator += n_a + n_b + n_c

            new_C[i] = numerator / denominator

        e_0 = abs(C[0] - new_C[0])
        e_1 = abs(C[1] - new_C[1])
        e_2 = abs(C[2] - new_C[2])
        e_3 = abs(C[3] - new_C[3])
        avg_error = (e_0 + e_1 + e_2 + e_3) / 4

        C = new_C

        print()
        print((_ + 1), ":", avg_error, end="\t\t")
        # print(C)
        print()

        if avg_error < E:
            break

    FILE_1 = open(f"{FOLDER}G_{FILE}.dat", mode="wb")
    FILE_2 = open(f"{FOLDER}L_{FILE}.dat", mode="wb")
    FILE_3 = open(f"{FOLDER}T_{FILE}.dat", mode="wb")

    pickle.dump(global_u, FILE_1)
    pickle.dump(local_u, FILE_2)
    pickle.dump(type_2_u_nrm, FILE_3)

    FILE_1.close()
    FILE_2.close()
    FILE_3.close()

    print(f"Congratulations, files are ready for {FILE}")
