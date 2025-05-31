from django.shortcuts import render, redirect
from django.contrib import messages
from app.models import Product
from app.dao.ProductDao import *
from app.common.Util import get_current_date

def add_product(request):
    if request.method == "POST":
        product = Product.Product()
        product.set_product_name(request.POST.get("product_name"))
        product.set_unit(request.POST.get("unit"))
        product.set_price(request.POST.get("price"))
        product.set_stock_quantity(request.POST.get("stock_quantity"))
        product.set_tolerance(request.POST.get("tolerance"))
        product.set_last_update(get_current_date())
        print(product)
        try:
            data, error = addProduct(product)
            messages.success(request, "Product Added successfully!")
            return redirect("list_product")
        except Exception as e:
            try:
                messages.error(request, "Error Adding Product. Message: " + e.message)
            except:
                messages.error(request, "Error Adding Product!")
    return render(request, "product_form.html")

def edit_product(request, productId):
    if request.method == "POST":
        product = Product.Product()
        product.set_product_id(productId)
        product.set_product_name(request.POST.get("product_name"))
        product.set_unit(request.POST.get("unit"))
        product.set_price(request.POST.get("price"))
        product.set_stock_quantity(request.POST.get("stock_quantity"))
        product.set_tolerance(request.POST.get("tolerance"))
        product.set_last_update(get_current_date())
        print(product.__dict__)
        try:
            data, error = editProduct(product)
            messages.success(request, "Product Edited successfully!")
            return redirect("list_product")
        except Exception as e:
            print(e)
            try:
                messages.error(request, "Error Editing Product. Message: " + e.message)
            except:
                messages.error(request, "Error Editing Product!")
    try:
        product = get_product_by_id(productId)
        print(product)
        return render(request, "product_form.html", {"product": product})
    except Exception as e:
        print(e)
        messages.error(request, "Error editing product")
        return redirect("list_product")

def delete_product(request, productId):
    print(productId)
    try:
        deleteProduct(productId)
        messages.success(request, "Product Deleted successfully!")
    except Exception as e:
        print(e)
        messages.error(request, "Product not deleted")
    return redirect("list_product")

def get_all_product(request):
    try:
        products, error = get_products()
        return render(request, "inventory_list.html", {"products": products[1]})
    except Exception as e:
        try:
            messages.error(request, "Error getting Product. Message: " + e.message)
        except:
            messages.error(request, "Error Getting Product!")
    return render(request, "inventory_list.html")

# Function to compute inventory summary
def get_inventory_summary():
    products, error = get_products()
    product_list = products[1] if products else []
    total_stock_quantity = sum([int(p.get_stock_quantity()) for p in product_list if p.get_stock_quantity()])
    total_products = len(product_list)
    out_of_stock_count = sum([1 for p in product_list if int(p.get_stock_quantity()) == 0])
    distribution_sum = sum([int(p.get_distributed_quantity()) if hasattr(p, 'get_distributed_quantity') else 0 for p in product_list])
    print(f"Total Products: {total_products}, Total Stock Quantity: {total_stock_quantity}, Out of Stock Count: {out_of_stock_count}, Distribution Sum: {distribution_sum}")
    print(f"Distribution Labels: {[p.get_product_name() for p in product_list]}")
    return {
        "total_products": total_products,
        "total_stock_quantity": total_stock_quantity,
        "distribution_sum": distribution_sum,
        "out_of_stock_products": out_of_stock_count,
        "distribution_labels": [p.get_product_name() for p in product_list],
        "distribution_values": [int(p.get_stock_quantity()) for p in product_list],
    }
