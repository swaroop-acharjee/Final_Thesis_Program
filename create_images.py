import os
from create_pgm import *
from header import *
from pickle import load
from numpy import full

FILE = open("data\\classified_img_143.dat", mode="rb")
classified_img = load(FILE)
FILE.close()

path = "data\\segmented_pgm"
if not os.path.exists(path):
    os.mkdir(path)
    os.mkdir(f"{path}\\CSF")
    os.mkdir(f"{path}\\GM")
    os.mkdir(f"{path}\\WM")

csf_img = full((Z, Y, X), 255)
gm_img = full((Z, Y, X), 255)
wm_img = full((Z, Y, X), 255)

for j in range(Z):
    for k in range(Y):
        for l in range(X):
            if classified_img[j][k][l] == 1:
                csf_img[j][k][l] = 0
            elif classified_img[j][k][l] == 2:
                gm_img[j][k][l] = 0
            elif classified_img[j][k][l] == 3:
                wm_img[j][k][l] = 0

COUNT = START
for j in range(Z):
    # Creating the CSF images
    create_pgm_file(
        width=X,
        height=Y,
        file_name=f"{path}\\CSF\\TEST_{COUNT}.pgm",
        comment=f"TEST_{COUNT}.pgm",
        img=csf_img[j],
        greylevel=255,
    )

    # Creating the GM images
    create_pgm_file(
        width=X,
        height=Y,
        file_name=f"{path}\\GM\\TEST_{COUNT}.pgm",
        comment=f"TEST_{COUNT}.pgm",
        img=gm_img[j],
        greylevel=255,
    )

    # Creating the WM images
    create_pgm_file(
        width=X,
        height=Y,
        file_name=f"{path}\\WM\\TEST_{COUNT}.pgm",
        comment=f"TEST_{COUNT}.pgm",
        img=wm_img[j],
        greylevel=255,
    )

    print(COUNT)
    COUNT += 1
