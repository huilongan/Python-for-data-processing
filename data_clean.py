# -*- coding: utf-8 -*-
"""
Created on Mon Sep 12 14:00:42 2016
for data cleaning
@author: an
"""
import csv
import os

os.listdir()
with open("raw_processed.csv","r") as f:
    next(f,None)
    reader=csv.reader(f)
    data=list(reader)

with open("chappaqua_elevation_river_water surface.csv","r") as f:
    next(f,None)
    reader=csv.reader(f)
    data2=list(reader)
    
lon1=[]
lat1=[]
for line in data:
    lon1.append(line[1])
    lat1.append(line[2])

lon2=[]
lat2=[]
elev=[]
for line in data2:
    lon2.append(line[0])
    lat2.append(line[1])
    elev.append(line[2])
    
hash_table=dict()
for i,j,k in zip(lon2,lat2,elev):
    hash_table[(i,j)]=k

cor_elev=[]
for i,j in zip(lon1,lat1):
    try:
        cor_elev.append(hash_table[(i,j)])
    except KeyError:
        cor_elev.append('NA')
cor_elev

with open("hash_result.txt","w") as f:
    for i in cor_elev:
        f.write("%s\n"%i)
    f.close()