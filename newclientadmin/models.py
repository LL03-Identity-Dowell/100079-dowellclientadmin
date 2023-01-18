from django.db import models
class ProfileInfo(models.Model):
    username=models.CharField(max_length=255)
    profile_info = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:

        db_table="ProfileInfo"
class Organisation(models.Model):
    username=models.CharField(max_length=255)
    organisation = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:

        db_table="Organisation"
class Products(models.Model):
    username=models.CharField(max_length=255)
    products = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:

        db_table="Products"
class Members(models.Model):
    username=models.CharField(max_length=255)
    members = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:

        db_table="Members"
class Portfolio(models.Model):
    username=models.CharField(max_length=255)
    portfolio = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:
        db_table="Portfolio"
class SecurtiyLayers(models.Model):
    username=models.CharField(max_length=255)
    layers = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:
        db_table="SecurityLayers"
class OtherOrg(models.Model):
    username=models.CharField(max_length=255)
    otherorg = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:
        db_table="OtherOrg"
class MyRoles(models.Model):
    username=models.CharField(max_length=255)
    roles = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    class Meta:
        db_table="MyRoles"

