from django.urls import path,include
from .views import UserDetails 
urlpatterns = [
     path('register/',UserDetails.register_user,name='register'),
     path('login/',UserDetails.login_user,name='login'),
     path('logout/',UserDetails.logout_user,name='logout'),
     path('',UserDetails.home,name='home'),
]
