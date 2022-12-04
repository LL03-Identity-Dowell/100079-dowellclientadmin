from django.urls import path,re_path
from . import views
from .views import BrowserView, CompanyView, ConnectionView, DepartmentView, DeviceView, LocationView, OrganisationView, OsView, ProcessView, ProjectView, YoutubeplaylistView,Organisations,Profile,Members




urlpatterns = [
# path('register', registeruser , name='registeruser'),

path('company/', CompanyView.as_view(), name='company'),
path('organisation/', OrganisationView.as_view(), name='organisation'),
path('department/', DepartmentView.as_view(), name='department'),
path('project/', ProjectView.as_view(), name='project'),
path('device/', DeviceView.as_view(), name='device'),
path('location/', LocationView.as_view(), name='location'),
path('os/', OsView.as_view(), name='os'),
path('connection/', ConnectionView.as_view(), name='connection'),
path('browser/', BrowserView.as_view(), name='browser'),
path('process/', ProcessView.as_view(), name='process'),
path('youtube_playlist/', YoutubeplaylistView.as_view(), name='youtube_playlist'),
path('organisations/', Organisations.as_view(), name='organisations'),
path('profile/', Profile.as_view(), name='profle'),
path('members/', Members.as_view(), name='members'),

]