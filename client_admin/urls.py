from pkgutil import get_data
from django.urls import path,re_path
from . import views
from .views import Dowell_Login, access_denied, add_browser, add_connection, add_device, add_layers, add_location, add_os, add_process, add_rights, add_roles, add_youtube_playlist, change_password, display_browser, display_connection, display_location, display_members, display_os, display_process, display_youtube_playlist, edit_organisation, edit_user, find_brands, get_all_users,get_all_data, get_company,get_organisation,get_department,assign_roles, get_organisation_lead, get_project, get_userdata, invite, linklogin, n_brands_belong, profile, registeruser,loginuser,home,logout,index,add_user,add_organisation,main,add_company,add_department,add_project,edit_company,edit_department,edit_project,display_device,n_add_department,n_get_department,n_add_project,n_get_project,n_assign_roles,n_get_all_data
from django.contrib.auth.views import LoginView, LogoutView



urlpatterns = [
# path('register', registeruser , name='registeruser'),
path('login/', loginuser , name='loginuser'),

path('', index , name='index'),
re_path(r'^register/$', registeruser, name='registeruser'),
re_path(r'^home/$', home, name='home'),
re_path(r'^logout/$', logout, name='logout'),
re_path(r'^user/$', get_userdata, name='userdata'),
re_path(r'^index/$', index, name='index'),
re_path(r'^add_user/$', add_user, name='add_user'),
re_path(r'^add_organisation/$', add_organisation, name='add_organisation'),
re_path(r'^add_company/$', add_company, name='add_company'),
re_path(r'^edit_company/$', edit_company, name='edit_company'),
re_path(r'^edit_organisation/$', edit_organisation, name='edit_organisation'),
re_path(r'^edit_department/$', edit_department, name='edit_department'),
re_path(r'^edit_project/$', edit_project, name='edit_project'),
re_path(r'^add_department/$', n_add_department, name='n_add_department'),
re_path(r'^add_project/$', n_add_project, name='n_add_project'),
re_path(r'^users/$',get_all_users, name='get_all_users'),
re_path(r'^edit_user/$',edit_user, name='edit_user'),
re_path(r'^organisation_leads/$',get_organisation_lead, name='get_organisation_lead'),
re_path(r'^display_company/$',get_company, name='get_company'),
re_path(r'^display_organisation/$',get_organisation, name='get_organisation'),
re_path(r'^display_department/$', n_get_department, name='n_get_department'),
re_path(r'^assign_roles/$', n_assign_roles, name='n_assign_roles'),
re_path(r'^display_project/$', n_get_project, name='n_get_project'),
re_path(r'^get_data$', n_get_all_data, name='n_get_all_data'),
path('get_company/<str:id>/', find_brands, name='find_brands'),

re_path(r'^add_roles/$', add_roles, name='add_roles'),
re_path(r'^profile/$', profile, name='profile'),
re_path(r'^change_password/$', change_password, name='change_password'),
re_path(r'^add_device/$', add_device, name='add_device'),
re_path(r'^display_device/$', display_device, name='display_device'),
re_path(r'^add_location/$', add_location, name='add_location'),
re_path(r'^display_location/$', display_location, name='display_location'),
re_path(r'^add_os/$', add_os, name='add_os'),
re_path(r'^display_os/$', display_os, name='display_os'),
re_path(r'^add_connection/$', add_connection, name='add_connection'),
re_path(r'^display_connection/$', display_connection, name='display_connection'),
re_path(r'^add_browser/$', add_browser, name='add_browser'),
re_path(r'^display_browser/$', display_browser, name='display_browser'),
re_path(r'^add_process/$', add_process, name='add_process'),
re_path(r'^display_process/$', display_process, name='display_process'),
re_path(r'^add_youtube_playlist/$', add_youtube_playlist, name='add_youtube_playlist'),
re_path(r'^display_youtube_playlist/$', display_youtube_playlist, name='display_youtube_playlist'),
re_path(r'^rights/$', add_rights, name='add_rights'),
re_path(r'^add_layers/$', add_layers, name='add_layers'),
re_path(r'^access_denied/$', access_denied, name='access_denied'),
re_path(r'^invite/$', invite, name='invite'),
re_path(r'^linklogin/$', linklogin, name='linklogin'),
re_path(r'^brandmembers/$', display_members, name='display_members'),
re_path(r'^brandsbelong/$', n_brands_belong, name='n_brands_belong'),







re_path(r'^main/$', main, name='main'),


]