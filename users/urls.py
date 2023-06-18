from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

urlpatterns = [
    path('register', RegisterUser.as_view(), name='register'),
    path('login', LoginUser.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
]
