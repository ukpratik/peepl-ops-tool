import streamlit as st
import os
import csv
# def save_uploadedfile(uploadedfile):
#         with open(os.path.join("",uploadedfile.name),"wb") as f:
#             f.write(uploadedfile.getbuffer())
#         return st.success("Saved File:{} to tempDir".format(uploadedfile.name))

def get_history(filename='history.csv'):
    history_file = open(filename,'r')
    history_file_reader = csv.reader(history_file)
    history = []
    for data in history_file_reader:
        history.append(data)
    return history

def append_history(first_part,to_append_part,filename='history.csv'):
    history_file = open(filename,'w')
    history_file_writer = csv.writer(history_file)
    history_file_writer.writerows(first_part)
    history_file_writer.writerows(to_append_part)

def orders_split(data_file):
    new_history = []
    old_history = get_history()
    prev_orders = []
    for order in old_history:
        try:
            prev_orders = order[0]
        except IndexError:
            print(IndexError)
    if data_file is not None:
        prev_order_id = ''
        prev_order_num = 0
        prev_data = [0]
        fields = []
        rows = []
        new_rows = []
        data_lines = open("uploaded_files/" + data_file.name,'r')
        csvreader = csv.reader(data_lines)

        fields = next(csvreader)
        for row in csvreader:
            rows.append(row)

        csvfile = open("uploaded_files/shopify_orders_export_splitted.csv",'w')
        writer = csv.writer(csvfile)
        writer.writerow(fields)
        # csvfile = open("shopify_orders_export_splitted.csv",'a')
        # writer = csv.writer(csvfile)
        for data in rows:
            # print(data)
            if len(data[0]) < 3:
                continue

            # If order cancelled has value, then continue,  {data[43] is Order cancelled at}
            if len(data[46]) > 3: 
                continue

            order_id = data[0]
            curr_data = data
            if prev_order_id == order_id:
                data = prev_data
                prev_order_num += 1
                # data[0] += '_' + str(prev_order_num)
                data[9] = curr_data[9]   # Shipping Charges remain same, only inlcuded in first sub order number
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
            
            # Pincode (Shipping Pincode) Data Sanitizing is done here
            data[40] = data[40].replace("'", '').replace(" ", '').replace("+91",'')

            # Mobile Number (Shipping Phone) Data Sanitizing is done here
            temp = "".join(data[43])

            temp = temp.replace("'", '').replace(" ", '').replace("+91",'')
            
            data[43] = temp
            try:
                if temp[0] == '0':
                    data[43] = temp[1:]
            except:
                continue

            csvfile = open("uploaded_files/shopify_orders_export_splitted.csv",'a')
            writer = csv.writer(csvfile)
            # print(data)
            writer.writerow(data)
            new_rows.append(data)
            prev_order_id = order_id   
            prev_data = data

            new_data = [data[0],data[1],0,0]
            if order_id not in prev_orders:
                new_history.append(new_data)
            append_history(first_part=old_history,to_append_part=new_history)


        