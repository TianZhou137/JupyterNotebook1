# -*- coding: utf-8 -*-
"""
Created on Wed Nov 27 10:27:02 2019

@author: dell
"""

import numpy 
from scipy.optimize import leastsq
from scipy.optimize import fmin_slsqp
from modules.twobandfit_T import twobandfit_T
import pandas as pd
import time
from modules.data_to_csv import Dataplot
import random
e=1.602*pow(10,-19)

# Rename Columns
def arrange_dataframe(df):
	df.columns = ['B', 'Ryx']
	return df
def errors(parameter,B,Rxy_experiment):
    Rxy_T=twobandfit_T(parameter,B)
    B_middle=(len(B)+1)/2
    res=0
    factor=5##############################factor is weighting factor
    for number in range(len(B)):
        if number>=B_middle:      
            if number>len(B)-50:
                res=res + factor*(Rxy_T[number]-Rxy_experiment[number])**2
            if number<B_middle+50:
                res=res + 0.2*factor*(Rxy_T[number]-Rxy_experiment[number])**2
            res=res+(Rxy_T[number]-Rxy_experiment[number])**2
    return res
def run_parameter(filenames,Ts,bound):
	for number in range(len(filenames)):
		time_start=time.time()
		filename = 'Datas/' + filenames[number]
		df2 = pd.read_csv(filename)
		# Delta    Gama     Barrier Height    Spin Polarization
		bounds = bound[number]
		print("The range of fitting parameters.")
		print("np : ",bounds[0])
		print("up  : ",bounds[1])
		print("  ne   : ",bounds[2])
		print("  ue   : ",bounds[3])

		df2 = arrange_dataframe(df2)

		T = float(Ts[number])

		print("Temperature : ",T)
		parameter = [1*pow(10,-1), 0.1, 1*pow(10,-2), 0.1]#########初始化参数
		#parameters=[x*1.602 for x in parameter]
#		for i in range(4):
#			parameter[i] += random.uniform(0,0.1)
		print('Parameters: ',parameter)
		B = df2['B'].values
		Rxy_experiment = df2['Ryx'].values
		Rxy_experiment = list(Rxy_experiment)
		print("Data points : ",len(B))
#        ''' 梯度下降 '''
		# Weightness 
		#factor = 38
		# annealing
		myerror = []
		myparameter = []

		for i in range(10):
			
			r1, res_fun, res_nit, res_stat, res_message = fmin_slsqp(errors,parameter,args=(B,Rxy_experiment),iter = 100,bounds = bounds,full_output=1)
			myerror.append(res_fun)
			myparameter.append(r1)
			time_end=time.time()
			print('Parameters fitting cost : ',round(time_end-time_start,2),'s !')
			print('np:' + str(round(r1[0]*pow(10,19),4)))
			print('up:' + str(round(r1[1],4)))
			print('ne:' + str(round(r1[2]*pow(10,19),4)))
			print('ue:' + str(round(r1[3],4)))
			print("My error function values: ")
			print(errors(r1,B,Rxy_experiment))
			print("\n")
			for j in range(4):
				parameter[j] = r1[j] + 0.1*random.uniform(-0.01*(10-i),0.01*(10-i)) #回一个浮点数 N，取值范围为如果 x<y 则 x <= N <= y，如果 y<x 则y <= N <= x。
#				parameter[j] += random.uniform(-0.0003*(9-i)*(8-i)*(7-i),0.0003*(9-i)*(8-i)*(7-i))
				if parameter[j] < 0:
					parameter[j] = 0
		min_myerror = min(myerror)
		min_myerror_index = myerror.index(min_myerror)
		r1 = myparameter[min_myerror_index]
		time_end=time.time()
		print('Parameters fitting totally cost : ',round(time_end-time_start,2),'s !')
		print('np:' + str(round(r1[0]*pow(10,19),4)))
		print('up:' + str(round(r1[1],4)))
		print('ne:' + str(round(r1[2]*pow(10,19),4)))
		print('ue:' + str(round(r1[3],4)))
		print("My minmum error function values: ")
		print(min_myerror)
		#r1s=[r1[0]*pow(10,19),r1[1],r1[2]*pow(10,19),r1[3]]
		Dataplot(r1,T,df2,'B','Ryx',filename)

if __name__ == "__main__":
	filenames = input("输入文件名并以空格分开多个文件！\n")
	filenames = [str(n) for n in filenames.split()]
	print(filenames)
	Ts = input("输入测量温度并以空格分开多个数据温度！\n")
	Ts = [float(n) for n in Ts.split()]
	print(Ts)
	n = len(Ts)        
	bound = line = [[0]*4]*n
	param = ['np','up','ne','ue']
	print("参考Delta,Gama,Z,P范围 [(0.5,2),(0,2),(0,10),(0,1)] ！")        
	for i in range(n):
		for j in range(len(param)):
			line[i][j] = input("输入第"+str(i+1)+"文件参数"+param[j]+"范围并以空格分开！\n").split(" ")
			bound[i][j] = (float(line[i][j][0]),float(line[i][j][1]))
			print(bound[i][j])      

	#bound = [[(0.5,2),(0,2),(0,10),(0,1)],[(0.5,2),(0,2),(0,10),(0,1)]]
	run_parameter(filenames,Ts,bound)
