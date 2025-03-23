from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from app.supabase_config import supabase
from django.contrib.auth import login, logout, authenticate
from app.models import UserDetails
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required


def home(request):
    response = supabase.table("user_details").select("*").execute()
    return render(request,'home.html')

# Register User
def register_user(request):
    if request.method == "POST":
        user_name = request.POST["user_name"]
        password = make_password(request.POST["password"])  # Hash password
        role = request.POST["role"]
        phone_number = request.POST["phone_number"]
        gender = request.POST["gender"]
        email = request.POST["email"]
        address = request.POST["address"]
        pincode = request.POST["pincode"]
        date_of_birth = request.POST["date_of_birth"]
        # Save to Supabase
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

        if error:
            messages.error(request, "Error in registration!")
        else:
            messages.success(request, "User registered successfully!")
        
        return redirect("login")

    return render(request, "register.html")

# User Login
def login_user(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]

        # Fetch user from Supabase
        data, error = supabase.table("user_details").select("*").eq("email", email).execute()
        if error==True or (not data[1]):
            messages.error(request, "Invalid Email or Password!")
            return redirect("login") 
        user = data[1][0]
        if not check_password(password, user["password"]):
            messages.error(request, "Incorrect password!")
            return redirect("login")
        # Login Django user session
        request.session["user_id"] = user["user_id"]
        request.session["user_name"] = user["user_name"]
        messages.success(request, "Login successful!")
        return redirect("home")

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
