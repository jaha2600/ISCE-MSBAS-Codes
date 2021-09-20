#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 14:56:08 2021

@author: jasmine
"""

# impor relavent modules
import argparse
import os, sys, glob 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

# input file is a texfile with the path and names of all of the header files you want to run through
# i.e. /path/to/header/header.txt
#      /path/to/header/header_2.txt

def getparser():
    parser = argparse.ArgumentParser(description="Extract ||x|| and ||Ax-y|| from MSBAS logs and make graph")
    parser.add_argument('input_file', type=str, help='input file with list of msbas logs to use')
    parser.add_argument('csv_out_loc', type=str, help='path and name of output csv file')
    return parser

parser = getparser()
args = parser.parse_args()
inputs= args.input_file
csv_outpath = args.csv_out_loc

# open input textfile and read 
orig_inputs = open(inputs)
input_list = orig_inputs.read()

# extract to a list where each line is seperate value
with open(inputs) as f:
    input_list = [line.rstrip() for line in f]
    
# initialize arrays to save values
r_value_list = []
x_list = []
ax_y_list = []


for infile in input_list:
    # open header file
    with open(infile) as inf:
        # extract each line of file into list
        file = [lines.rstrip() for lines in inf]
    
    #find line with r value on and extract value - append to r value list
    r_line = str([x for x in file if x.startswith('R_FLAG')][0])
    r_nums = r_line.split('=')[1]
    r_vals = r_nums.split(',')[1]
    r_value_list.append(r_vals)
    
    # same as above find line with ||x|| etc. values on and extract - appending to lists
    x_ax_y_line = str([y for y in file if y.startswith("computed ||x||" )][0])
    x = (x_ax_y_line.split())[5]
    ax_y = (x_ax_y_line.split())[6]
    ax_y_list.append(ax_y)
    x_list.append(x)

# convert lists to arrays
r_value_array = np.array(r_value_list)
x_array = np.array(x_list)
ax_y_array = np.array(ax_y_list)

# create a 3 column pandas data frame with r_val, ||x|| and ||Ax-y|| as columns
list_dict = {'r_val':r_value_array, 'x':x_array, 'ax-y':ax_y_array}
df = pd.DataFrame(list_dict)
df = df.astype(float)

#save dataframe as csv file 
df.to_csv(csv_outpath, index=False)

# plot a graph of ||x|| vs || || in log
# need to plot points, plot a function to make a line that joins all of them 
# color each individual point by r_number
# do trigonometry to find where the apex of the curve is, and spit out the r value that it sits inbetween

# figure = plt.figure()
# ax = plt.gca()
#ax.plot(df['ax-y'] ,df['x'], linestyle='solid', c='blue' )
#ax.plot(df['ax-y'] ,df['x'], 'o', c='y')
#ax.set_yscale('log')
#ax.set_xscale('log')

