# from django.shortcuts import render
# from django.db.models import Count
# from django.utils import timezone
# from django.db.models.functions import TruncDate

# from app.models.Family import Family
# from app.models.StockRequest import StockRequest
# from app.views.InventoryView import get_inventory_summary

# def dashboard_view(request):
#     inventory_summary = get_inventory_summary()

#     total_families = Family.objects.count()
#     new_registrations = Family.objects.filter(
#         created_at__month=timezone.now().month,
#         created_at__year=timezone.now().year
#     ).count()

#     new_reg_data = (
#         Family.objects.annotate(date=TruncDate('created_at'))
#         .values('date')
#         .annotate(count=Count('id'))
#         .order_by('date')
#     )

#     new_reg_dates = [str(entry['date']) for entry in new_reg_data]
#     new_reg_counts = [entry['count'] for entry in new_reg_data]

#     average_distribution_per_product = (
#         inventory_summary["distribution_sum"] / inventory_summary["total_products"]
#         if inventory_summary["total_products"] > 0 else 0
#     )

#     context = {
#         "total_products": inventory_summary["total_products"],
#         "total_stock_quantity": inventory_summary["total_stock_quantity"],
#         "distribution_sum": inventory_summary["distribution_sum"],
#         "pending_stock_requests": StockRequest.objects.filter(status='pending').count(),
#         "total_families": total_families,
#         "new_registrations": new_registrations,
#         "out_of_stock_products": inventory_summary["out_of_stock_products"],
#         "average_distribution_per_product": round(average_distribution_per_product, 2),
#         "distribution_labels": inventory_summary["distribution_labels"],
#         "distribution_values": inventory_summary["distribution_values"],
#         "new_reg_dates": new_reg_dates,
#         "new_reg_counts": new_reg_counts,
#         "out_of_stock_count": inventory_summary["out_of_stock_products"],
#     }

#     return render(request, "adminDashboard.html", context)
