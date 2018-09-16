
# coding: utf-8

# In[2]:


import requests
import pandas as pd
import re
import os
import csv
import sys
import itertools as itt
import fnmatch


# In[3]:


mother = []
mothership = []

def parser(r):
    #advisor information
    companies = []
    advisory = []

    #family information
    fam = []
    family = []
    number = []

    #series in the regisreant
    multi=[]
    counter = []

    # read line by line, save the items that you want
    for line in r.iter_lines():
        if line:
                #if it is a unit investment trust, skip
                if line[0:3] == '003':
                    if str.strip(line[11:]) != 'N':
                        continue
                else:
                    #family
                    if line[0:3] == '019':
                        if line [4:5] == 'A':
                            fam.append(str.strip(line[11:]))
                        if line [4:5] == 'B':
                            number.append(str.strip(line[11:]))
                        if line [4:5] == 'C':
                            family.append(str.strip(line[11:]))
                    #number of portfolios:
                    if line[0:3] == '007':
                        if line [4:5] == 'A':
                            multi.append(str.strip(line[11:]))
                        if line [4:5] == 'B':
                            counter.append(str.strip(line[11:]))
                    #advisor/subadvisor
                    if line[0:3] == '008':
                            # collect the advisor name
                            if line[4:5] == 'A':
                                companies.append(str.strip(line[11:]))
                            # collect the situation: A"advisor", B"Subadvisor"
                            if line[4:5] == 'B':
                                advisory.append(str.strip(line[11:]))

                    series_sit = list(set(zip(multi, counter)))
                    advise_sit = list(set(zip(advisory,companies)))
                    family_sit = list(set(zip(fam,family,number)))
                    mother = {'name':url,'adv':advise_sit, 'fam':family_sit, 'series':series_sit}
    return mother


# In[9]:


def dfmaker(dictionary):
    fund = []
    multi = []
    portfo = []

    member = []
    family = []
    siblings = []

    sub = []
    advisor = []

    for fc in dictionary:
            fund.append(fc['name'])

            if len(fc['series']) > 0:
                multi.append(fc['series'][0][0])
                portfo.append(fc['series'][0][1])
            else:
                multi.append('X')
                portfo.append('0')

            if len(fc['adv']) == 0:
                sub.append('X')
                advisor.append('X')
            elif len(fc['adv']) == 1:
                sub.append(fc['adv'][0][0])
                advisor.append(fc['adv'][0][1])
            elif len(fc['adv']) > 1:
                l = []
                m = []
                for each_advisor in range(0,len(mothership[8]['adv'])):
                    l.append(mothership[8]['adv'][each_advisor][1])
                    m.append(mothership[8]['adv'][each_advisor][0])
                advisors = (',').join(l)
                subs = (',').join(m)
                advisor.append(advisors)
                sub.append(subs)

            if fc['fam'] != []:
                member.append(fc['fam'][0][0])
                family.append(fc['fam'][0][1])
                siblings.append(fc['fam'][0][2])
            else:
                member.append('N')
                family.append('X')
                siblings.append('0')
    df = pd.DataFrame({'name':fund, 'multi' : multi, 'portfo' : portfo, 'member' : member, 'family' : family, 'siblings' : siblings,
                  'sub': sub, 'advisor': advisor})
    df.to_csv('output_{0}'.format('x'))
    return df
    print 'done!!!'


# In[5]:


get_ipython().run_cell_magic('timeit', '', "url = 'https://www.sec.gov/Archives/edgar/data/1002427/0001167420-05-000006.txt'\nr = requests.get(url)\na = parser(r)\na")

%%timeit
import time
file_list = os.getcwd()

for filename in os.listdir(file_list):
    mothership = []
    mother = []
    if fnmatch.fnmatch(filename, 'input_*.csv'):
        path_to_file = os.path.join('/home/users/mhaghbaali1/Thesis/new_data', filename)
        inputFile = open(path_to_file,'rb')
        paths = csv.reader(inputFile)
        for i,path in enumerate(paths):
            if i == 0:
                continue
            else:
                print filename
                url = path[0]
                print url
                r = requests.get(url)
                # this is for every url; everytime mothership is updated
                mother = parser(url)
                mothership.append(mother)
        #at the end of the file, a csv file is made for that year
        df = dfmaker(filename,mothership)
        #and now we move to the next file, next year!

# In[11]:


dfmaker(a)

