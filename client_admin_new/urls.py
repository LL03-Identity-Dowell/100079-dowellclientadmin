from django.urls import path,re_path
from . import views



urlpatterns = [
# path('register', registeruser , name='registeruser'),

path('', views.home, name='home'),



]