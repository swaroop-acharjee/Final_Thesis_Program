import matplotlib.pyplot as plt
import numpy as np
import math
from statistics import mean

# CONSTANTS
START = 50
END   = 100


Z 	  = (END-START)						# depth
Y 	  = 217								# height
X     = 181								# col
N_IT  = 100


A     = 0.7								# Value of alpha
N     = 4

M     = 2.5                             # Value of meu
E     = 0.01
p 	  = (1/(M-1))


'''
Include the names of the file that you want to test
in the list below!!
'''
# file_lst  = [
# 					'0_0', '0_20', '0_40',
# 					'1_0', '1_20', '1_40',
# 					'3_0', '3_20', '3_40',
# 					'5_0', '5_20', '5_40',
# 					'7_0', '7_20', '7_40',
# 					'9_0', '9_20', '9_40',
# 			]

file_lst = ['9_40']

'''
Possible values of the parameters
'''
POSSIBLE_P = [1]
POSSIBLE_Q = [4]
POSSIBLE_R = [3,4]


# FUNCTIONS
def read_pgm(file_path:str)->list:
	with open(file_path,mode='rb') as FILE:
		records = [row.decode('utf-8') for row in FILE.readlines()]

		img = []
		for i in records[4:]:
			temp = [int(x) for x in i.split()] 
			img.append(temp)

		return img


def find_neighbor(j:int,k:int,l:int,Z:int,Y:int,X:int)->list:
	coordinates = 	[]
	corr_list 	= 	[
						(-1,-1,-1), (-1,-1,0),(-1,-1,1),
						(-1,0,-1), (-1,0,1), (-1,0,0),
						(-1,1,-1),(-1,1,0),(-1,1,1),

						(0,-1,-1), (0,-1,0),(0,-1,1),
						(0,0,-1), (0,0,1),
						(0,1,-1),(0,1,0),(0,1,1),

						(1,-1,-1), (1,-1,0),(1,-1,1),
						(1,0,-1), (1,0,1), (1,0,0),
						(1,1,-1),(1,1,0),(1,1,1), 
					]

	for c in corr_list:
		new_j = j + c[0]
		new_k = k + c[1]
		new_l = l + c[2]

		condition_1 = (new_j >= 0) and (new_k >= 0) and (new_l >= 0) 		# Checking if all the index are positive
		condition_2 = new_j <= (Z-1) 										# Checking if z is in the range
		condition_3 = new_k <= (Y-1) 										# Checking if y is in the range
		condition_4 = new_l <= (X-1) 										# Checking if x is in the range

		if condition_1 and condition_2 and condition_3 and condition_4:
			temp  = (new_j,new_k,new_l)
			coordinates.append(temp)

	return coordinates


def mean_distance(img:list,lst_coordinates:list,cluster_center:int)->list:
	sum_m = 0
	N     = len(lst_coordinates)
	
	for j,k,l in lst_coordinates:
			sum_m += (cluster_center - img[j][k][l])**2

	return sum_m/N


def mean_pixels(img:list,lst_coordinates:list)->float:
	sum_m = 0
	N     = len(lst_coordinates)
	
	for j,k,l in lst_coordinates:
		sum_m += img[j][k][l]
	
	return (sum_m/N)

def likelihood(img:list,local_mem:list,lst_coordinates)->list:
	nume = 0
	deno = 0.0001

	for j,k,l in lst_coordinates:
		nume += local_mem[j][k][l]*img[j][k][l]
		deno += img[j][k][l]

	return (nume/deno)
	
def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))

	