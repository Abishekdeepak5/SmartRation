from app.dao.DatabaseUtil import *

def addProduct(product):
    dict_data=product.__dict__
    print(dict_data)
    return insertRow(product.get_table_name(),dict_data)

def get_product_by_id(productId):
    data,count=getRowsWithId("product","product_id",productId)
    return data[1][0]

def get_products():
    return getRows("product")

def editProduct(product):
    productId=product.get_product_id()
    return updateRow("product",product.__dict__,"product_id",productId)

def deleteProduct(productId):
    deleteRow("product","product_id",productId)