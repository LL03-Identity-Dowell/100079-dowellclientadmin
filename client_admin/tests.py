from django.test import TestCase
# from client_admin.dowellconnection import dowellconnection 
import json
# Create your tests here.
import json
import requests

url = 'http://100002.pythonanywhere.com/'

def dowellconnection(cluster,platform,database,collection,document,team_member_ID,function_ID,command,field,update_field):
    data= json.dumps({
      "cluster": cluster,
      "platform": platform,
      "database": database,
      "collection": collection,
      "document": document,
      "team_member_ID": team_member_ID,
      "function_ID": function_ID,
      "command": command,
      "field": field,
      "update_field":update_field
       })
    headers = {'content-type': 'application/json'}
    response = requests.request('POST',url, headers=headers,data=data)
    return response.text


username = 'Jazz3650'
field = {}
s =dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field,"nil")
print(s)
ss= json.loads(s)
p = ss["data"][0]["organisations"]
# print(p)
# organisations = [{'org_name':'Jazz3650','level1': {'items': ['python', 'mongodb', 'Django'], 'roles': [], 'level_name': 'HR Dept'}, 'level2': {'items': ['House'], 'roles': [], 'level_name': 'Technicall'}, 'level3': {'items': [], 'roles': [], 'level_name': 'Commercial'}, 'level4': {'items': [], 'roles': [], 'level_name': 'level4'}, 'level5': {'items': [], 'roles': [], 'level_name': 'level5'}}]
# p= organisations


# s = ss["data"][0]
# organisations = [s["organisations"]]
# # print(organisations)
# username = 'Jazz3650'
# field = {"document_name":username}
# update = {"organisations":organisations}
# org_dict = organisations[0]
# item_name = "abcd"
# items= org_dict["level1"]["items"]
# if item_name :
#     items.append(item_name)
# org_dict["level1"]["items"] = items
# organisations.append(org_dict)
# # print(organisations)
# field= {"document_name":username}
# field_update = {"organisations":organisations}
# print(p)
# result =dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,field_update)

# print(s)