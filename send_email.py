import smtplib
import os
import ssl
from dotenv import load_dotenv

load_dotenv()
CONTEXT = ssl.create_default_context()
EMAIL_ID = os.environ.get('EMAIL_ID')
PASSWORD = os.environ.get('PASSWORD')
SMTP_SERVER = os.environ.get('SMTP_SERVER')
SMTP_PORT = os.environ.get('SMTP_PORT')
SMTP_PORT = int(SMTP_PORT)

def send_email(to,body):
    print('step 1')
    smtp = smtplib.SMTP_SSL(SMTP_SERVER,SMTP_PORT, context=ssl.create_default_context())  # for SSL connection
    # smtp = smtplib.SMTP(SMTP_SERVER,SMTP_PORT)    # for TLS connection
    # print('4')
    print('step 2')
    smtp.ehlo()  # send the extended hello to our server
    print('step 3')
    # smtp.ssl
    # smtp.starttls(context=CONTEXT)  # tell server we want to communicate with TLS encryption
    # smtp.connect()
    # print('5')
    print('step 4')
    # print(SMTP_PORT)
    # print(EMAIL_ID)
    # print(PASSWORD)
    smtp.login(EMAIL_ID,PASSWORD)  # login to our email server
    # smtp.auth_login(EMAIL_ID, PASSWORD)
    # print('6')
    # send our email message 'msg' to our boss
    print('step 5')
    smtp.sendmail(from_addr = EMAIL_ID,to_addrs = to,msg = body)
    # smtp.send_message(from_addr = EMAIL_ID,to_addrs = to,msg = str(body))
    print('7 - email sent')             
    smtp.quit()  # finally, don't forget to close the connection