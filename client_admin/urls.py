from pkgutil import get_data
from django.urls import path,re_path
from . import views
from .views import Dowell_Login, edit_organisation, get_all_users,get_all_data, get_company,get_organisation,get_department,assign_roles, get_project, get_userdata, registeruser,loginuser,home,logout,index,add_user,add_organisation,main,add_company,add_department,add_project,edit_company,edit_department,edit_project
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
re_path(r'^add_department/$', add_department, name='add_department'),
re_path(r'^add_project/$', add_project, name='add_project'),
re_path(r'^users/$',get_all_users, name='get_all_users'),
re_path(r'^display_company/$',get_company, name='get_company'),
re_path(r'^display_organisation/$',get_organisation, name='get_organisation'),
re_path(r'^display_department/$', get_department, name='get_department'),
re_path(r'^assign_roles/$', assign_roles, name='assign_roles'),
re_path(r'^display_project/$', get_project, name='get_project'),
re_path(r'^get_data$', get_all_data, name='get_all_data'),






re_path(r'^main/$', main, name='main'),


]