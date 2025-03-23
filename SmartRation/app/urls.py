from django.urls import path,include
from .views import UserDetailsView,RationView
urlpatterns = [
     path('register/',UserDetailsView.register_user,name='register'),
     path('login/',UserDetailsView.login_user,name='login'),
     path('logout/',UserDetailsView.logout_user,name='logout'),
     path('adminDashboard',UserDetailsView.admin_dashboard,name='admin'),
     path('rations',RationView.list_rations,name='list_ration'),
     path('rations/add/',RationView.add_ration,name='add_ration'),
     path('rations/edit/<ration_id>',RationView.edit_ration,name='edit_ration'),
     path('rations/delete/<ration_id>',RationView.delete_ration_view,name='delete_ration'),
     
     path('staffDashboard',UserDetailsView.staff_dashboard,name='staff'),
     path('',UserDetailsView.home,name='home'),
]
