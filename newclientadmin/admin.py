from django.contrib import admin
#from .models import ProfileInfo,Organisation,Products,Members,Portfolio,SecurtiyLayers,OtherOrg,MyRoles
from django.apps import apps

all_models = apps.get_models()

for model in all_models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
