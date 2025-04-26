from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from app.supabase_config import supabase
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from app.dao.RationDao import *
from app.dao.UserDetailDao import get_user_by_id,get_staff
from app.views.LoadView import get_staff_ration

# View for listing all ration records
def list_rations(request):
    try:
        ration_dict,isSuccess= get_all_rations()
        if isSuccess == False:
            messages.error(request, "Error fetching data!")
        for curr_list in ration_dict:
            staff_id=curr_list["staff"]
            print(staff_id)
            try:
                staffDetail=get_user_by_id(staff_id)
                curr_list["staff_name"]=staffDetail["user_name"]
            except Exception as e:
                print("Ration error ",e)
        print(ration_dict)
        return render(request, "ration_list.html", {"rations": ration_dict})
    except Exception as e:
        messages.error(request, "Error fetching data!")
        return render(request, "ration_list.html", {"rations": []})
        

# View for creating a new ration entry
def add_ration(request):
    if request.method == "POST":
        staff_id = request.POST.get("staff")
        address = request.POST.get("address")
        # opening_days = request.POST.getlist("opening_days")  # Get multiple selected values
        opening_days=["monday","wednesday","friday"]
        pincode = request.POST.get("pincode")
        try:
            data,error = create_ration(staff_id, address, opening_days, pincode)
            messages.success(request, "Ration created successfully!")
            return redirect("list_ration")
        except Exception as e:
            messages.error(request, "Error creating ration!")
            return redirect("list_ration")
    return render(request, "ration_form.html")

# View for updating ration details
def edit_ration(request, ration_id):
    rationShop=None
    try:
        rationShop=get_ration_by_id(ration_id)
    except Exception as e:
        print("err ration shop",e)
    if request.method == "POST":
        staff = request.POST.get("staff")
        address = request.POST.get("address")
        # opening_days = request.POST.getlist("opening_days")
        opening_days=["monday","wednesday","friday"]
        pincode = request.POST.get("pincode")
        try:
            update_ration(ration_id, address, opening_days, pincode,staff)
            messages.success(request, "Ration updated successfully!")
            return redirect("list_ration")
        except Exception as e:
            messages.error(request, "Error updating ration!")
    return render(request, "ration_form.html", {"rationShop": rationShop})

# View for deleting a ration record
def delete_ration_view(request, ration_id):
    try:
        messages.success(request, "Ration deleted successfully!")
        delete_ration(ration_id)
    except Exception as e:
        messages.error(request, "Error deleting ration!")
    return redirect("list_ration")

def assign_staff(request,ration_id):
    try:
        if request.method=="POST":
            staff_id=request.POST["staff"]
            print(update_staff(ration_id,staff_id))
            # return redirect("admin")
        rationShop=get_ration_by_id(ration_id)
        rationStaff={}
        rationStaff["rationShop"]=rationShop
        data,error=get_staff()
        rationStaff["staffList"]=data[1]
        messages.success(request, "Staff Assigned successfully!")
        return render(request, "assign_ration.html", rationStaff)
    except Exception as e:
        print(e)
        messages.error(request, "Staff not Assign")
        return redirect("rations")
    
def list_ration_product(request):
    rationProducts=get_ration_product(request)
    return render(request,"ration_product.html",{"rationProducts":rationProducts})

def list_ration_families(request):
    ration=None
    try:
        ration=get_staff_ration(request)
    except Exception as e:
        print(e)
    rationFamilies=get_ration_families(request)
    return render(request,"ration_families.html",{"rationFamilies":rationFamilies,"ration":ration})

def distribute_product(request):
    rationProducts=get_ration_product(request)
    # request.session["rationDistributeProduct"]=None
    print(get_distribute_product(request))
    if request.method == 'POST':
        distributeProductDictionary={}
        for i in range(len(rationProducts)):
            product = rationProducts[i]
            distribute_quantity = int(request.POST.get("quantity_"+str(product["product_id"])))
            distributeProductDictionary[str(product["product_id"])]=distribute_quantity
        request.session["rationDistributeProduct"]=distributeProductDictionary
    distributeProduct=get_distribute_product(request)
    setRationDistribute(request,rationProducts,distributeProduct)
    print(rationProducts)
    return render(request,"ration_distribution.html",{"rationProducts":rationProducts,"distributeproducts":distributeProduct})

def setRationDistribute(request,rationProducts,distributeProduct):
    if distributeProduct == None:
        distributeProduct={}
        for rationProduct in rationProducts:
            distributeProduct[str(rationProduct["product_id"])] = 0
            rationProduct["distribute_quantity"] = 0
        setDistributeProduct(request,distributeProduct)
    else:
        for rationProduct in rationProducts:
            try:
                distribute_quantity = distributeProduct[str(rationProduct["product_id"])]
                if  distribute_quantity != None:
                    rationProduct["distribute_quantity"] = distribute_quantity
                else:
                    rationProduct["distribute_quantity"] = 0
            except Exception as e:
                print(e)
                rationProduct["distribute_quantity"] = 0

def setDistributeProduct(request,distributeProduct):
    request.session["rationDistributeProduct"] = distributeProduct

def distribute_family_product(request,family_id):
    # request.session["rationDistributeProduct"]=None
    distributeProduct=get_distribute_product(request)
    rationProducts=get_ration_product(request)
    if distributeProduct == None or len(distributeProduct) != len(rationProducts):
        messages.warning(request,"Please select or click update distribute products")
        return redirect("distribute_product")
    else:
        for i in range(len(rationProducts)):
            product = rationProducts[i]
            distribute_quantity = distributeProduct[str(product["product_id"])]
            product["distribute_quantity"] = distribute_quantity
        print(rationProducts)
        return render(request,"ration_family_distribute.html",{"rationProducts":rationProducts})

def get_distribute_product(request):
    return request.session.get("rationDistributeProduct")

def get_ration_product(request):
    try:
        ration=get_staff_ration(request)
        rationProducts=get_ration_products(ration["ration_id"])
        return rationProducts
    except Exception as e:
        print(e)
    return None

def get_ration_families(request):
    try:
        ration=get_staff_ration(request)
        rationFamilies=get_families(ration["ration_id"])
        print(rationFamilies)
        return rationFamilies
    except Exception as e:
        print(e)
    return None


















'''
def add_distribute(request,ration_product_id):
    ration_product_id=int(ration_product_id)
    rationDistributeProduct = get_distribute_product(request)
    if rationDistributeProduct == None:
        rationDistributeProduct=[ration_product_id]
    else:
        if ration_product_id not in rationDistributeProduct:
            rationDistributeProduct.append(ration_product_id)
    request.session["rationDistributeProduct"] = rationDistributeProduct
    print(get_distribute_product(request))
    return redirect("distribute_product")

def remove_distribute_product(request,ration_product_id):
    ration_product_id=int(ration_product_id)
    rationDistributeProduct = get_distribute_product(request)
    if rationDistributeProduct != None:
        if ration_product_id in rationDistributeProduct:
            rationDistributeProduct.remove(ration_product_id)
            request.session["rationDistributeProduct"] = rationDistributeProduct
    print(get_distribute_product(request))
    return redirect("distribute_product")
'''


