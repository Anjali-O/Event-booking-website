from django.urls import path
from .views import *

urlpatterns = [
    path('login_/',login_,name='login_'),
    path('register/',register,name='register'),
    path('profile/',profile,name='profile'),
    path('logout_/',logout_,name='logout_'),
    path('reset/',reset,name='reset'),
    path('forgot/',forgot,name='forgot'),
    path('newpassword/',newpassword,name='newpassword'),
    path('login2_/<int:pk>',login2_,name='login2_')
    
]
