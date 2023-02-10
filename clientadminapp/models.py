from django.db import models

class UserInfo(models.Model):
    username=models.CharField(max_length=255)
    userinfo = models.TextField()
    class Meta:
        db_table="UserInfo"
class UserOrg(models.Model):
    username=models.CharField(max_length=255)
    org = models.TextField()
    class Meta:
        db_table="UserOrg"
    def __str__(self):
        return self.username
class Urls(models.Model):
    product=models.CharField(max_length=255)
    url = models.TextField()
    class Meta:
        db_table="Urls"
class UserPortfolio(models.Model):
    username=models.CharField(max_length=255)
    portfolio = models.TextField()
    class Meta:
        db_table="UserPortfolio"
class UserData(models.Model):
    username=models.CharField(max_length=255)
    sessionid=models.CharField(max_length=255)
    alldata = models.TextField()
    class Meta:
        db_table="UserData"

class Rights(models.Model):
    username=models.CharField(max_length=255)
    membertype=models.CharField(max_length=255)
    member=models.CharField(max_length=255)
    product = models.CharField(max_length=255)
    datatype = models.CharField(max_length=255)
    operationalrights = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    portfolio_name = models.CharField(max_length=255)
    portfolio_code = models.CharField(max_length=255)
    portfolio_details = models.CharField(max_length=255)
    portfolio_u_code = models.CharField(max_length=255)
    portfolio_spec= models.CharField(max_length=255)
    class Meta:
        db_table="Rights"


class TeamMembers(models.Model):
    username=models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    member_code = models.CharField(max_length=255)
    member_details = models.CharField(max_length=255)
    member_u_code = models.CharField(max_length=255)
    member_spec = models.CharField(max_length=255)
    class Meta:
        db_table="TeamMembers"

class Guests(models.Model):
    username=models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    member_code = models.CharField(max_length=255)
    member_details = models.CharField(max_length=255)
    member_u_code = models.CharField(max_length=255)
    member_spec = models.CharField(max_length=255)
    class Meta:
        db_table="Guests"


class Roles(models.Model):
    username=models.CharField(max_length=255)
    level1 = models.CharField(max_length=255)
    level2 = models.CharField(max_length=255)
    level3 = models.CharField(max_length=255)
    level4 = models.CharField(max_length=255)
    level5 = models.CharField(max_length=255)
    security_layer = models.CharField(max_length=255)
    role_name = models.CharField(max_length=255)
    role_code = models.CharField(max_length=255)
    role_details = models.CharField(max_length=255)
    role_u_code = models.CharField(max_length=255)
    role_spec = models.CharField(max_length=255)
    class Meta:
        db_table="Roles"

class Level1Items(models.Model):
    username=models.CharField(max_length=255)
    item_name = models.CharField(max_length=255)
    item_code = models.CharField(max_length=255)
    item_details = models.CharField(max_length=255)
    item_u_code = models.CharField(max_length=255)
    item_spec = models.CharField(max_length=255)
    barcode = models.ImageField(upload_to='')
    image1 = models.ImageField(upload_to='')
    image2 = models.ImageField(upload_to='')
    class Meta:
        db_table="Level1Items"

class Level2Items(models.Model):
    username=models.CharField(max_length=255)
    item_name = models.CharField(max_length=255)
    item_code = models.CharField(max_length=255)
    item_details = models.CharField(max_length=255)
    item_u_code = models.CharField(max_length=255)
    item_spec = models.CharField(max_length=255)
    barcode = models.ImageField(upload_to='')
    image1 = models.ImageField(upload_to='')
    image2 = models.ImageField(upload_to='')
    class Meta:
        db_table="Level2Items"
class Level3Items(models.Model):
    username=models.CharField(max_length=255)
    item_name = models.CharField(max_length=255)
    item_code = models.CharField(max_length=255)
    item_details = models.CharField(max_length=255)
    item_u_code = models.CharField(max_length=255)
    item_spec = models.CharField(max_length=255)
    barcode = models.ImageField(upload_to='')
    image1 = models.ImageField(upload_to='')
    image2 = models.ImageField(upload_to='')
    class Meta:
        db_table="Level3Items"

class Level4Items(models.Model):
    username=models.CharField(max_length=255)
    item_name = models.CharField(max_length=255)
    item_code = models.CharField(max_length=255)
    item_details = models.CharField(max_length=255)
    item_u_code = models.CharField(max_length=255)
    item_spec = models.CharField(max_length=255)
    barcode = models.ImageField(upload_to='')
    image1 = models.ImageField(upload_to='')
    image2 = models.ImageField(upload_to='')
    class Meta:
        db_table="Level4Items"

class Level5Items(models.Model):
    username=models.CharField(max_length=255)
    item_name = models.CharField(max_length=255)
    item_code = models.CharField(max_length=255)
    item_details = models.CharField(max_length=255)
    item_u_code = models.CharField(max_length=255)
    item_spec = models.CharField(max_length=255)
    barcode = models.ImageField(upload_to='')
    image1 = models.ImageField(upload_to='')
    image2 = models.ImageField(upload_to='')
    class Meta:
        db_table="Level5Items"
class publiclink(models.Model):
    link=models.TextField()
    linkcode=models.CharField(max_length=255,null=True,blank=True)
    username=models.CharField(max_length=255,null=True,blank=True)
    dateof=models.CharField(max_length=255,null=True,blank=True)
    org=models.CharField(max_length=255,null=True,blank=True)
    other=models.CharField(max_length=255,null=True,blank=True)
    qrcodeid=models.CharField(max_length=255,null=True,blank=True)
    linkstatus=models.CharField(max_length=255,null=True,blank=True)
    productstatus=models.CharField(max_length=255,null=True,blank=True)
    portfolio=models.CharField(max_length=255,null=True,blank=True)
    product=models.CharField(max_length=255,null=True,blank=True)
    qrpath=models.CharField(max_length=255,null=True,blank=True)
    class Meta:
        db_table="publiclink"




class Devices(models.Model):
    username=models.CharField(max_length=255)
    data = models.TextField()
    class Meta:
        db_table="Devices"

class OperatingSystems(models.Model):
    username=models.CharField(max_length=255)
    data = models.TextField()
    class Meta:
        db_table="OperatingSystems"

class Browsers(models.Model):
    username=models.CharField(max_length=255)
    data = models.TextField()
    class Meta:
        db_table="Browsers"

class InternetConnection(models.Model):
    username=models.CharField(max_length=255)
    data = models.TextField()
    class Meta:
        db_table="InternetConnection"

class LoginType(models.Model):
    username=models.CharField(max_length=255)
    data = models.TextField()
    class Meta:
        db_table="LoginType"

class PasswordStrength(models.Model):
    username=models.CharField(max_length=255)
    data = models.TextField()
    class Meta:
        db_table="PasswordStrength"

class IdVerification(models.Model):
    username=models.CharField(max_length=255)
    data = models.TextField()
    class Meta:
        db_table="IdVerification"


class GeoLocation(models.Model):
    username=models.CharField(max_length=255)
    data = models.TextField()
    class Meta:
        db_table="GeoLocation"