#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 08:01:53 2022

@author: michaelfirrisa
"""


#A place to test my code to make sure it performs as expected. Not
#part of the problem and can be ignored.


import numpy as np

empty=[]

empty.append([1,2])
empty.append([3,4])
empty.append([2,1])

empty1=[[1,2],[3,2],[2,1]]

empty=np.asanyarray(empty)

print(np.sort(empty,axis=0))

empty1.sort(key = lambda y: y[0], reverse=True)

print(empty1)

x=[]

if x in empty1:
    empty1.remove(x)

print(empty1)

#print(np.minimum(4,3))


def income_expense(L,x):
    income=0
    share_count=0
    for l in L:
        if share_count<=x:
            income+=l[0]*np.minimum(x-share_count,l[1])
            share_count+=l[1]
    print(income)
    

L=[[44.18, 157], [44.1, 100]]
x=200

print(income_expense(L,x))