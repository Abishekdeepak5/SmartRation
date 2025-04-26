from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import Product
from app.dao.ProductDao import *
from app.common.Util import get_current_date
from app.views.InventoryView import *
from app.dao.LoadDao import * 
from app.dao.RationDao import  get_all_rations,get_staff_ration
from app.dao.ProductDao import get_product_by_id,editProduct

def add_load(request,productId):
    if request.method == "POST":
        product=Product.Product()
        product.set_product_id(productId)
        allocated_qty=request.POST.get("allocated_qty")
        try:
            addLoad(product,allocated_qty)
            messages.success(request, "Product Load successfully!")
            return get_all_product(request)
        except Exception as e:
            try:
                if e.code == '23505':
                    messages.error(request, "Error Loading Product. Product already loaded ")
                else:
                    messages.error(request, "Error Loading Product.")
            except:
                messages.error(request, "Error Loading Product")
            return get_all_product(request)
    try:
        product=get_product_by_id(productId)
        return render(request,"product_load.html",{"product":product,"mode":"add"})
    except Exception as e:
        print(e)
        messages.error(request,"Error load")
        return get_all_product(request)

def list_load(request):
    if request.method == "POST":
        ration_id=request.POST.get("ration_id")
        try:
            data,count=getLoadTransport()
            # print(rationTransport,ration_id)
            rationTransportDict=data[1][0]
            rationTransport=RationTransport.RationTransport()
            rationTransport.set_ration_transport_id(rationTransportDict["ration_transport_id"])
            rationTransport.set_load_send_date(get_current_date())
            rationTransport.set_status(RationTransport.Status.SEND.value)
            rationTransport.set_ration_id(ration_id)
            transportProductList=getTransportProduct(rationTransport.get_ration_transport_id())
            for transportProduct in transportProductList:
                product=get_product_by_id(transportProduct["product_id"])
                product["stock_quantity"]=product["stock_quantity"]-transportProduct["allocated_qty"]
                productObj=Product.Product()
                productObj.set_last_update(get_current_date())
                productObj.set_price(product["price"])
                productObj.set_product_id(product["product_id"])
                productObj.set_product_name(product["product_name"])
                productObj.set_stock_quantity(product["stock_quantity"])
                productObj.set_tolerance(product["tolerance"])
                productObj.set_unit(product["unit"])
                editProduct(productObj)
            editRationTransport(rationTransport)
            messages.success(request, "Load send successfully!")
            return get_all_product(request)
        except Exception as e:
            print(e)
            messages.error(request, "Error Loading Product")
        return get_all_product(request)
    try:
        rationList=get_all_rations()
        print(rationList)
        loads=get_loads()
        print("Loads  ",loads)
        return render(request,"product_load.html",{"mode":"view","loads":loads,"rations":rationList[0]})
    except:
        messages.error(request,"Error getting loads")
    return render(request,"product_load.html",{"mode":"view"})

def edit_load(request,ration_transport_product_id):
    if request.method == "POST":
        rationTransportProduct=RationTransportProduct.RationTransportProduct()
        rationTransportProduct.set_ration_transport_product_id(ration_transport_product_id)
        rationTransportProduct.set_product_id(request.POST.get("product_id"))
        rationTransportProduct.set_allocated_qty(request.POST.get("allocated_qty"))
        rationTransportProduct.set_ration_transport_id(request.POST.get("ration_transport_id"))
        rationTransportProduct.set_update_date(get_current_date())
        print(rationTransportProduct.__dict__)
        try:
            data,error = editRationTransportProduct(rationTransportProduct)
            messages.success(request, "Load Edit successfully!")
            return list_load(request)
        except Exception as e:
            print(e)
            try:
                messages.error(request, "Error Edit Load.Message:"+e.message)
            except:
                messages.error(request, "Error Edit Load!")
    try:
        rationTransportProduct=getRationTransportProductById(ration_transport_product_id)
        if rationTransportProduct!=None:
            return render(request,"product_load.html",{"load":rationTransportProduct,"mode":"edit"})
    except Exception as e:
        messages.error(request,"Error edit load")
    return list_load(request)
    
def delete_load(request,ration_transport_product_id):
    try:
        deleteRationTransportProduct(ration_transport_product_id)
        messages.success(request, "Load Delete successfully!")
    except Exception as e:
        messages.error(request,"Load not deleted")
    return list_load(request)


def list_ration_load(request):
    rationTransportProductList=getRationTransportProductList(request)   
    if request.method == "POST":
        try:
            isAllProductReceived=True
            for transportProduct in rationTransportProductList:
                if transportProduct["received_qty"] == None:
                    messages.warning(request,"Please enter all received quantity")
                    isAllProductReceived=False
            if isAllProductReceived == True:
                rationTransport=getRationTransport(request)
                ration=getStaffRation(request)
                addToRationInventory(rationTransportProductList,ration)
                setRationTransportReceived(rationTransport)
                print("All product receive entered ",rationTransport)
        except Exception as e:
            print(e)
            messages.error(request, "Error submit Product")
    loads=[]
    for load in rationTransportProductList:
        try:
            rationTransportProduct=getRationTransportProductById(load["ration_transport_product_id"])
            if rationTransportProduct!=None:
                loads.append(rationTransportProduct)
        except Exception as e:
            print(e)
    if len(loads)==0:
        return render(request,"ration_load.html",{"mode":"view"})    
    return render(request,"ration_load.html",{"loads":loads,"mode":"view"})

def receive_ration_load(request,ration_transport_product_id):
    if request.method == "POST":
        rationTransportProduct=RationTransportProduct.RationTransportProduct()
        rationTransportProduct.set_ration_transport_product_id(ration_transport_product_id)
        rationTransportProduct.set_product_id(request.POST.get("product_id"))
        rationTransportProduct.set_allocated_qty(request.POST.get("allocated_qty"))
        rationTransportProduct.set_ration_transport_id(request.POST.get("ration_transport_id"))
        rationTransportProduct.set_update_date(get_current_date())
        rationTransportProduct.set_received_qty(request.POST.get("received_qty"))
        try:
            data,error = editRationTransportProduct(rationTransportProduct)
            messages.success(request, "Load Edit successfully!")
            return redirect(list_ration_load)
        except Exception as e:
            print(e)
            try:
                messages.error(request, "Error Edit Load.Message:"+e.message)
            except:
                messages.error(request, "Error Edit Load!")
    try:
        rationTransportProduct=getRationTransportProductById(ration_transport_product_id)
        if rationTransportProduct!=None:
            return render(request,"ration_load.html",{"load":rationTransportProduct,"mode":"receive"})
    except Exception as e:
        messages.error(request,"Error edit load")
    return list_ration_load(request)

def getRationTransportProductList(request):
    rationTransport=getRationTransport(request)
    try:
        if rationTransport!=None:
            return getRationTransportProduct(rationTransport["ration_transport_id"])
    except Exception as e:
        print()    
    return []

def getRationTransport(request):
    try:
        ration=getStaffRation(request)
        return getRationTransportByRation(ration["ration_id"])
    except Exception as e:
        print(e)
        return redirect("staff")

def getStaffRation(request):
    return get_staff_ration(request)  

def setRationTransportReceived(rationTransport):
    rationTransportObj=RationTransport.RationTransport()
    rationTransportObj.set_ration_transport_id(rationTransport["ration_transport_id"])
    rationTransportObj.set_load_send_date(rationTransport["load_send_date"])
    rationTransportObj.set_load_received_date(get_current_date())
    rationTransportObj.set_ration_id(rationTransport["ration_id"])
    rationTransportObj.set_status(RationTransport.Status.RECEIVED.value)
    updateRationTransport(rationTransportObj)

def addToRationInventory(rationTransportProductList,ration):
    for transportProduct in rationTransportProductList:
        rationProductDict=getRationProduct(transportProduct["product_id"])
        if rationProductDict == None:
            rationProduct=getRationProductObject(ration["ration_id"],transportProduct["product_id"],transportProduct["received_qty"])
            createRationProduct(rationProduct)
        else:
            newStockQuantity=rationProductDict["stock_quantity"]+transportProduct["received_qty"]
            rationProduct=getRationProductObject(ration["ration_id"],transportProduct["product_id"],newStockQuantity)
            rationProduct.set_ration_product_id(rationProductDict["ration_product_id"])
            updateRationProduct(rationProduct)

def getRationProductObject(ration_id,product_id,received_qty):
    rationProduct=RationProduct.RationProduct()
    rationProduct.set_ration_id(ration_id)
    rationProduct.set_product_id(product_id)
    rationProduct.set_last_update(get_current_date())
    rationProduct.set_stock_quantity(received_qty)
    return rationProduct
