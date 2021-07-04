from header import *


import csv
import pickle
from numpy import (
    full,
    log as ln,
)

from math import (
	log,
	exp,
	pow,
)



path = 'Data'

for file_name in file_lst:

	hyperparameters = []
	for i in POSSIBLE_P:
	  for j in POSSIBLE_Q:
	    for k in POSSIBLE_R:
	      tmp = (i,j,k)
	      hyperparameters.append(tmp)

	FILE_1 = open(f'{path}\\{file_name}\\G_{file_name}.dat', mode = 'rb')
	FILE_2 = open(f'{path}\\{file_name}\\L_{file_name}.dat', mode = 'rb')
	FILE_3 = open(f'{path}\\{file_name}\\T_{file_name}.dat', mode = 'rb')
	FILE_4 = open(f'{path}\\ground_truth.dat', 	   mode = 'rb')


	global_u     = pickle.load(FILE_1)
	local_u      = pickle.load(FILE_2)
	type_2_u_nrm = pickle.load(FILE_3)
	ground_truth = pickle.load(FILE_4)


	FILE_1.close()
	FILE_2.close()
	FILE_3.close()
	FILE_4.close()


	FILE = open(f'{path}\\Results\\result_{file_name}.csv', mode = 'w', newline = '')

	fnames = [
	          'P', 'Q', 'R', 'MSE',
	          'SA_C1', 'SA_C2', 'SA_C3', 'SA_C4', 'ASA', 
	          'DSC', 
	          'VPC', 'VPE'
	        ]

	writer = csv.DictWriter(FILE, fieldnames=fnames)    
	writer.writeheader()

	for P, Q, R in hyperparameters:

	  final_u            = full((N,Z,Y,X),0.0)
	  classified_img     = full((Z,Y,X),0)
	  
	  test_img_cluster   = {0:[],1:[],2:[],3:[]}
	  ground_img_cluster = {0:[],1:[],2:[],3:[]}
	  SA                 = {}

	  sum_vpc            = 0 
	  sum_vpe            = 0
	  correct_classified = 0
	  mis_classified     = 0
	  sum_sa  		     = 0
	  sum_dsc 		     = 0
	  
	  
	  '''
	  Calculating the final membership values
	  '''
	  for i in range(N):
	    for j in range(Z):
	      for k in range(Y):
	        for l in range(X):
	          su = 0  
	          for r in range(N):
	            su += pow(global_u[r][j][k][l],P) * pow(local_u[r][j][k][l],Q) * pow(type_2_u_nrm[r][j][k][l],R)

	          final_u[i][j][k][l] = ((pow(global_u[i][j][k][l],P) * pow(local_u[i][j][k][l],Q) * pow(type_2_u_nrm[i][j][k][l],R))/su)
	  

	  '''
	  Calculating the VPE and VPC
	  '''
	  for j in range(Z):
	    for k in range(Y):
	      for l in range(X):
	        for i in range(N):
	          sum_vpc += pow(final_u[i][j][k][l],2)
	          sum_vpe -= (final_u[i][j][k][l]*ln(final_u[i][j][k][l]))

	  vpc  = sum_vpc/(Z*Y*X)
	  vpe  = sum_vpe/(Z*Y*X)


	  '''
	  Return a 3-D image matrix with the classifying label.
	  0 BG, 1 CSF, 2 GM 3 WM
	  '''
	  for j in range(Z):
	    for k in range(Y):
	      for l in range(X):
	        c_group        = 0
	        max_membership = 0
	        for i in range(N):
	          if max_membership < final_u[i][j][k][l]:
	            max_membership = final_u[i][j][k][l]
	            c_group = i
	        classified_img[j][k][l]   = c_group
	  
	  '''
	  Misclassification Error
	  '''
	  for j in range(Z):
	  	for k in range(Y):
	  		for l in range(X):
	  			if ground_truth[j][k][l] in [0,1,2,3]:
	  				test_img_cluster[classified_img[j][k][l]].append((j,k,l))
	  				ground_img_cluster[ground_truth[j][k][l]].append((j,k,l))
	          
	  				if ground_truth[j][k][l] == classified_img[j][k][l]:
	  					correct_classified += 1
	  				else:
	  					mis_classified += 1

	  '''
	  Calculating the DSC
	  '''
	  for key in test_img_cluster:
	      common_points = intersection(test_img_cluster[key],ground_img_cluster[key])
	      x = len(common_points)
	      y = len(ground_img_cluster[key])

	      
	      SA[key] = (x/y)
	      sum_sa += (x/y)

	      dsc_nume = 2*len(common_points)
	      dsc_deno = (len(test_img_cluster[key]) + len(ground_img_cluster[key]))
	      sum_dsc += (dsc_nume/dsc_deno)

	  dsc    			= (sum_dsc/4)
	  avg_sa 			= (sum_sa/4)
	  error_percentage  = ((mis_classified/(correct_classified+mis_classified))*100)

	  record = {
	      'P': P, 'Q': Q, 'R': R,
	      'MSE': error_percentage,
	      'SA_C1': SA[0], 'SA_C2': SA[1], 'SA_C3': SA[2], 'SA_C4': SA[3],
	      'ASA': avg_sa,
	      'DSC': dsc,
	      'VPC': vpc,
	      'VPE': vpe,   
	  }

	  writer.writerow(record)
	  
	  print(f"For P = {P}, Q = {Q} and R = {R} written!!")

	print(f'Results are written at {path}\\Results\\result_{file_name}.csv')
	FILE.close()