st.subheader("Email & SMS Automation : ")
    data_file = st.file_uploader("Upload csv file",type=["csv",'numbers'])
    if data_file is not None:
        save_uploadedfile(data_file)
        entries = open("uploaded_files/" + data_file.name,'r').read().split('\n')

    if (st.button(label="Run Process")):
        for entry in entries:
            data = entry.split(',')
            # print(data)
            # st.text(data)
            if len(data) < 2:
                continue
            ORDER_ID = data[2]
            AWB_NUMBER = data[8]
            INVOICE_LINK = ''
            try:
                EMAIL_ID = dict_order_email[ORDER_ID][0]
                if dict_order_email[ORDER_ID][1] == 1 and dict_order_email[ORDER_ID][2] == 1:
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

            
            email_filled_template = content_template.email_body_template(CUSTOMER_NAME,TRACKING_ID,TRACKING_LINK,INVOICE_LINK)
            mail_body = mail_message(subject="Your Order from Peepl Shipped",text=email_filled_template)
            # st.text("=============================================")
            try:
                if dict_order_email[ORDER_ID][1] == 1:
                    print('Email already sent for order : ' + ORDER_ID)  
                else:
                    if (not DEBUGGING):
                        send_email(EMAIL_ID,mail_body.as_string())
                        dict_order_email[ORDER_ID] = [dict_order_email[ORDER_ID][0],1,dict_order_email[ORDER_ID][2]]
                    print("Email Sent to " + EMAIL_ID)
                    st.text('[' + ORDER_ID + "] Email Sent to " + EMAIL_ID)
            except :
                print(" ** Alert Email not sent to : " + EMAIL_ID + '\n')
                st.text(ORDER_ID + " ** Alert Email not sent to : " + EMAIL_ID + '\n')
                # print(sys.exc_info()[1])
                print("\n")

            
            sms_filled_template = content_template.sms_body_template(CUSTOMER_NAME,TRACKING_ID,TRACKING_LINK,INVOICE_LINK)
            try:
                if dict_order_email[ORDER_ID][2] == 1:
                    print('SMS already sent for order : ' + ORDER_ID)
                else:
                    if not DEBUGGING:
                        send_sms(to=MOBILE_NUMBER,body=sms_filled_template)
                        dict_order_email[ORDER_ID] = [dict_order_email[ORDER_ID][0],dict_order_email[ORDER_ID][1],1]
                    print("SMS Sent to " + MOBILE_NUMBER)
                    print(dict_order_email[ORDER_ID])
                    print(dict_order_email[ORDER_ID][1])
                    st.text('[' + ORDER_ID + "] SMS Sent to " + MOBILE_NUMBER)
            except :
                print("\n ** Alert SMS not sent to : " + MOBILE_NUMBER + '\n')
                st.text("\n ** Alert SMS not sent to : " + MOBILE_NUMBER + '\n')
                # print(sys.exc_info()[1])
                print("\n")
            # st.text("=============================================")
        open('order_id-email_id.csv','w')
        # open('order_id-email_id.csv','a').write('order_id,email_address,email_sent,sms_sent\n')
        for key in dict_order_email.keys():
            email_adress = dict_order_email[key][0]
            email_sent = dict_order_email[key][1]
            sms_sent = dict_order_email[key][2]
            open('order_id-email_id.csv','a').write(str(key) + ',' + str(email_adress) + ',' + str(email_sent) + ',' + str(sms_sent) + '\n')
