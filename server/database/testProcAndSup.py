from tables import Supplier, Product, Reagent, Grid, Session

import pymysql
from sqlalchemy import exc

# --------------------------

s = Session()
suppliers = s.query(Supplier).all()

for supplier in suppliers:  # 列出供應商
    print("*: ", supplier.super_name)
    # print(product._suppliers)
    # for product in supplier._products:  # 列出產品類別
    #    print("--> ", product.name)
    for reagent in supplier._reagents:  # 列出該供應商的所有試劑編號
        print("--> ", reagent.reag_id)

    # for product in supplier._products:  # 列出產品類別
    #    print("--> ", product.name)
    print('---')

s.close()
