#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 00:08:25 2022

@author: michaelfirrisa
"""
import numpy as np
import pandas as pd

# To begin, I first load the data text file into a list, where each list entry corresponds
# to an add order or reduce order. 

book = open("pricer.txt").readlines()

# Here, I chose the first 100 orders. The data itself has well over 100,000 orders.

short_book=book[0:100]

# Since I am reading in a text file, each order is added as a single string value.
# For instance, if I am to print short_book[0] (the first order entry), a single string value

#'28800562 A c B 44.10 100'

# will be returned. In order to carry out any meaningful computation, I will first need 
# to break up these strings values into their individual components. Once I have 
# done that, I can then convert the numerical values from strings to 
# integers and floats. To that end, the goal is to create a new list, new_book,
# where each order is now a list (yes, we will have a list of lists), containing
# the necessary string, integer, and float types.


new_book=[]

for order_string in short_book:
    # The code below takes an order from short_book, which is a single string value, 
    # and breaks it up into a list of string values. For example, short_book[0]
    # will now look like ['28800538', 'A', 'b', 'S', '44.26', '100\n']
    
    order_list_of_strings=order_string.split(" ")
    # The '\n' denotes a new line in a text file. But, in order to convert something
    # like '100\n' to an interger, I will have to get rid of the '\n.' So, I will
    # make the modification as follows:
    
    order_list_of_strings_modified=[item.replace("\n", '')  for item in order_list_of_strings]
    new_book.append(order_list_of_strings_modified)
    
# Now, printing the first order, new_book[0], will return ['28800538', 'A', 'b', 'S', '44.26', '100'].
# But, each entry in this list is still a string value. In order to do any calculation
# I will need to convert the numerical entries to integers and floats. For the add
# orders, there are six entries; it is the 1st, 5th, and 6th entries which
# have numberical values. The reduce orders have four entries, with the first and 
# last entries being numberical values. The following code accounts for this and changes all
# of the numerical values to the desired types.

for order in new_book:
    if len(order)==6:
        order[0]=int(order[0])
        order[4]=float(order[4])
        order[5]=int(order[5])
    if len(order)==4:
        order[0]=int(order[0])
        order[3]=int(order[3])


# Before I write the main function, I define a function which takes in a list
# of tuples and an integer. In the context of this problem, when called, it will
# return the resulting expense, or income, based on a specified number of target shares. 


def income_expense(list_of_price_and_size,target_size):
    income_expense=0
    share_count=0
    for price_and_size in list_of_price_and_size:
        if share_count<=target_size:
            income_expense+=price_and_size[0]*np.minimum(target_size-share_count,price_and_size[1])
            share_count+=price_and_size[1]
    return income_expense
            
        
# The function I'll define below is the meat of the problem.    

def pricer(target_size):
    # This function will perform the following: while going through each order, the
    # client will be continuously informed what their income (or expense) will be once
    # the number of shares available reaches the desired target size. To make this
    # task easier, I will create separate lists for 'sell' orders and 'buy'
    # orders. The lists will be updated as necessary when there is a
    # reduce order.
    
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
                 
        # Now, the function I defined earlier takes in a list of tuples and
        # an integer representing the number of shares the client would like to
        # buy/sell. In order to call the income_expense function successfully,
        # I will create two separate lists of tuples (first entry being the
        # price per share, the second being the total number of shares offered)
        # based on the newly created 'buy' and 'sell' lists. Further, since the client will
        # want to sell at the highest price possible, and buy at the lowest,
        # I will order the lists of tuples according to the values of the first
        # entries. 
                
        expense_sorted=[]
        income_sorted=[]
        
        for sell_order in expense:
            expense_sorted.append([sell_order[4],sell_order[5]])
        
        for buy_order in income:
            income_sorted.append([buy_order[4],buy_order[5]])
            
        expense_sorted.sort(key = lambda y: y[0])
        income_sorted.sort(key = lambda y: y[0], reverse=True)
        
        # I am now ready to calculate the correct output based on the 
        # client's desired number of shares as each new order comes in. On a 
        # technical note, I'll need to take into account that an output should 
        # only be generated if a newly received order changes the previous 
        # output.
        
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

        
        
    
    
