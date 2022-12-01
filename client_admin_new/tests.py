from django.test import TestCase
from client_admin.dowellconnection import dowellconnection 
import json
# Create your tests here.

username = 'Jazz3650'
field = {"document_name":username}
s =dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field,"nil")
json.loads(s)
s = s["data"][0]
organisations = [{'org_name':'Jazz3650','level1': {'items': ['python', 'mongodb', 'Django'], 'roles': [], 'level_name': 'HR Dept'}, 'level2': {'items': ['House'], 'roles': [], 'level_name': 'Technicall'}, 'level3': {'items': [], 'roles': [], 'level_name': 'Commercial'}, 'level4': {'items': [], 'roles': [], 'level_name': 'level4'}, 'level5': {'items': [], 'roles': [], 'level_name': 'level5'}}]
s["organisations"]= organisations
username = 'Jazz3650'
field = {"document_name":username}
update = s
print(s)
# s =dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field,update)