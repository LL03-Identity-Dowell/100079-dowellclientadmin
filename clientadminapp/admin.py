from django.contrib import admin
from .models import UserInfo,UserOrg,Urls,UserPortfolio,UserData,publiclink,Devices,OperatingSystems,Browsers,InternetConnection,LoginType,PasswordStrength,IdVerification
admin.site.register(UserInfo)
admin.site.register(UserOrg)
admin.site.register(Urls)
admin.site.register(UserPortfolio)
admin.site.register(UserData)
admin.site.register(publiclink)
admin.site.register(Devices)
admin.site.register(OperatingSystems)
admin.site.register(Browsers)
admin.site.register(InternetConnection)
admin.site.register(LoginType)
admin.site.register(PasswordStrength)
admin.site.register(IdVerification)

