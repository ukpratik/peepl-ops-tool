# import sys
import streamlit as st
import os
from dotenv import load_dotenv
from email_message import mail_message
from send_email import send_email
from twilio_sms_api import send_sms
import content_template
from manual_alerts import manual_sms, manual_email
from orders_spliting import orders_split
from send_file_email import send_file_email
from xpressbees_converter import convert_to_xprsbs_format
import run_process
# from Shopify-to-xpressbees-converter import orders_splitting

load_dotenv()
DEBUGGING = True
flag = 0
authenticated = False
# uploaded_file = st.file_uploader("Upload file to process : ")

# if uploaded_file is not None:
#     # stringio = StringIO(uploaded_file.getvalue().decode('utf-8'))
#     # file_data = uploaded_file.getvalue().decode('utf-8')
#     # entries = file_data.read().split('\n')
#     # bytes_data = uploaded_file.getvalue()
#     pass
username = st.text_input('Enter username : ')
password = st.text_input('Enter password : ',type='password')

def is_authenticated(username,password):
    return username == "peepl" and password == "automation"

def save_uploadedfile(uploadedfile):
    with open(os.path.join("uploaded_files",uploadedfile.name),"wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved File:{} to tempDir".format(uploadedfile.name))

if not is_authenticated(username,password):
    st.warning("No authentication")
else:
    authenticated = True

    dict_order_email = {}
    with open('order_id-email_id.csv','r') as f:
        lines = f.read().split('\n')
    for line in lines:
        if len(line) < 2:
            continue
        line = line.split(',')
        if line[0] in dict_order_email.keys():
            print("order id repeated .. : " + str(line[0]))
            continue
        else:
            dict_order_email[line[0]] = [line[1],line[2],line[3]]
            
    
    # print(dict_order_email)
    st.title('Process Automation Tool')
    if DEBUGGING:
        st.text('DEBUGGING TRUE')


    st.subheader("Order Splitting Automation : ")
    data_file = st.file_uploader("Upload shopify exported csv file to split orders : ",type=["csv"])
    if data_file is not None:
        save_uploadedfile(data_file)
        orders_split(data_file)
        st.text("Order Splitting Done")
        send_file_email(key='abcd',attachment="uploaded_files/shopify_orders_export_splitted.csv",button_label="Send splitted orders file mail",subject="Splitted orders file")
        flag = 1

    if flag == 1:
        convert_to_xprsbs_format()
        st.text("Formatting Done")
        send_file_email(key='xyz',attachment="xpressbees-import.csv",button_label="Send xpressbees format orders file mail",subject="Upload to xpressbees")

    st.subheader("Email & SMS Automation : ")
    data_file = st.file_uploader("Upload csv file",type=["csv",'numbers'])
    if data_file is not None:
        save_uploadedfile(data_file)
        run_process.run_process(data_file)


if authenticated:
    manual_sms()
    manual_email()