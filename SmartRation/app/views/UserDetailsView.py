from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from app.supabase_config import supabase
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from app.dao import UserDetailDao
from app.models import UserDetails 
from app.dao import RationDao
from app.common.email_util import send_custom_email
from django.utils.translation import gettext as _
from django.utils.translation import activate

def home(request):
    message = _("Welcome")
    response = supabase.table("user_details").select("*").execute()
    return render(request,'home.html',{"message": message})

def staff_dashboard(request):
    return render(request,"staffDashboard.html")

def admin_dashboard(request):
    return render(request,"adminDashboard.html")
def profile(request):
    user=get_user(request)
    try:
        ration=RationDao.get_staff_ration(request)
        return render(request,"profile.html",{"user":user,"ration":ration})
    except Exception as e:
        print(e)
    return render(request,"profile.html",{"user":user})

# Register User
def register_user(request):
    if request.method == "POST":
        userObj=UserDetails.UserDetails()
        userObj.set_user_name(request.POST["user_name"])
        userObj.set_password(make_password(request.POST["password"]))
        userObj.set_role(request.POST["role"])
        userObj.set_phone_number(request.POST["phone_number"])
        userObj.set_gender(request.POST["gender"])
        userObj.set_email(request.POST["email"])
        userObj.set_address(request.POST["address"])
        userObj.set_pincode(request.POST["pincode"])
        userObj.set_date_of_birth(request.POST["date_of_birth"])
        # Save to Supabase
        try:
            data,error = UserDetailDao.register_user(userObj)
            messages.success(request, "User registered successfully!")
            return redirect("login")
        except Exception as e:
            messages.error(request, e.details)
            print(e)
            print(e.details)
            return redirect("register")
    return render(request, "register.html") 

# User Login
def login_user(request):
    # send_custom_email(subject="Smart Ration",body="Hello from Django with Gmail App Password!",to_emails=["abishekdeepakff@gmail.com"])

    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        user = None
        try:
            data,error=UserDetailDao.get_user_by_email(email)
            user=data[1][0]
        except Exception as e:
            messages.error(request,"Invalid Email or Password!")
            return redirect("login")
        if not check_password(password, user["password"]):
            messages.error(request, "Invalid Email or Password!")
            return redirect("login")
        # Login Django user session
        request.session["user"] = user
        request.session["user_id"] = user["user_id"]
        request.session["user_name"] = user["user_name"]
        request.session["user_role"] = user["role"]
        messages.success(request, "Login successful!")
        print(user)
        if user['role']=="admin":
            return redirect("admin")    
        return redirect("staff")

    return render(request, "login.html")

# Logout User
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")

# Fetch User List
def user_list(request):
    data, error = supabase.table("user_details").select("*").execute()
    return JsonResponse({"users": data[1]} if not error else {"error": "Failed to fetch users"})

# Update User
def update_user(request, user_id):
    if request.method == "POST":
        user_name = request.POST["user_name"]
        role = request.POST["role"]
        phone_number = request.POST["phone_number"]
        gender = request.POST["gender"]
        address = request.POST["address"]
        pincode = request.POST["pincode"]
        date_of_birth = request.POST["date_of_birth"]

        data, error = supabase.table("user_details").update({
            "user_name": user_name,
            "role": role,
            "phone_number": phone_number,
            "gender": gender,
            "address": address,
            "pincode": pincode,
            "date_of_birth": date_of_birth
        }).eq("user_id", user_id).execute()

        if error:
            messages.error(request, "Error updating user!")
        else:
            messages.success(request, "User updated successfully!")

        return redirect("user_list")

# Delete User
def delete_user(request, user_id):
    data, error = supabase.table("user_details").delete().eq("user_id", user_id).execute()
    if error:
        messages.error(request, "Error deleting user!")
    else:
        messages.success(request, "User deleted successfully!")
    
    return redirect("user_list")


def get_user(request):
    try:
        return request.session.get("user")
    except Exception as e:
        print(e)
    return None




"""

def register_user(request):
    UserDetailDao.register_user(UserDetails.UserDetails())
    if request.method == "POST":
        userObj=UserDetails.UserDetails()
        user_name = request.POST["user_name"]
        userObj.set_user_name(user_name)
        password = make_password(request.POST["password"])  # Hash password
        userObj.set_password(password)
        role = request.POST["role"]
        userObj.set_role(role)
        phone_number = request.POST["phone_number"]
        userObj.set_phone_number(phone_number)
        gender = request.POST["gender"]
        userObj.set_gender(gender)
        email = request.POST["email"]
        userObj.set_email(email)
        address = request.POST["address"]
        userObj.set_address(address)
        pincode = request.POST["pincode"]
        userObj.set_pincode(pincode)
        date_of_birth = request.POST["date_of_birth"]
        userObj.set_date_of_birth(date_of_birth)
        UserDetailDao.register_user(userObj)
        # Save to Supabase
        try:
            data, error = supabase.table("user_details").insert({
                "user_name": user_name,
                "password": password,
                "role": role,
                "phone_number": phone_number,
                "gender": gender,
                "email": email,
                "address": address,
                "pincode": pincode,
                "date_of_birth": date_of_birth
            }).execute()
        except Exception as e:
            messages.error(request, e.details)
            return redirect("register")
        messages.success(request, "User registered successfully!")
        return redirect("login")
    return render(request, "register.html")

"""