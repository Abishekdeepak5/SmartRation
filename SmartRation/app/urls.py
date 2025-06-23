from django import views
from django.urls import path,include
from .views import UserDetailsView,RationView
from .views import Family
from .views import InventoryView
from .views import LoadView
from .views import productWeightView
from .views import WeightLoad

# from .views.dashboard import dashboard_view
urlpatterns = [
     path('register/',UserDetailsView.register_user,name='register'),
     path('login/',UserDetailsView.login_user,name='login'),
     path('profile/',UserDetailsView.profile,name='profile'),
     path('logout/',UserDetailsView.logout_user,name='logout'),
     path('adminDashboard',UserDetailsView.admin_dashboard,name='admin'),
     path('adminDashboard', UserDetailsView.admin_dashboard, name='adminDashboard'),
      path('adminDashboard/', UserDetailsView.summarize_dashboard, name='summarize_dashboard'),
     # path('summarize_dashboard/', views.summarize_dashboard, name='summarize_dashboard'),
 path("issues/", Family.get_issues_list, name="issues"),
    path("issues/generate-summary/", Family.generate_issue_summary_view, name="generate_issue_summary"),
#    path('dashboard/', dashboard_view, name='dashboard'),

     path('ration/<rationId>/family',Family.list_family,name='listfamily'),
     
     path('rations',RationView.list_rations,name='list_ration'),
     path('rations/add/',RationView.add_ration,name='add_ration'),
     path('rations/edit/<ration_id>',RationView.edit_ration,name='edit_ration'),
     path('rations/delete/<ration_id>',RationView.delete_ration_view,name='delete_ration'),
     path('rations/assign/<ration_id>',RationView.assign_staff,name='staff_assign'),
     path('ration/loads',LoadView.list_ration_load,name='list_ration_load'),
     path('ration/load/receive/<ration_transport_product_id>',LoadView.receive_ration_load,name='receive_ration_load'),
     path('ration/products',RationView.list_ration_product,name='ration_products'),
     path('ration/families',RationView.list_ration_families,name='list_ration_families'),
     path('ration/distribute',RationView.distribute_product,name='distribute_product'),
     path('ration/distribute/family/<family_id>',RationView.distribute_family_product,name='distribute_family_product'),
     path('ration/distribute/histroy',RationView.get_ration_distribute_history,name='ration_distribute_histroy'),

     path('family/add',Family.add_family,name='addfamily'),

     path('product/add',InventoryView.add_product,name='add_product'),
     path('products',InventoryView.get_all_product,name='list_product'),
     path('product/edit/<productId>',InventoryView.edit_product,name='edit_product'),
     path('product/delete/<productId>',InventoryView.delete_product,name='delete_product'),

     path('product/load/add/<productId>',LoadView.add_load,name='load_product'),
     path('product/loads',LoadView.list_load,name='list_load'),
     path('product/load/edit/<ration_transport_product_id>',LoadView.edit_load,name='edit_load'),
     path('product/load/delete/<ration_transport_product_id>',LoadView.delete_load,name='delete_load'),

     path('get_weight/', productWeightView.get_weight, name='get_weight'),
     path('display_weight/', productWeightView.display_html, name='display_weight'),
     # path('init_setup/', productWeightView.initial_setup, name='initial_setup'),
     # path('display_weight/', productWeightView.display_html1, name='display_weight'),
     # path('get_weight/', productWeightView.get_weight, name='get_weight'),
     path('weight_page/',WeightLoad.weight_page),
     path('init_setup/', WeightLoad.init_setup),
    path('read_weight/', WeightLoad.read_weight),
    path('submit_weight/', WeightLoad.submit_weight),
    path('finish/<family_id>', WeightLoad.finish),
    
     path('staffDashboard',UserDetailsView.staff_dashboard,name='staff'),
     # Family form
     path('family/form/<family_id>',Family.grievance_form,name='family_form'),
     path('family/issues',Family.get_issues_list,name='family_issues'),
     path('family/issue/<issue_id>',Family.update_issue_status,name='family_issues_update'),
     path('family/issuelogs/<issue_id>',Family.get_issues_log_list,name='family_issues_logs'),

     path('',UserDetailsView.home,name='home'),

]

     # path('ration/distribute/add/<ration_product_id>',RationView.add_distribute,name='add_distribute_product'),
     # path('ration/distribute/remove/<ration_product_id>',RationView.remove_distribute_product,name='remove_distribute_product'),