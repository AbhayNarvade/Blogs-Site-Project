
from django.urls import path
from .views import * 
urlpatterns = [
     path('', home ,  name='home' ),
     path('auth/login/', loginuser ,  name='loginuser' ),
     path('auth/logout/', logoutuser ,  name='logoutuser' ),
     path('auth/register/', register ,  name='register' ),
     path('OTP_Verify/', OTP_Verify ,  name='OTP_Verify' ),
     path('auth/profile/', profile ,  name='profile' ),
]
