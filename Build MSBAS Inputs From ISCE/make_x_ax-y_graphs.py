#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 14:56:08 2021

@author: jasmine
"""
## create graphs 

# read in input list of MSBAS log files somehow 

# for each file open it and extract relavent line

# have a three column pandas dataframe with r value,  ||x|| and ||Ax-Y||

# in a loop append to list then combine to make dataframe

# plot as graph 
import argparse
import os, sys, glob 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
def getparser():
    # Parser to submit inputs for scripts. See Jul 27 Email from Jasmine
    parser = argparse.ArgumentParser(description="Extract ||x|| and ||Ax-y|| from MSBAS logs and make graph")
    parser.add_argument('input_file', type=str, help='input file with list of msbas logs to use')
   # parser.add_argument('--r_vals', action='store_true',help='If included makes array of header with r_vals between 0.05 - 50')
    #parser.add_argument('rm_flag', type=int, help='Flag to assign removal of large unecessary files, has to be 0 or 1. 0 files are kept, 1 files are deleted')
    return parser

# i think sticking with full paths on summit is safer as i have had issues with relative pathing and chdir
parser = getparser()
args = parser.parse_args()
inputs= args.input_file

orig_inputs = open(inputs)
input_list = orig_inputs.read()

with open(inputs) as f:
    input_list = [line.rstrip() for line in f]
    
# identify relavent line -  changes depending on how many files so find using reg instead of tailing file
r_value_list = []
x_list = []
ax_y_list = []

for infile in input_list:
    with open(infile) as inf:
        file = [lines.rstrip() for lines in inf]

    r_line = str([x for x in file if x.startswith('R_FLAG')][0])
    r_nums = r_line.split('=')[1]
    r_vals = r_nums.split(',')[1]
    r_value_list.append(r_vals)
    
        
    x_ax_y_line = str([y for y in file if y.startswith("computed ||x||" )][0])
    x = (x_ax_y_line.split())[5]
    ax_y = (x_ax_y_line.split())[6]
    ax_y_list.append(ax_y)
    x_list.append(x)
    
r_value_array = np.array(r_value_list)
x_array = np.array(x_list)
ax_y_array = np.array(ax_y_list)

# create a 3 column pandas data frame with r_val, ||x|| and ||Ax-y|| as columns
list_dict = {'r_val':r_value_array, 'x':x_array, 'ax-y':ax_y_array}
df = pd.DataFrame(list_dict)
df = df.astype(float)


# Get Unique continents
color_labels = df['r_val'].unique()

# List of colors in the color palettes
rgb_values = sns.color_palette("Set2", 4)

# Map continents to the colors
color_map = dict(zip(color_labels, rgb_values))





figure = plt.figure()
ax = plt.gca()
ax.plot(df['ax-y'] ,df['x'], linestyle='solid', c='blue' )
ax.plot(df['ax-y'] ,df['x'], 'o', c='y')

groups = df.groupby('r_val')
for name, group in groups:
    group.plot(ax=ax, kind='scatter',x=df['ax-y'], y=df['x'], y=df['r_val'], label=name marker="o", linestyle="", label=name)


ax.set_yscale('log')
ax.set_xscale('log')
df.plot.scatter(x="ax-y",y='x')