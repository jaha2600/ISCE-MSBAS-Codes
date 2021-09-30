#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 13 14:56:08 2021

@authors: jasmine hansen, ethan pierce & joel johnson, 2021
"""

## This code is used to find the optimum r_val to input into your MSBAS header file by looking at an array
## of previous MSBAS runs and finding the critical value
## To be used after running an array of MSBAS Files with differeing R Vals

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
import seaborn as sns

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

sns.set_theme(style = 'ticks')
# fig, ax = plt.subplots(figsize = (6, 6))

# ax.plot(points[0], points[1], color = 'k', alpha = 0.5)
# sns.scatterplot(data = df, x = 'ax-y', y = 'x', hue = 'r', ax = ax, palette = 'flare')
# ax.set_yscale('log')
# ax.set_xscale('log')
# plt.legend()
# plt.show()

# Take the derivative of our fitted polynomial
derivative = fit.deriv()

# Interpolate the derivative to points
dy_points = derivative.linspace(n)

# Find the index where the derivative is greatest
index = np.argmin(np.abs(np.abs(dy_points[1]).max() - np.abs(dy_points[1])))

# Translate the index into ax-y space
axy_crit = dy_points[0][index]

### produce intermediate plots - commented out for now ####
# print('Critical ax-y value is ' + str(np.round(axy_crit, 3)))

# plt.plot(dy_points[0], dy_points[1])
# # check with ethan that it is axy_crit?
# plt.scatter(axy_crit, dy_points[1][index], color = 'red', label = 'Critical value')

# #plt.scatter(critical_axy, dy_points[1][index], color = 'red', label = 'Critical value')
# plt.xlabel('ax-y')
# plt.ylabel('$\\frac{d}{d(ax-y)}$ fit')
# plt.legend()
# plt.show()

# Find the x, ax-y, and r-values where the derivative is steepest
r_index = np.argmin(np.abs(axy_crit - df['ax-y']))
r_crit = df['r'][r_index]
x_crit = df['x'][r_index]

# Plot everything together
sns.set_theme(style = 'ticks')
fig, ax = plt.subplots(figsize = (6, 6))

ax.plot(points[0], points[1], color = 'k', alpha = 0.5)
sns.scatterplot(data = df, x = 'ax-y', y = 'x', hue = 'r', ax = ax, palette = 'flare')

ax.plot(axy_crit, x_crit, marker = 'o', fillstyle = 'none', color = 'red', markersize = 10, label = 'critical value')

ax.set_yscale('log')
ax.set_xscale('log')
plt.legend()
#plt.show()
#save figure
fig_outname = os.path.join(outpath, 'crit_rval_x_ax-y_graph.png') 
plt.savefig(fig_outname, dpi=300)

axy_crit_round = np.round(axy_crit, 3)
x_crit_round = np.round(x_crit, 3)
r_crit_round = np.round(r_crit, 3)

#print('Critical ax-y-value is ' + str(np.round(axy_crit, 3)))
#print('Critical x-value is ' + str(np.round(x_crit, 3)))
#print('Critical r-value is ' + str(np.round(r_crit, 3)))

crit_outdata = 'Crit r_val: ' + str(r_crit_round) + '\n' + 'Crit x-val: ' + str(x_crit_round) + '\n' + 'Crit ax-y val: ' + str(axy_crit_round) 
crit_outpath = os.path.join(outpath, 'critical_r_values.txt')

print('Saving out data')
# save textfile 
text_file = open(crit_outpath, "w")
n = text_file.write(crit_outdata)
text_file.close()





















