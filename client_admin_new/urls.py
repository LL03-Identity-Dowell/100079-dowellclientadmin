from django.urls import path,re_path
from . import views



urlpatterns = [
# path('register', registeruser , name='registeruser'),

path('', views.home, name='newhome'),
path('form/', views.form, name='form'),
path('join/', views.linklogin_new, name='join'),
path('guest-join/', views.guestlogin, name='guest-join'),




]