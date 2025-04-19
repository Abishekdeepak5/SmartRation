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
