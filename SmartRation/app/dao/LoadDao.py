from app.dao.DatabaseUtil import *
from app.models import RationTransport
from app.models import RationTransportProduct
from app.models import RationProduct
from app.models import Product
from app.common.Util import get_current_date
from app.supabase_config import supabase

def addLoad(product:Product,allocated_qty):
    rationTransport,error=getLoadTransport()
    rationTransportObj=None
    if len(rationTransport[1]) == 0:
        rationTransport=RationTransport.RationTransport()
        rationTransport.set_status("loading")
        response,error=insertRow(RationTransport.RationTransport.TABLE_NAME,rationTransport.__dict__)
        rationTransportObj=response[1][0]
    else:
        rationTransportObj=rationTransport[1][0]
    rationTransportProduct=RationTransportProduct.RationTransportProduct()
    rationTransportProduct.set_ration_transport_id(rationTransportObj["ration_transport_id"])
    rationTransportProduct.set_product_id(product.get_product_id())
    rationTransportProduct.set_allocated_qty(allocated_qty)
    rationTransportProduct.set_update_date(get_current_date())
    insertRationTransportProduct(rationTransportProduct)

def get_loads():
    loading_ids = supabase.table("ration_transport").select("ration_transport_id").eq("status", RationTransport.Status.LOADING.value).execute()
    ids = [row["ration_transport_id"] for row in loading_ids.data]
    data,count = supabase.table("ration_transport_product").select("*,product(*),ration_transport(*)").in_("ration_transport_id", ids).execute()
    return data[1]


def insertRationTransportProduct(rationTransportProduct):
    return insertRow(RationTransportProduct.RationTransportProduct.TABLE_NAME,rationTransportProduct.__dict__)

def getLoadTransport():
    return getRowsWithId(RationTransport.RationTransport.TABLE_NAME,"status","loading")

def deleteProduct(productId):
    deleteRow("product","product_id",productId)

# def getRationTransportProductById(ration_transport_product_id):
#     data,count=supabase.table(RationTransportProduct.RationTransportProduct.TABLE_NAME).select("*,product(*),ration_transport(*)").eq("ration_transport_product_id", ration_transport_product_id).execute()
#     return  data[1][0]

def getRationTransportProductById(ration_transport_product_id):
    send_ids = supabase.table(RationTransport.RationTransport.TABLE_NAME).select("ration_transport_id").eq("status", RationTransport.Status.SEND.value).execute()
    ids = [row["ration_transport_id"] for row in send_ids.data]
    data,count = supabase.table(RationTransportProduct.RationTransportProduct.TABLE_NAME).select("*,product(*),ration_transport(*)").eq("ration_transport_product_id", ration_transport_product_id).in_("ration_transport_id", ids).execute()
    # data,count=supabase.table(RationTransportProduct.RationTransportProduct.TABLE_NAME).select("*,product(*),ration_transport(*)").eq("ration_transport_product_id", ration_transport_product_id).execute()
    if len(data[1])==0:
        return None
    return  data[1][0]

def editRationTransportProduct(rationTransportProduct):
    return updateRow(RationTransportProduct.RationTransportProduct.TABLE_NAME,rationTransportProduct.__dict__,"ration_transport_product_id",rationTransportProduct.get_ration_transport_product_id())

def deleteRationTransportProduct(ration_transport_product_id):
    return deleteRow(RationTransportProduct.RationTransportProduct.TABLE_NAME,"ration_transport_product_id",ration_transport_product_id)

def editRationTransport(rationTransport):
    return updateRow(RationTransport.RationTransport.TABLE_NAME,rationTransport.__dict__,"ration_transport_id",rationTransport.get_ration_transport_id())

def getTransportProduct(ration_transport_id):
    data,count=getRowsWithId(RationTransportProduct.RationTransportProduct.TABLE_NAME,"ration_transport_id",ration_transport_id)
    return data[1]

def getRationTransportByRation(ration_id):
    data,count=supabase.table(RationTransport.RationTransport.TABLE_NAME).select("*").eq("status", RationTransport.Status.SEND.value).eq("ration_id",ration_id).execute()
    if len(data[1])==0:
        return None
    return data[1][0]

def getRationTransportProduct(ration_transport_id):
    data,count=getRowsWithId(RationTransportProduct.RationTransportProduct.TABLE_NAME,'ration_transport_id',ration_transport_id)
    return data[1]

def getRationProduct(product_id):
    data,count=getRowsWithId(RationProduct.RationProduct.TABLE_NAME,'product_id',product_id)
    if len(data[1])==0:
        return None
    return data[1][0]

def createRationProduct(rationProduct):
    insertRow(RationProduct.RationProduct.TABLE_NAME,rationProduct.__dict__)

def updateRationProduct(rationProduct:RationProduct):
    updateRow(RationProduct.RationProduct.TABLE_NAME,rationProduct.__dict__,'ration_product_id',rationProduct.get_ration_product_id())

def updateRationTransport(rationTransport):
    updateRow(RationTransport.RationTransport.TABLE_NAME,rationTransport.__dict__,'ration_transport_id',rationTransport.get_ration_transport_id())