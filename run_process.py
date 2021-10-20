import streamlit as st
import csv
import os
from email_message import mail_message
from send_email import send_email
from twilio_sms_api import send_sms
import content_template

# TESTING = True
TESTING = False
SEND_EMAIL = True
SEND_SMS = False


dict_order_email = {}
dict_order_history = []
entries = []
fields = ['order_id','email_address','email_sent','sms_sent']

def save_uploadedfile(uploadedfile):
        with open(os.path.join("uploaded_files",uploadedfile.name),"wb") as f:
            f.write(uploadedfile.getbuffer())
        return st.success("Saved File:{} to tempDir".format(uploadedfile.name))

def create_dict(order_id,e_add,email,sms):
    dict_ = {'order_id':order_id,'email_address':e_add,'email_sent':email,'sms_sent':sms}
    return dict_

def get_alerts_history(filename="history.csv"):
    print("Got into alerts history ...")
    history_file = open(filename,'r')
    # print("step 1 clear")
    history_file_reader = csv.reader(history_file)
    # print("step 2 clear")
    # skip_files = next(history_file)
    print(history_file_reader)
    for entry in history_file_reader:
        # print('Entry : ' + str(entry))
        if len(entry[0]) < 2:
            continue
        # print('dec')
        dict_order_email[entry[0]] = [entry[1],entry[2],entry[3]]
        # dict_order_history[entry[0]] = [entry[1],entry[2],entry[3]]
    print(dict_order_email)
    

def run_process(data_file):
    if data_file is not None:
        file_read = open("uploaded_files/" + data_file.name,'r')
        entries = csv.reader(file_read)
        skip_files = next(entries)
        get_alerts_history()
        # print(dict_order_email)

        for entry in entries:
            data = entry
            # print(data)
            # st.text(data)
            if len(data) < 2:
                continue
            ORDER_ID = data[2]
            AWB_NUMBER = data[8]
            INVOICE_LINK = ''
            try:
                print(ORDER_ID)
                EMAIL_ID = dict_order_email[ORDER_ID][0]
                print(EMAIL_ID)
                if dict_order_email[ORDER_ID][1] == '1' and dict_order_email[ORDER_ID][2] == '1':
                    print('email and sms already sent for order : ' + str(ORDER_ID))
                    continue
            except:
                print("some error occured in getting email id ... order_id:" + ORDER_ID + " escaped for now")
                # st.text("some error occured in getting email id ... order_id:" + ORDER_ID + " escaped for now")
                continue
            MOBILE_NUMBER = data[11]
            PRODUCT_NAME = data[36]
            CUSTOMER_NAME = data[10]
            TRACKING_ID = ''
            TRACKING_LINK = "https://www.xpressbees.com/track/"

            if ORDER_ID == 'Order ID':
                continue
            
            if len(ORDER_ID) < 2:
                continue

            if MOBILE_NUMBER[0] != '+':
                MOBILE_NUMBER = '+' + MOBILE_NUMBER

            # print(ORDER_ID)
            
            email_filled_template = content_template.email_body_template(CUSTOMER_NAME,PRODUCT_NAME,TRACKING_ID,TRACKING_LINK,INVOICE_LINK)
            mail_body = mail_message(subject="Your Order from Peepl Shipped",text=email_filled_template)
            # st.text("=============================================")
            try:
                if dict_order_email[ORDER_ID][1] == '1':
                    email_sent = 1
                    print('Email already sent for order : ' + ORDER_ID)  
                else:
                    if (not TESTING) and SEND_EMAIL:
                        send_email(EMAIL_ID,mail_body.as_string())
                        # dict_order_email[ORDER_ID] = [dict_order_email[ORDER_ID][0],1,dict_order_email[ORDER_ID][2]]
                    print("Email Sent to " + EMAIL_ID)
                    email_sent = 1
                    st.text('[' + ORDER_ID + "] Email Sent to " + EMAIL_ID)
            except :
                print(" ** Alert Email not sent to : " + str(EMAIL_ID) + '\n')
                st.text(ORDER_ID + " ** Alert Email not sent to : " + EMAIL_ID + '\n')
                email_sent = 0
                # print(sys.exc_info()[1])
                print("\n")

            
            
            try:
                if dict_order_email[ORDER_ID][2] == '1':
                    print('SMS already sent for order : ' + ORDER_ID)
                    sms_sent = 1
                else:
                    if (not TESTING) and SEND_SMS:
                        sms_filled_template = content_template.sms_body_template(CUSTOMER_NAME,PRODUCT_NAME,TRACKING_ID,TRACKING_LINK,INVOICE_LINK)
                        send_sms(to=MOBILE_NUMBER,body=sms_filled_template)
                        # dict_order_email[ORDER_ID] = [dict_order_email[ORDER_ID][0],dict_order_email[ORDER_ID][1],1]
                    print("SMS Sent to " + MOBILE_NUMBER)
                    # print(dict_order_email[ORDER_ID])
                    sms_sent = 1
                    st.text('[' + ORDER_ID + "] SMS Sent to " + MOBILE_NUMBER)
            except :
                sms_sent = 0
                print("\n ** Alert SMS not sent to : " + MOBILE_NUMBER + '\n')
                st.text("\n ** Alert SMS not sent to : " + MOBILE_NUMBER + '\n')
                # print(sys.exc_info()[1])
                print("\n")
            dict_order_history.append(create_dict(ORDER_ID,EMAIL_ID,email_sent,sms_sent))
            # st.text("=============================================")
        history_file = open('history.csv','w')
        update_history = csv.DictWriter(history_file,fieldnames=fields)
        update_history.writeheader()
        update_history.writerows(dict_order_history)
        # print(dict_order_history)

# data_file = st.file_uploader("Upload csv file",type=["csv",'numbers'])
# if data_file is not None:
#     save_uploadedfile(data_file)
#     run_process(data_file)

print("*********** Hello World! ************")