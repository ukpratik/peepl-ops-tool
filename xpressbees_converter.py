import streamlit as st
import os
import csv
import products_info_utils as pro_db

pro_db_dict = pro_db.load_product_db()

def convert_to_xprsbs_format():
    # if data_file is not None:
    
    data_lines = open("uploaded_files/shopify_orders_export_splitted.csv",'r')
    data_lines = csv.reader(data_lines)

    skip_those_fields = next(data_lines)
    new_fields = ["Order ID","Payment Type","Tags","First Name","Last Name","Address 1","Address 2","Phone","City","State","Pincode",'Weight(gm)',"Length(cm)","Height(cm)","Breadth(cm)","Shipping Charges","Discount","SKU(1)","Product(1)","Quantity(1)","Price(1)","SKU(2)","Product(2)","Quantity(2)","Price(2)"]

    file_export = open('xpressbees-import.csv','w')
    file_exporter = csv.writer(file_export)
    file_exporter.writerow(new_fields)

    # file_export = open('xpressbees-import.csv','a')
    # file_exporter = csv.writer(file_export)

    for data_line in data_lines:
        NAME = data_line[0]
        # print(NAME)
        if len(NAME) < 2:
            continue

        EMAIL = data_line[1]
        FINANCIAL_STATUS = data_line[2]
        PAID_AT = data_line[3]
        FULFILLMENT_STATUS = data_line[4]
        FULFILLED_AT = data_line[5]
        ACCEPTS_MARKETING = data_line[6]
        CURRENCY = data_line[7]
        SUBTOTAL = data_line[8]
        SHIPPING = data_line[9]
        TAXES = data_line[10]
        TOTAL_DISCOUNT = data_line[11]
        DISCOUNT_CODE = data_line[12]
        SHIPPING_METHOD = data_line[13]
        CREATED_AT = data_line[14]
        LINEITEM_QUANTITY = data_line[15]
        LINEITEM_NAME = data_line[17]
        BILLING_NAME = data_line[24]


        SHIPPING_ADDRESS_1 = data_line[36]
        SHIPPING_ADDRESS_2 = data_line[37]
        PHONE = data_line[43]  # Shipping Phone Number
        CITY = data_line[39]
        STATE = data_line[70]
        PINCODE = data_line[40]

        print(LINEITEM_NAME)
        LINEITEM_NAME = LINEITEM_NAME.split('(')[0]
        if LINEITEM_NAME[-1] == ' ':
            LINEITEM_NAME = LINEITEM_NAME[:-1]
        print(LINEITEM_NAME)

        if LINEITEM_NAME in pro_db_dict.keys():
            WEIGHT = pro_db_dict[LINEITEM_NAME][0]
            LENGTH = pro_db_dict[LINEITEM_NAME][1]
            HEIGHT = pro_db_dict[LINEITEM_NAME][2]
            BREADTH = pro_db_dict[LINEITEM_NAME][3]
        else:
            WEIGHT = '400'
            LENGTH = '10'
            HEIGHT = '10'
            BREADTH = '10'
        QUANTITY = ''
        PRICE = data_line[27]


        PAYMENT_TYPE = ''

        FIRST_NAME = ''
        LAST_NAME = ''

        SHIPPING_CHARGES = ''
        DISCOUNT = ''
        SKU = ''
        PRODUCT_1 = ''
        QUANTITY_1 = ''
        PRICE_1 = ''

        ORDER_ID = NAME

        if FINANCIAL_STATUS == 'paid':
            PAYMENT_TYPE = 'Prepaid'
        elif FINANCIAL_STATUS == 'pending':
            PAYMENT_TYPE = 'Cash on Delivery'
        else:
            PAYMENT_TYPE = 'void'

        TAGS = ''

        name_array = BILLING_NAME.split(' ')
        first_name = ''
        last_name = ''
        for i in range(len(name_array)):
            if i < len(name_array) - 1:
                first_name += ' ' + name_array[i]
            else:
                last_name = name_array[i]

        # print('Name Array :' + str(name_array))
        # print('First Name :' + first_name)
        # print("Last Name :" + last_name)

        address_1 = SHIPPING_ADDRESS_1
        address_2 = SHIPPING_ADDRESS_2
        phone = PHONE
        city = CITY
        state = STATE
        pincode = PINCODE
        weight = WEIGHT
        length = LENGTH
        height = HEIGHT
        breadth = BREADTH
        shipping_charges = SHIPPING_CHARGES
        discount = DISCOUNT

        # print("step in transit.. id 1099999")
        data_format = """{order_id},{payment_type},{tags},{first_name},{last_name},{address_1},{address_2},{phone},{city},{state},{pincode},{weight},{length},{height},{breadth},{shipping_charges},{discount},{sku_1},{product_1},{quantity_1},{price_1},,,,""".format(order_id=ORDER_ID,payment_type=PAYMENT_TYPE,tags=TAGS,first_name=first_name,last_name=last_name,address_1=address_1,address_2=address_2,phone=PHONE,city=CITY,state=STATE,pincode=PINCODE,weight=weight,length=length,height=height,breadth=breadth,shipping_charges=shipping_charges,discount=discount,sku_1=SKU,product_1=PRODUCT_1,quantity_1=QUANTITY_1,price_1=PRICE_1)
        # open('xpressbees-import.csv','w') # csv_export = 
        data_arr = [ORDER_ID,PAYMENT_TYPE,TAGS,first_name,last_name,address_1,address_2,PHONE,CITY,STATE,PINCODE,weight,length,height,breadth,shipping_charges,discount,SKU,PRODUCT_1,QUANTITY_1,PRICE_1]
        # open('uploaded_files/xpressbees-import.csv','a').write(data_format + '\n')
        file_export = open('xpressbees-import.csv','a')
        file_exporter = csv.writer(file_export)
        file_exporter.writerow(data_arr)