#!/usr/bin/env python3

import os
import glob
import re
import numpy as np
from datetime import datetime


##################### JH ADD THIS MODULE AUG 11 2021 ###############################
from osgeo import gdal
import argparse
################################################################################################
# Step 0: run ISCE up to 'computeBaselines' step. Container does this.
# Step 1: Edit dir_in below to point to directory of interferogram directories. Run this script.
################################################################################################

def getparser():
    # Parser to submit inputs for scripts. See Jul 27 Email from Jasmine
    parser = argparse.ArgumentParser(description="Create inputs for MSBAS")
    parser.add_argument('current_dir', type=str, help='dir with 20* directories in (can just used $PWD if in correct place')
    #parser.add_argument('rm_flag', type=int, help='Flag to assign removal of large unecessary files, has to be 0 or 1. 0 files are kept, 1 files are deleted')
    return parser

# i think sticking with full paths on summit is safer as i have had issues with relative pathing and chdir
parser = getparser()
args = parser.parse_args()
currentdir= args.current_dir
#os.chdir(currentdir)

dir_in = currentdir


#confirm folder exists to save to. 
trackdir = os.path.join(dir_in, "asc")
if not os.path.isdir(trackdir):
	os.makedirs(trackdir)
	print("created folder ", trackdir)
else:
	print(trackdir, " folder exists")



os.chdir(dir_in)
dates = glob.glob('20*')
size =len(dates)
print(size, "folders found")

saveList = []




for i in range(size):
    phaseFileIn = os.path.join(dir_in,dates[i], 'filt_topophase.unw_m.geo')
    
    convertdir = os.path.join(dir_in,dates[i])
    
    if os.path.isdir(convertdir):
        #    if os.path.isdir(convertdir):
        os.chdir(convertdir)
       
        #Command from scotty cheat sheet with -1 added to make negative values match surface moving AWAY from the satellite. Call the .vrt extension for use with gdal
       
        convert2m_command= 'gdal_calc.py -A filt_topophase.unw.geo.vrt --A_band=2 --calc="A*-1*0.05546576/12.5663706" --outfile=filt_topophase.unw_m.geo  --format=ENVI --NoDataValue=-9999 --overwrite'
       
        os.system(convert2m_command)
       
        phaseFileOut = os.path.join(dir_in,trackdir,dates[i] + ".filt_topophase.unw_m.geo.clip.tif")
       
       
        # get the extents from qgis and the -COR or -AMP or -UNW geotiffs and paste below.
       
        phase_gdal_command = 'gdal_translate -projwin -55.54984305896815 68.0001446011998 -48.14986218680518 65.16982519688996 -of GTiff '+str(phaseFileIn)+' '+str(phaseFileOut)
       
       
        os.system(phase_gdal_command)
       
        # adapted from magalis script 
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
los_file_in = os.path.join(dir_in,dates[0],'los.rdr.geo.vrt')
los_file_out = os.path.join(dir_in,trackdir,dates[0] + '.los.rdr.geo.tif.clip')
clip_los_command = 'gdal_translate -projwin -55.54984305896815 68.0001446011998 -48.14986218680518 65.16982519688996 -of GTiff '+str(los_file_in)+' '+str(los_file_out)

os.system(clip_los_command)

# read gdal info in python instead of commandline 
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

# extract safe file lines from the input textfile
for item in orig_filelist_data.split("\n"):
    if "SAFE" in item:
        sf = (item.strip())
        safe_files.append(sf)

# extract times
start_time = (safe_files[0])[26:32]
end_time = (safe_files[0])[42:48]


#get file size from clipped filt_file 

phaseFileOut_e = os.path.join(dir_in,trackdir,dates[0] + ".filt_topophase.unw_m.geo.clip.tif")
phase_file_info = gdal.Info(phaseFileOut_e, format='json')
file_size = phase_file_info['size']
# create textfile 
# this file has blank placeholders for variables like format, file size etc. values can be added to this script later if needed
header_combined = 'FORMAT=2, 0' + '\n' +'FILE_SIZE=' + str(file_size[0]) + ', ' + str(file_size[1]) + '\n' + 'WINDOW_SIZE' + '\n' + 'C_FLAG=' + '\n' + 'R_FLAG=' + '\n' + 'I_FLAG=' + '\n' + 'SET=' + str(start_time) +', ' + str(azimuth) + ', ' + str(incidence_angle) + ', saveList.txt'
header_savepath = os.path.join(dir_in, 'header.txt')

# save textfile 
text_file = open(header_savepath, "w")
n = text_file.write(header_combined)
text_file.close()


# combine = string[i] + "\t" + base[i] + "\t" + ref[i] + "\t" + sec[i]
# 	content.append(combine)
# np.savetxt('asc.txt', (content), fmt="%s", delimiter='\t', newline='\n')

#print("track list: ", trackList)
#print("bperp list: ", bperpList)


