from django.db import models

# Create your models here.


# class Profile(models.Model):
#     first_name = models.CharField(max_length=20, null=True)
#     last_name = models.CharField(max_length=20, null=True)
#     profile_image = models.CharField(max_length=50, null=True)
#     email = models.CharField(max_length=20, null=True)
#     phonecode = models.CharField(max_length=20, null=True)
#     phone = models.CharField(max_length=20, null=True)
    
#     # class Meta:
# 	# 	ordering = ('-received',)
	
# 	# def __str__(self):
# 	# 	return str(self.device)
	
class ClientAdmin(models.Model):
    id = models.CharField(primary_key=True,max_length=100)
    document_name = models.CharField(max_length=20)
    profile = models.TextField()
    organisations = models.TextField()
    products = models.TextField()
    members = models.TextField()
    portfolio = models.TextField()
    security_layers = models.TextField()
    other_organisation = models.TextField()
