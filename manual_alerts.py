import streamlit as st
from twilio_sms_api import send_sms
from send_email import send_email
from email_message import mail_message

def manual_sms():
    st.header('Send Manual SMS')
    template = ''
    template_selected = st.selectbox(key='sms_type',label='Select template : ', options=['Order Placed', 'Order Shipped', 'Order Delivered'])

    to_mobile_number = st.text_input('Send to mobile number: ')

    if template_selected == 'Order Placed':
        template = "Hi {name}!, Your order(s) at Peepl has been placed. Thanks for choosing Peepl"
    elif template_selected == 'Order Shipped':
        template = "Hi {name}!, Your order(s) at Peepl has been shipped. Thanks for choosing Peepl"
    elif template_selected == 'Order Delivered':
        template = "Hi {name}!, Your order(s) from Peepl was Delivered. Thanks for choosing Peepl"

    message = st.text_area(label='Enter your sms here:', value=template)

    if st.button(label='Send SMS'):
        try:
            send_sms(to=to_mobile_number,body=message)
            st.text("Hurray, SMS to " + to_mobile_number + ' sent successfully. :)')
        except:
            st.text('Oops SMS to ' + to_mobile_number + ' failed. :(')


def manual_email():
    st.header('Send Manual Email')
    template = ''
    template_selected = st.selectbox(key='email_type',label='Select template : ', options=['Order Placed', 'Order Shipped', 'Order Delivered'])

    email_id = st.text_input('Send to Email Id: ')

    if template_selected == 'Order Placed':
        template = "Hi {name}!, Your order(s) at Peepl has been placed. Thanks for choosing Peepl"
    elif template_selected == 'Order Shipped':
        template = "Hi {name}!, Your order(s) at Peepl has been shipped. Thanks for choosing Peepl"
    elif template_selected == 'Order Delivered':
        template = "Hi {name}!, Your order(s) from Peepl was Delivered. Thanks for choosing Peepl"

    subject = st.text_input('Enter subject :', value='Peepl Notification')
    message = st.text_area(label='Enter your email body here:', value=template)
    email_body = mail_message(subject=subject,text=message)

    if st.button(label='Send Email'):
        try:
            send_email(to=email_id,body=email_body.as_string())
            st.text("Hurray, email to " + email_id + ' sent successfully. :)')
        except:
            st.text('Oops email to ' + email_id + ' failed. :(')


def set_template(template):
    template = template