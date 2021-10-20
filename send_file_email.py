import streamlit as st
from email_message import mail_message
from send_email import send_email

def send_file_email(attachment,key,button_label="Submit Button",subject="mail from automation tool",text="PFA"):
    sent_to_2 = st.selectbox(key=key,label='Send email to :', options=['peepl.official@gmail.com','ukeykiran26@gmail.com','pratikuk99@gmail.com','pratik.ukey@vehere.com'])
    if st.button(key=key+key,label="Email csv file to upload at Xpressbees"):
        mail_body = mail_message(subject=subject,text=text,attachment=attachment)
        send_email(to=sent_to_2,body=mail_body.as_string())
        st.success("CSV sent successfully file :")