from header import *
import pickle
import os


if not os.path.isfile('Data\\ground_truth.dat'):
    # Creating the ground truth file
    ground_truth = []
    for j in range(START, END):
        ground_truth.append(read_pgm(f'Data\\Ground Truth\\TEST_{j}.pgm'))

    FILE = open(f'Data\\ground_truth.dat',  mode = 'wb')
    pickle.dump(ground_truth, FILE)
    FILE.close()
    print("Ground Truth is created!!")
else:
    print("Ground Truth Already created!!!")


# Creating the image files
for file in file_lst:

	# Creating a 3-D Matrix of the Image Voxels
	img_vol 	 = []

	for j in range(START,END):
		img_vol.append(read_pgm(f'Data\\{file}\\BV_{file}\\TEST_{j}.pgm'))

	FILE = open(f'Data\\{file}\\img_{file}.dat',  mode = 'wb')
	pickle.dump(img_vol, FILE)
	FILE.close()

	print("FILES created!!")