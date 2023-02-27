from django.urls import path
from .views import sessionView,OrgView,OrgsView,DeviceLayers,OsLayers,BrowserLayers,ConnectionLayers,LoginLayers,IdVerificationLayers,PasswordLayers,GetPort,UpdateQr
urlpatterns = [
    path('userinfo/', sessionView,name="userinfo"),
    path('members/', OrgView,name="members"),
    path('orgs/', OrgsView,name="orgs"),
    path('devicelayers/',DeviceLayers,name="devicelayers"),
    path('oslayers/',OsLayers,name="oslayers"),
    path('browserlayers/',BrowserLayers,name="browserlayers"),
    path('connectionlayers/',ConnectionLayers,name="connectionlayers"),
    path('loginlayers/',LoginLayers,name="loginlayers"),
    path('idverifiationlayers/',IdVerificationLayers,name="idverificationlayers"),
    path('passwordlayers/',PasswordLayers,name="passwordlayers"),
    path('getportfolio/',GetPort,name="getportfolio"),
    path('updateqr/',UpdateQr,name="updateqr")

]