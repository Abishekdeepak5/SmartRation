from django.shortcuts import render
from app.supabase_config import supabase
from datetime import datetime, timedelta

def admin_dashboard(request):
    today = datetime.now().date()

    # 1. Product Stock Data
    product_data = supabase.table("product").select("product_id", "stock_quantity").execute().data or []
    distribution_labels = [f"Product {p['product_id']}" for p in product_data]
    distribution_values = [p['stock_quantity'] for p in product_data]
    total_stock_quantity = sum(distribution_values)
    out_of_stock_count = sum(1 for p in product_data if p['stock_quantity'] == 0)
    distribution_sum = total_stock_quantity

    # 2. Pending stock requests
    pending_requests = supabase.table("stock_requests").select("status").eq("status", "pending").execute().data or []
    pending_stock_requests = len(pending_requests)

    # 3. Total families
    family_data = supabase.table("family").select("family_id").execute().data or []
    total_families = len(family_data)

    # 4. New Registrations (last 7 days) using registration date
    users = supabase.table("user_details").select("registration_date").execute().data or []
    new_regs_by_date = {}

    for user in users:
        try:
            reg_date = datetime.strptime(user["registration_date"], "%Y-%m-%d").date()
            if (today - reg_date).days <= 7:
                key = reg_date.strftime('%Y-%m-%d')
                new_regs_by_date[key] = new_regs_by_date.get(key, 0) + 1
        except:
            continue

    date_labels = [(today - timedelta(days=i)).strftime('%Y-%m-%d') for i in range(6, -1, -1)]
    new_reg_counts = [new_regs_by_date.get(date, 0) for date in date_labels]
    new_registrations = sum(new_reg_counts)

    # 5. Total Products and Average Distribution
    total_products = len(product_data)
    average_distribution = round(distribution_sum / total_products, 2) if total_products > 0 else 0

    return render(request, "adminDashboard.html", {
        "distribution_labels": distribution_labels,
        "distribution_values": distribution_values,
        "total_stock_quantity": total_stock_quantity,
        "out_of_stock_products": out_of_stock_count,
        "distribution_sum": distribution_sum,
        "pending_stock_requests": pending_stock_requests,
        "new_reg_dates": date_labels,
        "new_reg_counts": new_reg_counts,
        "total_families": total_families,
        "new_registrations": new_registrations,
        "total_products": total_products,
        "average_distribution_per_product": average_distribution,
    })
