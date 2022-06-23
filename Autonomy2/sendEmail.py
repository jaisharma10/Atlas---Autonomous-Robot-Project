# =====================================================
#                    Send Emails
# =====================================================

import os
from datetime import datetime
import smtplib
from smtplib import SMTP
from smtplib import SMTPException
import email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

from picamera import PiCamera
import time

# function to send email
def sendit():
    # Email information
    usr = 'myEmail@gmail.com'
    pwd = 'secret'

    # Destination email information
    toAdd = ['email_1','email_2']
    fromAdd = usr

    msg = MIMEMultipart()
    sub = 'Final Challenge Update'
    msg['Subject'] = sub
    msg['From'] = fromAdd
    # msg['to'] = toAdd
    msg['to'] = ",".join(toAdd)
    msg.preamble = 'Grand Challenge --> Block Succesfully Picked Up'

    # Email text
    body = MIMEText('Block Succesfully Retrieved! Thank You - Jai Sharma')
    msg.attach(body)
    
    
    # Attach Image
    # fp = open(fName, 'rb')
    # img = MIMEImage(fp.read())
    # fp.close()
    # msg.attach(img)

    # Send Email
    s = smtplib.SMTP('smtp.gmail.com', 587)

    s.ehlo()
    s.starttls()
    s.ehlo()

    s.login(usr, pwd)
    s.sendmail(fromAdd, toAdd, msg.as_string())
    s.quit()

    print('The Image has been Emailed!')
