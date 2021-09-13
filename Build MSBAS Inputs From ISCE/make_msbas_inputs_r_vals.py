#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 15:51:32 2021

@author: jasmine
"""

import os, sys
import glob
import re
import numpy as np
from datetime import datetime


##################### JH ADD THESE MODULES AUG 2021 ###############################
from osgeo import gdal, ogr
import argparse
import pandas as pd
################################################################################################
# Step 0: run ISCE up to 'computeBaselines' step. Container does this.
# Step 1: Edit dir_in below to point to directory of interferogram directories. Run this script.
################################################################################################

def getparser():
    # Parser to submit inputs for scripts. See Jul 27 Email from Jasmine
    parser = argparse.ArgumentParser(description="Create inputs for MSBAS")
    parser.add_argument('input_file', type=str, help='link to the input file with variables in')
    parser.add_argument('--r_vals', action='store_true',help='If included makes array of header with r_vals between 0.05 - 50')
    #parser.add_argument('rm_flag', type=int, help='Flag to assign removal of large unecessary files, has to be 0 or 1. 0 files are kept, 1 files are deleted')
    return parser

# i think sticking with full paths on summit is safer as i have had issues with relative pathing and chdir
parser = getparser()
args = parser.parse_args()
inputs= args.input_file
#extentfile=args.shapefile_area
#os.chdir(currentdir)



#read in variables from input text file 

df=pd.read_csv(inputs,names=['var_names','var_vals'], sep='=')
var_vals = df['var_vals']

dir_in=str(var_vals[0])
extent_val = str(var_vals[1])

# check directory is valid 
if os.path.isdir(dir_in):
    print('Working Dir exists - continuing')
else:
    sys.exit('Input Directory Does Not Exist')
    
# check if extents input is a shapefile or just a string 
if extent_val.endswith(".shp"):
    inDriver = ogr.GetDriverByName("ESRI Shapefile")
    inDataSource = inDriver.Open(extent_val, 0)
    inLayer = inDataSource.GetLayer()
    extents = inLayer.GetExtent()
    extent = str(extents[0]) + ', ' + str(extents[3]) + ', ' + str(extents[1]) + ', ' + str(extents[2]) 
else:
    extent = extent_val
    
    
#confirm folder exists to save to. 
trackdir = os.path.join(dir_in, "asc")
if not os.path.isdir(trackdir):
	os.makedirs(trackdir)
	print("created folder ", trackdir)
else:
	print(trackdir, " folder exists")



os.chdir(dir_in)
dates = glob.glob('20*')
dates.sort()
size =len(dates)
print(size, "folders found")

saveList = []



for i in range(size):
    print(' ## Working on {}/{} ##'.format((i+1),size))
    merged_dir = os.path.join(dir_in,dates[i],'merged/')
    phaseFileIn = os.path.join(merged_dir, 'filt_topophase.unw_m.geo')
    
    convertdir = os.path.join(dir_in,dates[i])
    
    if os.path.isdir(convertdir):
        #    if os.path.isdir(convertdir):
        os.chdir(merged_dir)
       
        #Command from scotty cheat sheet with -1 added to make negative values match surface moving AWAY from the satellite. Call the .vrt extension for use with gdal
        print('Clipping filt_topophase')
        convert2m_command= 'gdal_calc.py -A filt_topophase.unw.geo.vrt --A_band=2 --calc="A*-1*0.05546576/12.5663706" --quiet --outfile=filt_topophase.unw_m.geo  --format=ENVI --NoDataValue=-9999 --overwrite'
       
        os.system(convert2m_command)
       
        phaseFileOut = os.path.join(dir_in,trackdir,dates[i] + ".filt_topophase.unw_m.geo.clip.tif")
       
       
        # clip filt file. 
       
        phase_gdal_command = 'gdal_translate -projwin '+str(extent)+' -of GTiff '+str(phaseFileIn)+' '+str(phaseFileOut)
       
       
        os.system(phase_gdal_command)
       
        # adapted from magalis script 
        print('Creating data for input textfile')
        full = dates[i]
        first = full[0:8]
        second = full[9:17]
        logfile_path = os.path.join(dir_in, dates[i], 'isce.log')
        logfile = open(logfile_path)
       
        data = logfile.read()
       
        match_IW1_first = re.search('baseline.IW-1 Bperp at midrange for first common burst = (-?\d*\.?\d*)',data)
        match_IW2_first = re.search('baseline.IW-2 Bperp at midrange for first common burst = (-?\d*\.?\d*)',data)
        match_IW3_first = re.search('baseline.IW-3 Bperp at midrange for first common burst = (-?\d*\.?\d*)',data)
       
        bperps = []
        if match_IW1_first:
            bperps.append(match_IW1_first.group(1))
        if match_IW2_first:
            bperps.append(match_IW2_first.group(1))
        if match_IW3_first:
            bperps.append(match_IW3_first.group(1))
           
        bperps = np.array(bperps,dtype='float')
        bperp_ave = round(np.average(bperps),5)
       
        trackFileOut = os.path.join(trackdir, dates[i] +".filt_topophase.unw_m.geo.clip.tif") #Gives location column for trackFile
        print(trackFileOut, bperp_ave,first,second)
        combine = str(trackFileOut) + " " + str(bperp_ave) + " " + str(first) + " " + str(second)
        saveList.append(combine) #Saves all the info we want for our track txt
        
    
        
    else:
        print(convertdir + ' does not exist')


print(saveList)

savepath = os.path.join(dir_in,'saveList.txt') #Same as the asc.txt

np.savetxt(savepath, saveList, fmt="%s", delimiter=' ', newline='\n')



################################## JH ADD AUG 11 2021 - code to create a header file and clip/extract values from LOS file #####################################

# clip an los file from an example subdirectory to extract azumith and incidence angle
# we have one los file which is in the main msbas directory msbas/los* in same as 20XX_20XX dirs.

print('Clipping an los.rdr.geo.vrt file')
los_file_in = os.path.join(dir_in,'los.rdr.geo.vrt')
los_file_out = os.path.join(dir_in,'los.rdr.geo.tif.clip')
clip_los_command = 'gdal_translate -projwin '+str(extent)+' -of GTiff -q '+str(los_file_in)+' '+str(los_file_out)

os.system(clip_los_command)

print('Conveting an example filt_topo.clip file to view pixel coordinates')
examp_filt = os.path.join(dir_in,trackdir,dates[0] + ".filt_topophase.unw_m.geo.clip.tif")
examp_filt_out = os.path.join(dir_in,dates[0] + ".filt_topophase.unw_m.geo.clip.pixel.tif")
pixel_command = 'gdal_translate -ot Byte -scale '+str(examp_filt)+' '+str(examp_filt_out)
os.system(pixel_command)

# read gdal info in python instead of commandline 
print('Extracting incidence and azumith')
los_info = gdal.Info(los_file_out, format='json', stats='True')
los_band_info = los_info['bands']
# extract mean of band 1
los_band_1_mean = los_band_info[0]['mean']
incidence_angle = los_band_1_mean
# extract mean of band 2
los_band_2_mean = los_band_info[1]['mean']
azimuth = (los_band_2_mean * (-1)) + 90


examp_file = dates[0]
first_e = examp_file[0:8]
second_e = examp_file[9:17]

#line changed post sending to joel...
# i have a file that lists the original files from the ISCE run that i use to read the safefile headers
orig_filelist_name = first_e + '_' + second_e + '_orig_filelist'
orig_filelist_path = os.path.join(dir_in,dates[0],orig_filelist_name)
orig_filelist = open(orig_filelist_path)
orig_filelist_data = orig_filelist.read()

safe_files = []
print('Getting Start Time')
# extract safe file lines from the input textfile
for item in orig_filelist_data.split("\n"):
    if "SAFE" in item:
        sf = (item.strip())
        safe_files.append(sf)

# extract times
start_time = (safe_files[0])[26:32]
end_time = (safe_files[0])[42:48]


#get file size from clipped filt_file 
print('Getting Image Size')
phaseFileOut_e = os.path.join(dir_in,trackdir,dates[0] + ".filt_topophase.unw_m.geo.clip.tif")
phase_file_info = gdal.Info(phaseFileOut_e, format='json')
file_size = phase_file_info['size']
# create textfile 
# # this file has blank placeholders for variables like format, file size etc. values can be added to this script later if needed
# header_combined = 'FORMAT=2, 0' + '\n' +'FILE_SIZE=' + str(file_size[0]) + ', ' + str(file_size[1]) + '\n' + 'C_FLAG=' + '\n' + 'R_FLAG=' + '\n' + 'I_FLAG=' + '\n' + 'SET=' + str(start_time) +', ' + str(azimuth) + ', ' + str(incidence_angle) + ', saveList.txt'
# header_savepath = os.path.join(dir_in, 'header.txt')

# print('Creating header.txt file')
# # save textfile 
# text_file = open(header_savepath, "w")
# n = text_file.write(header_combined)
# text_file.close()



### ADDED BY JH SEP 13th - NEED TO CHECK ###
# if there is an array flag create multiple header files with different r values.
if args.r_vals:
    r_values = [0.5,1,5,10,20,50]
    print('Creating array of header text files with different r values')
    for r in r_values:
        #print(r)
        header_combined = 'FORMAT=2, 0' + '\n' +'FILE_SIZE=' + str(file_size[0]) + ', ' + str(file_size[1]) + '\n' + 'C_FLAG=' + '\n' + 'R_FLAG=' + str(r) + '\n' + 'I_FLAG=' + '\n' + 'SET=' + str(start_time) +', ' + str(azimuth) + ', ' + str(incidence_angle) + ', saveList.txt'
        header_name = 'header_{}.txt'.format(r)
        header_savepath = os.path.join(dir_in, header_name)
        text_file = open(header_savepath, "w")
        n = text_file.write(header_combined)
        text_file.close()


else:
    print('Creating header.txt file - user must manually add r_val')
    # this file has blank placeholders for variables like format, file size etc. values can be added to this script later if needed
    header_combined = 'FORMAT=2, 0' + '\n' +'FILE_SIZE=' + str(file_size[0]) + ', ' + str(file_size[1]) + '\n' + 'C_FLAG=' + '\n' + 'R_FLAG=' + '\n' + 'I_FLAG=' + '\n' + 'SET=' + str(start_time) +', ' + str(azimuth) + ', ' + str(incidence_angle) + ', saveList.txt'
    header_savepath = os.path.join(dir_in, 'header.txt')

    print('Creating header.txt file')
    # save textfile 
    text_file = open(header_savepath, "w")
    n = text_file.write(header_combined)
    text_file.close()
################
print('#### Script Complete ####')
