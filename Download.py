# -*- coding: utf-8 -*-
"""
Created on Thu Sep 22 10:57:48 2016

@author: Andy
"""
import shutil
import zipfile
import tarfile
import urllib.request as ur
import os
import bs4
import re


base='http://www.srh.noaa.gov/ridge2/Precip/qpehourlyshape/'

def download_data(base,to):
    if not os.path.exists(to):
        raise ValueError("no such a folder!")
    html=ur.urlopen(base)
    bsobj=bs4.BeautifulSoup(html)
    downthing=bsobj.findAll('a',href=re.compile("nws_precip_[0-9]+\.tar\.gz"))
    if len(downthing) > 0:
        for i in downthing:
            name=i.get_text()
            link=base+i['href']
            try:
                ur.urlretrieve(link,to+'/'+name)
                print(name+" done!")
                files=tarfile.open(to+'/'+name)
                files.extractall()
                for i in files.getnames():
                    os.rename(i,i.replace(os.path.dirname(i),to))
                shutil.rmtree(files.getnames()[0].split("/")[0])
                os.remove(to+'/'+name)
                print(name+" unzip done!")
            except:
                pass
                
    folders=bsobj.findAll('a',href=re.compile("^([0-9]+)/"))
    if len(folders) > 0:
        for fold in folders:
            new=fold['href']
            download_data(base+new,to)

def download_data_zip(base,to):
    if not os.path.exists(to):
        raise ValueError("no such a folder!")
    html=ur.urlopen(base)
    bsobj=bs4.BeautifulSoup(html)
    downthing=bsobj.findAll('a',href=re.compile("nws_precip_[0-9]+\.tar\.gz"))
    if len(downthing) > 0:
        for i in downthing:
            name=i.get_text()
            link=base+i['href']
            try:
                ur.urlretrieve(link,to+'/'+name)
                print(name+" done!")
            except:
                pass
                
    folders=bsobj.findAll('a',href=re.compile("^([0-9]+)/"))
    if len(folders) > 0:
        for fold in folders:
            new=fold['href']
            download_data_zip(base+new,to)

if __name__=='__main__':
    print('{}'.format('********************************'))
    print('{}'.format('Hourly rain data downloading'))
    print('{}'.format('Year 2005 - 2016'))
    print('{}'.format('********************************'))
    add_base=input("write down the year you want (2011-2016),eg.2011,2012,2013. or 2011/201103/20110320 for specific day, or 2011/201103 for specific month.\n")
    towhere=input("where you want to store?e.g \"/users/andy/desktop/internship/prec\"\n")
    y_n=input("zip for zipfile, shp for unzipfile!")
    for i in add_base.split(','):
        if y_n == 'shp':
            download_data(base+i+'/',towhere)
        elif y_n=='zip':
            download_data_zip(base+i+'/',towhere)
        else:
            print("Byebye!")
    
