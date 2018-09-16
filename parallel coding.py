#%%
import urllib
from bs4 import BeautifulSoup
from cStringIO import StringIO
import unicodecsv
import csv
import time
import sys
import itertools as itt
import os
start_time = time.time()

#how to chunck your data to run it on parallel computers


#input_path  = raw_input('insert the input path')
#output_path = raw_input('insert the output path')
sys_argv=sys.argv;
input_path=sys_argv[1]
output_path=sys_argv[2]

SLURM_ARRAY_TASK_ID=os.environ['SLURM_ARRAY_TASK_ID']
print(SLURM_ARRAY_TASK_ID)
SLURM_ARRAY_TASK_COUNT=os.environ['SLURM_ARRAY_TASK_MAX']
print(SLURM_ARRAY_TASK_COUNT)
output_path=sys_argv[2]+SLURM_ARRAY_TASK_ID+'.csv'
print(SLURM_ARRAY_TASK_ID,SLURM_ARRAY_TASK_COUNT)



# Write the names into a list called names
names = []
with open ('names.csv') as names_path:
    names_path_csv = csv.reader(names_path)
    for row in names_path_csv:
        names += row
#%%   
inputFile = open(input_path,'rb')
paths = csv.reader(inputFile)
pathstr=[]
for row in paths:
        pathstr += row
chunk=len(pathstr)/int(SLURM_ARRAY_TASK_COUNT)
pathslice=list(itt.islice(pathstr, int(SLURM_ARRAY_TASK_ID)*chunk,(int(SLURM_ARRAY_TASK_ID)+1)*chunk))
print(len(pathstr))
print(int(SLURM_ARRAY_TASK_ID)*chunk,(int(SLURM_ARRAY_TASK_ID)+1)*chunk)
for path in pathslice:
    page = path
    soup = BeautifulSoup(urllib.urlopen(page),'lxml')
    page_text = soup.get_text()
    # All in upper case
    page_text = page_text.upper()


           
print("--- %s seconds ---" % (time.time() - start_time))
