#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 00:08:25 2022

@author: michaelfirrisa
"""
import numpy as np
import pandas as pd

#We first load the text file into a list, where each list entry corresponds\
#to an add order or reduce order. Further, we choose the first 100 orders
#(the data itself has well over 100,000 orders).

book = open("pricer.txt").readlines()

short_book=book[0:100]

#Since we are reading in a text file, the elements of each order entry are
#strings. We have to first convert the numbers to floats and integers before
#we can carry out any meaningful computation.

new_book=[]

for i in short_book:
    L0=i.split(" ")
    L1=[item.replace("\n", '')  for item in L0]
    new_book.append(L1)

for i in new_book:
    if len(i)==6:
        i[0]=int(i[0])
        i[4]=float(i[4])
        i[5]=int(i[5])
    if len(i)==4:
        i[0]=int(i[0])
        i[3]=int(i[3])


#Before we write the main function, we define a function which takes in a list
#of tuples and an integer. In the context of this problem, when called, it will
#return the resulting expense, or income, based on a specified number of shares. 


def income_expense(L,x):
    income_expense=0
    share_count=0
    for l in L:
        if share_count<=x:
            income_expense+=l[0]*np.minimum(x-share_count,l[1])
            share_count+=l[1]
    return income_expense
            
        
#The function we define below is the meat of the problem.    

def pricer(x):
    #There are two main tasks we have, as we read through each order, we want
    # to let our client know what their income, or expense, will be based on
    #whether they are selling, or buying, a set number of shares. To make this
    #task easier, we will create separate lists for 'sell' orders and 'buy'
    #orders. We will also update both lists as necessary when we receive a
    #reduce order.
    
    expense=[]
    income=[]
    prev_income_output=[]
    prev_expense_output=[]
     
    for i in new_book:
        if 'B' in i:
            income.append(i)
        if 'S' in i:
            expense.append(i)
        if 'R' in i:
            to_be_removed=[]
            
            for j in income:
                if i[2]==j[2]:
                    m=j[5]-i[3]
                    if m > 0:
                        j[5]=m
                    else:
                        to_be_removed=j
           
            for j in expense:
                if i[2]==j[2]:
                    m=j[5]-i[3]
                    if m > 0:
                        j[5]=m
                    else:
                        to_be_removed=j
                
            if to_be_removed in income:
                 income.remove(to_be_removed)
            
            if to_be_removed in expense:
                     expense.remove(to_be_removed)
                 
        #Now, the function we defined earlier takes in a list of tuples and
        #an integer representing the number of shares the client would like to
        #buy/share. In order to call the income_expense function successfully,
        #we will create two separate lists of tuples (first entry being the
        #price per share, the second being the total number of shares offered)
        #based on our newly created 'buy' and 'sell' lists. Further, since we
        #want to sell at the highest price possible, and buy at the lowest,
        #we will order our lists of tuples according to the values of the first
        #tuple entries. 
                
        expense_sorted=[]
        income_sorted=[]
        
        for j in expense:
            expense_sorted.append([j[4],j[5]])
        
        for j in income:
            income_sorted.append([j[4],j[5]])
            
        expense_sorted.sort(key = lambda y: y[0])
        income_sorted.sort(key = lambda y: y[0], reverse=True)
        
        #We are now ready to calculate the correct output based on the 
        #client's desired number of shares as each new order comes in. On a 
        #techinical note, we need to take into account that an output should 
        #only be generated if a newly received order changes the previous 
        #output.
        
        total_sell_share=0
        for j in income_sorted:
            total_sell_share+=j[1]
        if total_sell_share>=x:
            m=income_expense(income_sorted, x)
            m_round='{0:.2f}'.format(m)
            if m_round not in prev_income_output:
                print([i[0],'S',m_round])
                prev_income_output=[i[0],'S',m_round]
        if total_sell_share < x and prev_income_output != [] and 'NA' not in\
            prev_income_output:
            print([i[0],'S','NA'])
            prev_income_output=[i[0],'S','NA']
        
        total_buy_share=0
        for j in expense_sorted:
            total_buy_share+=j[1]
        if total_buy_share>=x:
            m=income_expense(expense_sorted, x)
            m_round='{0:.2f}'.format(m)
            if m_round not in prev_expense_output:
                print([i[0],'B',m_round])
                prev_expense_output=[i[0],'B',m_round]
        if total_buy_share < x and prev_expense_output != [] and 'NA' not in\
            prev_expense_output:
            print([i[0],'B','NA'])
            prev_expense_output=[i[0],'B','NA']
        
        
print(pricer(200))

        
        
        
        
        
        
        
            
            
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    