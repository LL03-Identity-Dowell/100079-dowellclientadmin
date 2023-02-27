from django.urls import path
from .views import *
urlpatterns = [
    path('',Home,name="home"),
    path("otherorg",otherorg,name="otherorg"),
    path("otherorg1",otherorg1,name="otherorg1"),
    path('portfolio',portfolio,name="portfolio"),
    path('exportfolio',portfolioUrl,name="exportfolio"),
    path('refresh',Refresh,name="refresh"),
    path('refreshother',RefreshOther,name="refreshother"),

    path('portfolioadd',PortfolioAdd,name="portfolioadd"),
    path("level_name",Levels,name="level_name"),
    path("members",Members,name="members"),
    path("item_name",Items,name="item_name"),
    path("settings",Settings,name="settings"),
    path("endis",En_dis,name="endis"),

    # path("edit_item",edititems, name="edit_item"),
    path("addroles",AddRoles,name="addroles"),
    path("invitemembers",InviteMembers,name="invitemebers"),
    path("invitelink",InviteLink,name="invitelink"),
    # path("invitesocial",invitesocial,name="invitesocial"),
    # path("addpublic",addpublic,name="addpublic"),
    path('status',StatusChange,name="status"),
    path("memberen",MemEnDis,name="memberen"),

    # path('logout',Logout,name="logout")
]
