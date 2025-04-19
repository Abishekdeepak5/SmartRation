from django.urls import path,include
from .views import UserDetailsView,RationView
from .views import Family
from .views import InventoryView
urlpatterns = [
     path('register/',UserDetailsView.register_user,name='register'),
     path('login/',UserDetailsView.login_user,name='login'),
     path('logout/',UserDetailsView.logout_user,name='logout'),
     path('adminDashboard',UserDetailsView.admin_dashboard,name='admin'),
     
     path('ration/<rationId>/family',Family.list_family,name='listfamily'),
     
     path('rations',RationView.list_rations,name='list_ration'),
     path('rations/add/',RationView.add_ration,name='add_ration'),
     path('rations/edit/<ration_id>',RationView.edit_ration,name='edit_ration'),
     path('rations/delete/<ration_id>',RationView.delete_ration_view,name='delete_ration'),
     path('rations/assign/<ration_id>',RationView.assign_staff,name='staff_assign'),

     path('family/add',Family.add_family,name='addfamily'),

     path('product/add',InventoryView.add_product,name='add_product'),
     path('products',InventoryView.get_all_product,name='list_product'),
     path('product/edit/<productId>',InventoryView.edit_product,name='edit_product'),
     path('product/delete/<productId>',InventoryView.delete_product,name='delete_product'),
     
     path('staffDashboard',UserDetailsView.staff_dashboard,name='staff'),
     path('',UserDetailsView.home,name='home'),
]
