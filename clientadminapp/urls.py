
from django.urls import path
from .views import *
urlpatterns = [
    path('',Home,name="home"),
    path('portfolio',portfolio,name="portfolio"),
    path("level_name",levels,name="level_name"),
    path("item_name",items,name="item_name"),
    path("edit_item",edititems, name="edit_item"),
    path("addroles",addroles,name="addroles"),
    path("portfolioadd",addportfolio,name="portfolioadd"),
    path("invite",invitemembers,name="invite"),
    path("invitelink",invitelink,name="invitelink"),
    path("invitesocial",invitesocial,name="invitesocial"),
    path("otherorg",otherorg,name="otherorg"),
    path("addpublic",addpublic,name="addpublic"),
    path('en_dis_port',disablep,name="en_dis_port"),
    path('logout',Logout,name="logout"),
    path('layers',Layers,name="layers")

]
