# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 22:58:17 2019

@author: dell
"""

e=1.602
    #N=ne*e
    #P=np*e

import matplotlib.pyplot as plt
def twobandfit_T(parameters,B):
    P,up,N,ue=parameters
    P=P*e
    N=N*e
    #Rxx=(B**2*ne*ue*up**2 + B**2*np*ue**2*up + ne*ue + np*up)/(e*(B**2*ne**2*ue**2*up**2 + 2*B**2*ne*np*ue**2*up**2 + B**2*np**2*ue**2*up**2 + ne**2*ue**2 + 2*ne*np*ue*up + np**2*up**2))
    Rxy=B*(B**2*N*ue**2*up**2 - B**2*P*ue**2*up**2 + N*ue**2 - P*up**2)/((B**2*N**2*ue**2*up**2 - 2*B**2*N*P*ue**2*up**2 + B**2*P**2*ue**2*up**2 + N**2*ue**2 + 2*N*P*ue*up + P**2*up**2))
    #plt.figure()
    #plt.plot(B,Rxx)
    #plt.plot(B,Rxy)
    #plt.show()
    return Rxy
