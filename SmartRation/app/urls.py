from django.urls import path,include
from .views import UserDetailsView,RationView
from .views import Family
from .views import InventoryView
from .views import LoadView
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

     path('product/load/add/<productId>',LoadView.add_load,name='load_product'),
     path('product/loads',LoadView.list_load,name='list_load'),
     path('product/load/edit/<ration_transport_product_id>',LoadView.edit_load,name='edit_load'),
     path('product/load/delete/<ration_transport_product_id>',LoadView.delete_load,name='delete_load'),

     path('ration/loads',LoadView.list_ration_load,name='list_ration_load'),
     path('ration/load/receive/<ration_transport_product_id>',LoadView.receive_ration_load,name='receive_ration_load'),
     
     path('staffDashboard',UserDetailsView.staff_dashboard,name='staff'),
     path('',UserDetailsView.home,name='home'),
]
