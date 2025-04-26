from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from app.supabase_config import supabase
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from app.dao.RationDao import create_ration, get_all_rations, get_ration_by_id, update_ration, delete_ration,update_staff
from app.dao.UserDetailDao import get_user_by_id,get_staff
from app.models import Product
from app.dao.ProductDao import *
from app.common.Util import get_current_date
        
def add_product(request):
    if request.method == "POST":
        product=Product.Product()
        product.set_product_name(request.POST.get("product_name"))
        product.set_unit(request.POST.get("unit"))
        product.set_price(request.POST.get("price"))
        product.set_stock_quantity(request.POST.get("stock_quantity"))
        product.set_tolerance(request.POST.get("tolerance"))
        product.set_last_update(get_current_date())
        print(product)
        try:
            data,error = addProduct(product)
            messages.success(request, "Product Added successfully!")
            return redirect("list_product")
        except Exception as e:
            try:
                messages.error(request, "Error Adding Product.Message:"+e.message)
            except:
                messages.error(request, "Error Adding Product!")
    return render(request, "product_form.html")

def edit_product(request,productId):
    if request.method == "POST":
        product=Product.Product()
        product.set_product_id(productId)
        product.set_product_name(request.POST.get("product_name"))
        product.set_unit(request.POST.get("unit"))
        product.set_price(request.POST.get("price"))
        product.set_stock_quantity(request.POST.get("stock_quantity"))
        product.set_tolerance(request.POST.get("tolerance"))
        product.set_last_update(get_current_date())
        print(product.__dict__)
        try:
            data,error = editProduct(product)
            messages.success(request, "Product Edit successfully!")
            return redirect("list_product")
        except Exception as e:
            print(e)
            try:
                messages.error(request, "Error Edit Product.Message:"+e.message)
            except:
                messages.error(request, "Error Edit Product!")
    try:
        product=get_product_by_id(productId)
        print(product)
        return render(request,"product_form.html",{"product":product})
    except Exception as e:
        print(e)
        messages.error(request,"Error edit product")
        return redirect("list_product")

def delete_product(request,productId):
    print(productId)
    try:
        deleteProduct(productId)
        messages.success(request, "Product Delete successfully!")
    except Exception as e:
        print(e)
        messages.error(request,"Product not deleted")
    return redirect("list_product")

def get_all_product(request):
    try:
        products,error=get_products()
        return render(request,"inventory_list.html", {"products":products[1]})
    except Exception as e:
        try:
            messages.error(request, "Error getting Product.Message:"+e.message)
        except:
            messages.error(request, "Error Getting Product!")
    return render(request,"inventory_list.html")

