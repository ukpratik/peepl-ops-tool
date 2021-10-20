import csv

def load_product_db():

    data_arr = {}

    with open("product_db.csv",'r') as f:
        product_db = csv.reader(f)
        skip_headlines = next(product_db)

        for data in product_db:
            product_name = data[1]

            wt = data[15]  # 0.4 kg
            if wt == '':
                wt = 'x'
            dimensions = data[16] # L*B*H (cms)

            wt = wt.split(' ')[0] # to grams
            # wt = str(int(wt))

            dims = dimensions.split(' ')[0]
            print(dimensions)
            print(dims)
            dims = dims.split('*')
            print(dims)
            if len(dims) == 3:
                dim_l = dims[0]
                dim_b = dims[1]
                dim_h = dims[2]
            else:
                dim_l = 'x'
                dim_b = 'x'
                dim_h = 'x'

            temp = []
            temp.append(wt)
            temp.append(dim_l)
            temp.append(dim_b)
            temp.append(dim_h)

            data_arr[product_name] = temp

    return data_arr

# print(load_product_db())
