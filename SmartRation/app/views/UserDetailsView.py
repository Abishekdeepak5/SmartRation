from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import logout
from datetime import datetime, timedelta

from app.supabase_config import supabase
from app.dao import UserDetailDao, RationDao
from app.models import UserDetails

import io
import base64
import matplotlib
matplotlib.use('Agg')  # Use non-GUI backend for matplotlib
import matplotlib.pyplot as plt
import seaborn as sns

# Home page
def home(request):
    message = "Welcome"
    return render(request, 'home.html', {"message": message})

# Staff dashboard page
def staff_dashboard(request):
    return render(request, "staffDashboard.html")

# Combined Admin Dashboard view with all required stats
def admin_dashboard(request):
    today = datetime.now().date()

    # Fetch family data
    family_data = supabase.table("families").select("family_id").execute().data or []
    total_families = len(family_data)

    # Fetch product stock data
    product_data = supabase.table("product").select("product_id", "stock_quantity").execute().data or []
    distribution_labels = [f"Product {p['product_id']}" for p in product_data]
    distribution_values = [p['stock_quantity'] for p in product_data]
    total_stock_quantity = sum(distribution_values)
    out_of_stock_count = sum(1 for p in product_data if p['stock_quantity'] == 0)
    distribution_sum = total_stock_quantity
    total_products = len(product_data)
    average_distribution_per_product = round(distribution_sum / total_products, 2) if total_products > 0 else 0

    # Pending stock requests
    pending_requests = supabase.table("stock_requests").select("status").eq("status", "pending").execute().data or []
    pending_stock_requests = len(pending_requests)

    # User registrations data (assume "date_of_birth" field)
    users = supabase.table("user_details").select("date_of_birth").execute().data or []
    new_regs_by_date = {}
    new_regs = 0
    for user in users:
        try:
            reg_date = datetime.strptime(user["date_of_birth"], "%Y-%m-%d").date()
            if (today - reg_date).days <= 7:
                key = reg_date.strftime('%Y-%m-%d')
                new_regs_by_date[key] = new_regs_by_date.get(key, 0) + 1
                new_regs += 1
        except Exception:
            continue

    date_labels = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
    new_reg_counts = [new_regs_by_date.get(date, 0) for date in date_labels]

    # Generate charts using matplotlib and seaborn

    # 1. Total Stock per Product (Bar Chart)
    plt.figure(figsize=(10, 5))
    sns.barplot(x=distribution_labels, y=distribution_values, palette='Blues_d', hue=distribution_labels, legend=False)
    plt.title('Total Stock per Product')
    plt.ylabel('Stock Quantity')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png')
    plt.close()
    buf1.seek(0)
    stock_per_product_chart = base64.b64encode(buf1.read()).decode('utf-8')

    # 2. Out-of-Stock Product Breakdown (Pie Chart)
    labels = ['In Stock', 'Out of Stock']
    sizes = [total_products - out_of_stock_count, out_of_stock_count]
    colors = ['#4bc0c0', '#ff6384']
    plt.figure(figsize=(6,6))
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.title('Out-of-Stock Product Breakdown')
    plt.tight_layout()
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png')
    plt.close()
    buf2.seek(0)
    out_of_stock_chart = base64.b64encode(buf2.read()).decode('utf-8')

    # 3. Distribution vs Pending Stock Requests (Bar Chart)
    plt.figure(figsize=(6,4))
    sns.barplot(x=['Distributed', 'Pending Requests'], y=[distribution_sum, pending_stock_requests], palette='Set2', hue=['Distributed', 'Pending Requests'], legend=False)
    plt.title('Distribution vs Pending Stock Requests')
    plt.ylabel('Stock (kg)')
    plt.tight_layout()
    buf3 = io.BytesIO()
    plt.savefig(buf3, format='png')
    plt.close()
    buf3.seek(0)
    distribution_vs_pending_chart = base64.b64encode(buf3.read()).decode('utf-8')

    # 4. New Registrations Over Time (Line Chart)
    plt.figure(figsize=(10, 5))
    sns.lineplot(x=date_labels, y=new_reg_counts, marker='o')
    plt.title('New Registrations Over Time (Last 7 days)')
    plt.ylabel('New Registrations')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    buf4 = io.BytesIO()
    plt.savefig(buf4, format='png')
    plt.close()
    buf4.seek(0)
    new_registrations_chart = base64.b64encode(buf4.read()).decode('utf-8')

    return render(request, "adminDashboard.html", {
        "total_families": total_families,
        "distribution_sum": distribution_sum,
        "pending_stock_requests": pending_stock_requests,
        "new_registrations": new_regs,
        "total_products": total_products,
        "total_stock_quantity": total_stock_quantity,
        "out_of_stock_products": out_of_stock_count,
        "average_distribution_per_product": average_distribution_per_product,
        "stock_per_product_chart": stock_per_product_chart,
        "out_of_stock_chart": out_of_stock_chart,
        "distribution_vs_pending_chart": distribution_vs_pending_chart,
        "new_registrations_chart": new_registrations_chart,
    })

# User profile page
def profile(request):
    user = get_user(request)
    try:
        ration = RationDao.get_staff_ration(request)
        return render(request, "profile.html", {"user": user, "ration": ration})
    except Exception as e:
        print(e)
    return render(request, "profile.html", {"user": user})

# Register user view
def register_user(request):
    if request.method == "POST":
        userObj = UserDetails.UserDetails()
        userObj.set_user_name(request.POST["user_name"])
        userObj.set_password(make_password(request.POST["password"]))
        userObj.set_role(request.POST["role"])
        userObj.set_phone_number(request.POST["phone_number"])
        userObj.set_gender(request.POST["gender"])
        userObj.set_email(request.POST["email"])
        userObj.set_address(request.POST["address"])
        userObj.set_pincode(request.POST["pincode"])
        userObj.set_date_of_birth(request.POST["date_of_birth"])
        try:
            data, error = UserDetailDao.register_user(userObj)
            if error:
                messages.error(request, error)
                return redirect("register")
            messages.success(request, "User registered successfully!")
            return redirect("login")
        except Exception as e:
            messages.error(request, str(e))
            return redirect("register")
    return render(request, "register.html")

# Login user view
def login_user(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        try:
            data, error = UserDetailDao.get_user_by_email(email)
            user = data[1][0]
        except Exception:
            messages.error(request, "Invalid Email or Password!")
            return redirect("login")
        if not check_password(password, user["password"]):
            messages.error(request, "Invalid Email or Password!")
            return redirect("login")

        # Save user session info
        request.session["user"] = user
        request.session["user_id"] = user["user_id"]
        request.session["user_name"] = user["user_name"]
        request.session["user_role"] = user["role"]

        messages.success(request, "Login successful!")

        if user['role'] == "admin":
            return redirect("admin_dashboard")
        else:
            return redirect("staff_dashboard")

    return render(request, "login.html")

# Logout user view
def logout_user(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect("login")

# Fetch user list (JSON API)
def user_list(request):
    data, error = supabase.table("user_details").select("*").execute()
    if error:
        return JsonResponse({"error": "Failed to fetch users"})
    return JsonResponse({"users": data})

# Update user view
def update_user(request, user_id):
    if request.method == "POST":
        update_data = {
            "user_name": request.POST.get("user_name"),
            "role": request.POST.get("role"),
            "phone_number": request.POST.get("phone_number"),
            "gender": request.POST.get("gender"),
            "address": request.POST.get("address"),
            "pincode": request.POST.get("pincode"),
            "date_of_birth": request.POST.get("date_of_birth"),
        }
        data, error = supabase.table("user_details").update(update_data).eq("user_id", user_id).execute()
        if error:
            messages.error(request, "Error updating user!")
        else:
            messages.success(request, "User updated successfully!")
        return redirect("user_list")
    # For GET request, fetch user and render update form (not shown here)
    return redirect("user_list")

# Delete user view
def delete_user(request, user_id):
    data, error = supabase.table("user_details").delete().eq("user_id", user_id).execute()
    if error:
        messages.error(request, "Error deleting user!")
    else:
        messages.success(request, "User deleted successfully!")
    return redirect("user_list")

# Helper function to get logged-in user info
def get_user(request):
    user = request.session.get("user")
    return user
