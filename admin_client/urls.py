from django.urls import path
from .views import *
urlpatterns = [
    path('',Home,name="home"),
    path('rights',Rights,name="rights"),
    # path('role',Role,name="role"),
    # path('level',Level,name="level"),
    # path('member',Member,name="member"),
    # path('layer',Layer,name="layer"),


]