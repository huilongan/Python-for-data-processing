# -*- coding: utf-8 -*-
"""
Created on Mon Oct 10 10:58:50 2016

@author: Andy
"""
from email.message import EmailMessage
from email.headerregistry import Address
from email.utils import make_msgid
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
from smtplib import SMTPException
from email.headerregistry import Address
import argparse
import smtplib
import urllib.request
import bs4
import re
import csv
# get the message
def get_info(url):
    html = urllib.request.urlopen(url)
    bsobj = bs4.BeautifulSoup(html,'xml')
    body = bsobj.find('div',{'id':'body'})
    name = bsobj.find('div',{'id':'name'})
    sign = bsobj.find('div',{'id':'sign'})
    return body,name,sign



# for 29 categories
#divs = bsobj.findAll('div',id = re.compile('Category [0-9]+'))
#
#names = []
#bodys = []
## bodys
#for i in divs:
#    body = i.find('div',{'id':'message'})
#    name = i.find('p',{'id':'name'})
#    bodys.append(body)
#    names.append(name)


# Create the base text message.

#fussellolivia@yahoo.com
#: ofussell@cincs.com 
'''
Get the result
'''
def get_names(address):
    result = []
    with open(address,'r',encoding='ISO-8859-1') as f:
        fieldnames = ['ind','full_name','F_name','L_name','Email']
        csvreader = csv.DictReader(f,fieldnames = fieldnames)
        for reader in csvreader:
            full_name = reader['full_name']
            F_name = reader['F_name']
            L_name = reader['L_name']
            Emaila = reader['Email']
            result.append((full_name,F_name,L_name,Emaila))
        f.close()
    result.pop(0)
    return result
def send_message(Toname,Toadd,Todomain,Tofirst,emailAd,emailPs):
    msg = EmailMessage()
    msg['Subject'] = "How can we protect our Properties and Communities from Climate Risk?"
    msg['From'] = Address("Olivia Fussell", "ofussell", "cincs.com")
    msg['To'] = Address(Toname, Toadd, Todomain)
    
    # Add the html version.  This converts the message into a multipart/alternative
    # container, with the original text message as the first part and the new html
    # message as the second part.
    asparagus_cid = make_msgid()
    msg.add_alternative("""<p> Dear {name},</p><br>{content}<br>{signiture}
    """.format(name=Tofirst,content = body,signiture = sign), subtype='html')
    # note that we needed to peel the <> off the msgid for use in the html.

    # Send the message via local SMTP server.
    try:
        server = smtplib.SMTP("smtp.mail.yahoo.com",587)
        server.ehlo()
        server.starttls()
        server.login(emailAd,emailPs)
        server.send_message(msg)
        base = '/users/andy/desktop/api/records/'
        nameForMSG = 'To_'+ Toname+'.msg'
        with open(base + nameForMSG, 'wb') as f:
            f.write(bytes(msg))
            f.close()
        print('Successed to send email to '+Toname)
    except Exception:
        print('failed to send email to '+Toname)

def main():
    print('{}'.format('********************************'))
    print('{}'.format('Auto email-send machine'))
    print('{}'.format('By Andy An'))
    print('{}'.format('********************************'))
    urlEmail = str(input('Where is your email HTML? for example:\'file:///Users/Andy/Desktop/demo_files/email.html\' '))
    body,name,sign = get_info(urlEmail)
    emailAd = str(input('eamilAddress: '))
    emailPs = str(input('emailPassword: '))
    address = str(input('Your email list? for example: \'/users/andy/desktop/api/emailS.csv\' '))
    lists = get_names(address)
    for i in lists:
        if '@' in i[3]:
            Toadd,Todomain = i[3].split('@')
            send_message(i[0],Toadd,Todomain,i[1],emailAd,emailPs)

if __name__ == '__main__':
    main()
