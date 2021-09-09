#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  2 13:21:20 2021

@author: jasmine
"""
import os,sys,glob
import rasterio 
import numpy as np 

dirs = '/data/GREENLAND/INSAR/MSBAS/asc/'
files = glob.glob((os.path.join(dirs,'*clip_2.tif')))
files.sort()
names = []
for n in files:
    val = os.path.basename(n)
    names.append(val)
    
saveList = []
saveList.append('Filename Mean Median Percent_Coverage')

for f in files:
    print(f)
    with rasterio.open(f) as src:
        vals = src.read(1,masked=True)
        
    #get mask distribution
    mask = vals.mask
    # total number of values in array 
    count = (len(mask)) * (len(mask[0]))
    # number of bad values
    true_values = np.count_nonzero(mask)
    # number of values of valid data points 
    positive_values = count - true_values
    
    # coverage in i.e. how many good values are there compared to overall grid size
    coverage_value = positive_values/count
    # get percentage of non zero values i.e. coverage. 
    coverage_percent = coverage_value * 100
    
    mean = vals.mean()
    median = np.ma.median(vals)
    
    # round values
    format_mean = float('{:0.3e}'.format(mean))
    format_median = float('{:0.3e}'.format(median))
    format_percent = float('{:0.3e}'.format(coverage_percent))

    
    combine_string = str(f) + " " + str(format_mean) + " " + str(format_median) + " " + str(format_percent)
    saveList.append(combine_string)
    

out_filename = os.path.join(dir,'filt_topo_clip_2_statistics.txt')
np.savetxt(out_filename, saveList, fmt='%s', delimiter=' ', newline = '\n')
