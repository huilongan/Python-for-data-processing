# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 12:31:11 2016

@author: Andy
"""

import email
import os
import re
import csv
os.chdir('/users/andy/desktop/Inbox')
os.listdir()

f = open('44824000000033011.eml','r')
email_text = email.parser.Parser()
t = email_text.parse(f)
t.keys()
t['Subject']
t['From']
t.as_string()
'''
[{"emailAddress":"alkekk42@gmail.com","action":"failed",
'''
re.findall(r'\[\{\"emailAddress\":\"(.+)\",\"action\":\"failed\"',t.as_string())

def get_all_fails(path):
    result = []
    files = os.listdir(path)
    for file in files:
        if '.eml' in file:
            fileaddress = path + '/' + file
            f = open(fileaddress,'r')
            emailParser = email.parser.Parser()
            remail = emailParser.parse(f)
            if 'Subject' in remail.keys() and 'From' in remail.keys():
                if remail['Subject'] == 'AWS Notification Message' and remail['From'] =='Bounces <no-reply@sns.amazonaws.com>':
                    failedadd = re.findall(r'\[\{\"emailAddress\":\"(.+)\",\"action\":\"failed\"',remail.as_string())
                    if 'amirmirza1@gmail.com' in remail.as_string():
                        print('+++',file)
                    result.append(failedadd)
            f.close()
    return result

result = get_all_fails('/users/andy/desktop/Inbox')    


results = []
for i in result:
    if len(i) >=1 :
        results.append(i[0])
        
len(set(results))

with open('/users/andy/desktop/forzabir.csv','w') as f:
    fieldname = ['failed']
    csvWriter = csv.DictWriter(f,fieldnames=fieldname)
    csvWriter.writeheader()
    for i in set(results):
        try:
            csvWriter.writerow({'failed':i})
        except Exception:
            pass
    f.close()
    
