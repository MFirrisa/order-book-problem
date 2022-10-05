#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 00:08:25 2022

@author: michaelfirrisa
"""
import numpy as np
import pandas as pd

#I first load the text file into a list, where each list entry corresponds
#to an add order or reduce order. Here, I chose the first 100 orders
#(the data itself has well over 100,000 orders).

book = open("pricer.txt").readlines()

short_book=book[0:100]

#Since I am reading in a text file, the elements of each order entry are
#strings. I have to first convert the numbers to floats and integers before
#I can carry out any meaningful computation.

new_book=[]

for order in short_book:
    L0=order.split(" ")
    L1=[item.replace("\n", '')  for item in L0]
    new_book.append(L1)

for order in new_book:
    if len(order)==6:
        order[0]=int(order[0])
        order[4]=float(order[4])
        order[5]=int(order[5])
    if len(order)==4:
        order[0]=int(order[0])
        order[3]=int(order[3])


#Before I write the main function, I define a function which takes in a list
#of tuples and an integer. In the context of this problem, when called, it will
#return the resulting expense, or income, based on a specified number of shares. 


def income_expense(list_of_price_and_size,target_size):
    income_expense=0
    share_count=0
    for price_and_size in list_of_price_and_size:
        if share_count<=target_size:
            income_expense+=price_and_size[0]*np.minimum(target_size-share_count,price_and_size[1])
            share_count+=price_and_size[1]
    return income_expense
            
        
#The function I'll define below is the meat of the problem.    

def pricer(target_size):
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
     
    for order in new_book:
        if 'B' in order:
            income.append(order)
        if 'S' in order:
            expense.append(order)
        if 'R' in order:
            to_be_removed=[]
            
            for buy_order in income:
                if order[2]==buy_order[2]:
                    m=buy_order[5]-order[3]
                    if m > 0:
                        buy_order[5]=m
                    else:
                        to_be_removed=buy_order
           
            for sell_order in expense:
                if order[2]==sell_order[2]:
                    m=sell_order[5]-order[3]
                    if m > 0:
                        sell_order[5]=m
                    else:
                        to_be_removed=sell_order
                
            if to_be_removed in income:
                 income.remove(to_be_removed)
            
            if to_be_removed in expense:
                     expense.remove(to_be_removed)
                 
        #Now, the function I defined earlier takes in a list of tuples and
        #an integer representing the number of shares the client would like to
        #buy/sell. In order to call the income_expense function successfully,
        #I will create two separate lists of tuples (first entry being the
        #price per share, the second being the total number of shares offered)
        #based on the newly created 'buy' and 'sell' lists. Further, since I
        #want to sell at the highest price possible, and buy at the lowest,
        #I will order the lists of tuples according to the values of the first
        #tuple entries. 
                
        expense_sorted=[]
        income_sorted=[]
        
        for sell_order in expense:
            expense_sorted.append([sell_order[4],sell_order[5]])
        
        for buy_order in income:
            income_sorted.append([buy_order[4],buy_order[5]])
            
        expense_sorted.sort(key = lambda y: y[0])
        income_sorted.sort(key = lambda y: y[0], reverse=True)
        
        #I am now ready to calculate the correct output based on the 
        #client's desired number of shares as each new order comes in. On a 
        #technical note, we need to take into account that an output should 
        #only be generated if a newly received order changes the previous 
        #output.
        
        total_sell_share=0
        for buy_order in income_sorted:
            total_sell_share+=buy_order[1]
        if total_sell_share>=target_size:
            m=income_expense(income_sorted, target_size)
            m_rounded_to_two_decimal_places='{0:.2f}'.format(m)
            if m_rounded_to_two_decimal_places not in prev_income_output:
                print([order[0],'S',m_rounded_to_two_decimal_places])
                prev_income_output=[order[0],'S',m_rounded_to_two_decimal_places]
        if total_sell_share < target_size and prev_income_output != [] and 'NA' not in\
            prev_income_output:
            print([order[0],'S','NA'])
            prev_income_output=[order[0],'S','NA']
        
        total_buy_share=0
        for sell_order in expense_sorted:
            total_buy_share+=sell_order[1]
        if total_buy_share>=target_size:
            m=income_expense(expense_sorted, target_size)
            m_rounded_to_two_decimal_places='{0:.2f}'.format(m)
            if m_rounded_to_two_decimal_places not in prev_expense_output:
                print([order[0],'B',m_rounded_to_two_decimal_places])
                prev_expense_output=[order[0],'B',m_rounded_to_two_decimal_places]
        if total_buy_share < target_size and prev_expense_output != [] and 'NA' not in\
            prev_expense_output:
            print([order[0],'B','NA'])
            prev_expense_output=[order[0],'B','NA']
        
        
print(pricer(200))

        
        
    
    
