#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 14:56:08 2021

@authors: jasmine hansen, ethan pierce & joel johnson, 2021
"""

## simplified graph code that plots x and ax-y and labels by r-val to ref which msbas runs are good

## inputs are a textfile containing the path and name of all of your log files
## i.e./path/to/header/header.txt
##      /path/to/header/header_2.txt
## and the out directory you wish to save your files in 

# outputs : graph of |x| vs |ax-y|, critical (best) r val and csv of all r |x| and |ax-y| values

# import relavent modules
import argparse
import os, sys 
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
#import seaborn as sns

# parser for command line inputs 
def getparser():
    parser = argparse.ArgumentParser(description="Extract ||x|| and ||Ax-y|| from MSBAS logs and make graph")
    parser.add_argument('input_file', type=str, help='input file with list of msbas logs to use')
    parser.add_argument('out_dir', type=str, help='path to where you want outfiles')
    return parser

parser = getparser()
args = parser.parse_args()
inputs= args.input_file
outpath = args.out_dir

#test
#inputs = '/data/GREENLAND/INSAR/MSBAS/test_log_data/log_list.txt'
#outpath = '/data/GREENLAND/INSAR/MSBAS/test_log_data/'

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

# convert lists with values in to arrays
r_value_array = np.array(r_value_list)
x_array = np.array(x_list)
ax_y_array = np.array(ax_y_list)

# create a 3 column pandas data frame with r_val, ||x|| and ||Ax-y|| as columns
list_dict = {'r':r_value_array, 'x':x_array, 'ax-y':ax_y_array}
df = pd.DataFrame(list_dict)
df = df.astype(float)

#save dataframe as csv file
csv_outpath = os.path.join(outpath, 'msbas_log_r_data.csv')
df.to_csv(csv_outpath, index=False)

### code written by Ethan Pierce September 2021 ###

# Compute a least-squares fit to data
fit = np.polynomial.Polynomial.fit(df['ax-y'], df['x'], 2, domain = [df['ax-y'].min(), df['ax-y'].max()])

# Interpolate the fit to some points in our domain
n = 100
points = fit.linspace(n)


# Plot everything together
#sns.set_theme(style = 'ticks')
fig, ax = plt.subplots(figsize = (11, 8.5))

ax.plot(points[0], points[1], color = 'k', alpha = 0.5)
#sns.scatterplot(data = df, x = 'ax-y', y = 'x', hue = 'r', ax = ax, palette = 'flare')
#ax.scatter(df['ax-y'], df['x'])

#ax.plot(axy_crit, x_crit, marker = 'o', fillstyle = 'none', color = 'red', markersize = 10, label = 'critical value')

# new code to add markers to points 
for i,rval_text in enumerate(df['r']):
    print(i)
    print(rval_text)
    x = df['ax-y'][i]
    y = df['x'][i]
    ax.scatter(x, y, marker='.', color='red')
    ax.text(x, y, rval_text, fontsize=9)
#plt.show()


ax.set_yscale('log')
ax.set_xscale('log')
ax.set_xlabel('log(ax-y)')
ax.set_ylabel('log(x)')
plt.legend()
plt.show()
#save figure
fig_outname = os.path.join(outpath, 'crit_rval_x_ax-y_graph.png') 
plt.savefig(fig_outname, dpi=300)




















