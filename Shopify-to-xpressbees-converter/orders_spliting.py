import streamlit as st
import os
import csv
def save_uploadedfile(uploadedfile):
        with open(os.path.join("",uploadedfile.name),"wb") as f:
            f.write(uploadedfile.getbuffer())
        return st.success("Saved File:{} to tempDir".format(uploadedfile.name))

# data_lines = open("shopify_orders_export.csv",'r').read().split('\n')
# open("shopify_orders_export_splitted.csv",'w').write('Name,Email,Financial Status,Paid at,Fulfillment Status,Fulfilled at,Accepts Marketing,Currency,Subtotal,Shipping,Taxes,Total,Discount Code,Discount Amount,Shipping Method,Created at,Lineitem quantity,Lineitem name,Lineitem price,Lineitem compare at price,Lineitem sku,Lineitem requires shipping,Lineitem taxable,Lineitem fulfillment status,Billing Name,Billing Street,Billing Address1,Billing Address2,Billing Company,Billing City,Billing Zip,Billing Province,Billing Country,Billing Phone,Shipping Name,Shipping Street,Shipping Address1,Shipping Address2,Shipping Company,Shipping City,Shipping Zip,Shipping Province,Shipping Country,Shipping Phone,Notes,Note Attributes,Cancelled at,Payment Method,Payment Reference,Refunded Amount,Vendor,Id,Tags,Risk Level,Source,Lineitem discount,Tax 1 Name,Tax 1 Value,Tax 2 Name,Tax 2 Value,Tax 3 Name,Tax 3 Value,Tax 4 Name,Tax 4 Value,Tax 5 Name,Tax 5 Value,Phone,Receipt Number,Duties,Billing Province Name,Shipping Province Name,Payment Terms Name,Next Payment Due At\n')

product_dict = {'Bareilly ki Burfi':307,'Balushahi':309,'Badam Patisa (400gm)':279,'Anjeer Burfi (400gms)':659,'Panjiri (400gm)':309,"Gaya's Khowa Anarsa (400gm)":300} 


data_file = st.file_uploader("Upload shopify exported csv file to split orders : ",type=["csv"])

if data_file is not None:
    save_uploadedfile(data_file)
    prev_order_id = ''
    prev_order_num = 0
    prev_data = [0]
    fields = []
    rows = []
    new_rows = []
    data_lines = open(data_file.name,'r')
    csvreader = csv.reader(data_lines)

    fields = next(csvreader)
    for row in csvreader:
        rows.append(row)

    csvfile = open("shopify_orders_export_splitted.csv",'w')
    writer = csv.writer(csvfile)
    writer.writerow(fields)
    # csvfile = open("shopify_orders_export_splitted.csv",'a')
    # writer = csv.writer(csvfile)
    for data in rows:
        if len(data[0]) < 3:
            continue
        order_id = data[0]
        curr_data = data
        if prev_order_id == order_id:
            data = prev_data
            prev_order_num += 1
            # data[0] += '_' + str(prev_order_num)
            data[16] = curr_data[16]
            data[17] = curr_data[17]
            data[18] = curr_data[18]
            data[19] = curr_data[19]
            data[21] = curr_data[21]
            data[22] = curr_data[22]
            data[23] = curr_data[23]
        else:
            prev_order_num = 0

        data[0] = order_id + '_' + str(prev_order_num)
        
        csvfile = open("shopify_orders_export_splitted.csv",'a')
        writer = csv.writer(csvfile)
        print(data)
        writer.writerow(data)
        new_rows.append(data)
        prev_order_id = order_id   
        prev_data = data


    if st.button("Email order splitted csv file"):
        pass
        # st.write(open("shopify_orders_export_splitted.csv",'rb').read())
        # f'<a href="data:file/csv;base64" download="shopify_orders_export_splitted.csv">Download</a>'
# b64 = base64.b64encode(csv.encode().decode())
# f'<a href="data:file/csv;base64,{b64}" download="shopify_orders_export_splitted.csv">Download</a>'
