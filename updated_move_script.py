#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 11 15:26:01 2021

@author: jasmine
"""

### edits by JH of Joels Moving codes without changing directories and using full paths ####
# differences from joels: 
# - does not create a merged directory in the MSBAS directory 
# - copies all of the geotiffs not just the S1*cor file. 
# - we may want to change the checks for 'did isce run' to one of the *.geo files 

import os
import glob
import shutil
import argparse

def getparser():
    # Parser to submit inputs for scripts. See Jul 27 Email from Jasmine
    parser = argparse.ArgumentParser(description="Move ISCE outputs for MSBAS")
    parser.add_argument('current_dir', type=str, help='home directory holding date pair folders. i.e./net/tiampostorage2/volume2/JoelShare2/KristyProcessing/Colorado/Calwood/10m')
    parser.add_argument('rm_flag', type=int, help='Flag to assign removal of large unecessary files, has to be 0 or 1. 0 files are kept, 1 files are deleted')
    return parser

# i think sticking with full paths on summit is safer as i have had issues with relative pathing and chdir
parser = getparser()
args = parser.parse_args()
currentdir= args.current_dir
remove_flag = args.rm_flag
#os.chdir(currentdir)

#check that the inputted directory exits 
if os.path.isdir(currentdir) == True:
    print('Directory Valid - Continuing')
else:
    sys.exit('Input Directory Does Not Exist')

# check the remove flag is correct value
if remove_flag == 0:
        print('No File Removal')
elif remove_flag == 1:
        print('Large unecessary files will be removed')
else:
        #print('rm_flag must be either 0 or 1')
        sys.exit('Error - rm_flag must be either 0 or 1')



# list the directories with the pathnames
dates = glob.glob(os.path.join(currentdir,'20*'))

# get just the directory names
dir_names = []
for line in dates:
    val = os.path.basename(line)
    dir_names.append(val)

# list number of directories
datesize =len(dates)
print(str(datesize) + " folders found")

# create a directory for the msbas files to go into
savepath = os.path.join(currentdir, "MSBAS_FILES")

if os.path.isdir(savepath): 
	print("Transfer folder exists")
else: 
	os.mkdir(savepath) 
	print("making Transfer folder")
    
for i in dates:
   
    #check that isce ran in the directory
    isce_log_path = os.path.join(i, "isce.log")
    merge_dir_path = os.path.join(i, "merged/")
    filt_geo_path = os.path.join(merge_dir_path, "filt_topophase.unw.geo.vrt")
    
    # i have had some instances where you have the below files but it doesnt produce *.geo files
    if os.path.isfile(filt_geo_path) and os.path.isfile(isce_log_path):
        dir_only = os.path.basename(i)
        print('Working on {}'.format(dir_only))
        
        #make the directory to move the msbas files into 
    
        #os.mkdir(os.path.join(savepath,dir_only))
        msbas_directory = os.path.join(savepath,dir_only)
        if os.path.isdir(msbas_directory):
            print('MSBAS dir already exists')
        else: 
            os.mkdir(msbas_directory)
            print('Making MSBAS dir')
        
        print('Creating and copying original filelist')
        #save the files in the original directory for a list
        dir_files = [f for f in os.listdir(i) if os.path.isfile(os.path.join(i,f))]
        ls_filename = os.path.join(i,'{}_orig_files'.format(dir_only))
        with open (ls_filename, 'wt') as output:
            for item in dir_files:
                output.write("%s\n" % item)
        # move filelist to msbas directory 
        shutil.copy2(ls_filename,msbas_directory)
                
        
        #ls_command = 'ls {}/* > {}_orig_files'.format(i,os.path.join(i,dir_only)) 
        #os.system(ls_command)
        
        #move listfile to msbas directory CHECK THIS BIT
        lsinpath = os.path.join(i,'{}_orig_files'.format(dir_only))
        lsoutpath = msbas_directory
        shutil.copy2(lsinpath,lsoutpath)
        
        print('Copying isce.log file')
        # move the isce.log file
        shutil.copy2(isce_log_path,msbas_directory)
        
        print('Working on filt_topophase files')
        # make a list of all the /merged/filt_topohase files
        filt_topo_files = glob.glob(os.path.join(merge_dir_path,'filt_topophase.unw.geo*'))
        
        #if list is not empty copy the files over
        if len(filt_topo_files) != 0:
        
            for f in filt_topo_files:
                #copy the file from location to msbas_directory
                shutil.copy2(f,msbas_directory)
        else: print('filt_topophase.unw.geo files do not exist')
          
        print('Working on los files')
        # do the same for the los.rdr.geo files
        los_files = glob.glob(os.path.join(merge_dir_path,'los.rdr.geo*'))
        
        if len(los_files) != 0:
            for l in los_files:
                shutil.copy2(l, msbas_directory)
        else: print('los.rdr.geo files do not exist')
        
        print('Working on copying geotif files')
        #copy the geotiffs produced also 
        tif_files = glob.glob(os.path.join(i,'S1*.tif'))
        if len(tif_files) != 0:
            for t in tif_files:
                shutil.copy2(t,msbas_directory)
        else: print('S1*.tif files do not exist')    
         
        print('Creating directory for large files to be removed')
        # this section is to remove the large uncessary files
        # make a directory in each directory for files to be removed 
        remove_directory_name = os.path.join(i,'{}_remove'.format(dir_only))
        os.mkdir(remove_directory_name)
        
        print('Moving geom_master, fine_offsets, fine_coreg and .SAFE files to dir')
        #paths to directories and files to put in remove directory 
        geom = os.path.join(i, 'geom_master')
        shutil.move(geom,remove_directory_name)
        fine_offset = os.path.join(i, 'fine_offsets')
        shutil.move(fine_offset,remove_directory_name)
        fine_coreg = os.path.join(i, 'fine_coreg')
        shutil.move(fine_coreg,remove_directory_name)
        
        safe_files = glob.glob(os.path.join(i,'*.SAFE'))
        
        for s in safe_files:
            shutil.move(s,remove_directory_name)
            
        
        if remove_flag == 0:
            print('Large files moved to {} but not deleted'.format(remove_directory_name))
        elif remove_flag == 1:
            print('Removing Large Files')
            shutil.rmtree(remove_directory_name)
        else:
            print('remove_flag must be 1 or 0')
        # actually remove files - commented out for now
        #print('Removing large files')    
        #shutil.rmtree(remove_directory_name)
    else:
        print('ISCE did not run correctly')
            
        
        
        
            
            
            
            
    
    





