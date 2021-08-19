#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 23 13:31:08 2021

@author: jasmine
"""
# code to extract possible pairs from a textfile of sentinal images
###### Jasmine Hansen 2021 #########
import os, sys
from itertools import combinations
import argparse
import pandas as pd

def getparser():
    parser = argparse.ArgumentParser(description='Create every possibe iterations of object')
    #make sure you hardcode the path or use $PWD/ in the commandline infront of file
    parser.add_argument('files', type = str, help = 'list of files to be ran through')
    parser.add_argument('seperation', type = int, help = 'max day difference between pairs')
    
    return parser

parser = getparser()
args = parser.parse_args()

filelist = args.files 
day_diff = args.seperation

#filelist = '/data/GREENLAND/DATASETS/InSAR/watson_id_list_feb_21.txt'
# open textfile and read into a list
with open(filelist) as f3:
      file_list = f3.read().splitlines()

# work out every possible combination in the textfile into list of tuples
combos = list(combinations(file_list,2))   
# convert to pandas dataframe where the two file ids are columns in the same row
df = pd.DataFrame(combos)
# extract the first date from each file 
df['date_1'] = [x[17:25] for x in df[0]]
df['date_2'] = [x[17:25] for x in df[1]]

#convert to datetime object to get days inbetween
df['date_1'] = pd.to_datetime(df['date_1'])
df['date_2'] = pd.to_datetime(df['date_2'])
# calculate the number of days between the two values
df['day_difference'] = (abs(df['date_1'] - df['date_2']).dt.days)

# extract those values that are equal than or less too than the threshold specified in input
good_difference = df[df['day_difference']  <= int(day_diff)]
good_difference = good_difference.copy()
# set column titles
good_difference.columns = ['id_1', 'id_2', 'date_1', 'date_2', 'day_difference']

# set condition if first date is older than second 
cond = good_difference['date_1'] > good_difference['date_2']
# if that condition is met w
good_difference.loc[cond, ['id_1', 'id_2']] = good_difference.loc[cond, ['id_2', 'id_1']].values

#check the date order is correcvt (in this example we have the more recent date first)
#df.a, df.b = np.where(df.a > df.b, [df.b, df.a], [df.a, df.b])
#good_difference
# extract the first two columns only (filenames)
good_difference = good_difference.iloc[:, 0:2]

# turn back into list of tuples
combo_2 = list(map(tuple, good_difference.to_numpy()))

# define output filenane

out_textfile = os.path.split(filelist)[0] + '/possible_combinations.txt'
out_file_isce = os.path.split(filelist)[0] + '/isce_input_list.txt'
#open textfile in write mode 
file_object = open(out_textfile, 'w')

# for each entry save the values as a line with a space between files and two spaces between rows.
for i in combo_2:
    values = ' '.join(i)
    file_object.write(values +'\n')
file_object.close()


# os sys command to convert spaces to new lines 
convert_cmd = 'sed -i \'s/ /\\n/g\''
total = convert_cmd + ' {}'.format(out_textfile)
os.system(total)
# os sys command to remove -SLC from the ending 
remove_cmd = 'sed -i \'s/\-SLC//g\''
change = remove_cmd + ' {}'.format(out_textfile)
os.system(change)

