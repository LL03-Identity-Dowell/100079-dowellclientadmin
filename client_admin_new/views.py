from distutils import unixccompiler
from multiprocessing.spawn import old_main_modules
from sqlite3 import connect
from unicodedata import category
from django.db import connection
from django.shortcuts import render, HttpResponse,redirect
# from .forms import AddDepartment, AddOrganisation, AddProject, RegisterClient,LoginClient,AddCompany,EditCompany
import requests
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import user_passes_test
import json
import base64
# from .decorators import authenticationrequired, is_client_admin, is_client_and_super_admin, is_super_admin, loginrequired, unauthenticated_user
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from .login import get_user_profile
# from .dowellconnection import dowellconnection 
from copy import copy
from collections import defaultdict
from client_admin import decorators
from client_admin.decorators import authenticationrequired
from client_admin.dowellconnection import dowellconnection 
from django.urls import reverse

# @authenticationrequired
# def home(request):
#     session_id = request.session.get('session_id')
#     with requests.Session() as s:
#         url = "https://100014.pythonanywhere.com/api/userinfo/"
#         r = s.post(url = url,data={"session_id":session_id})
#         r = json.loads(r.text)
#         # print (r[0])

#     username = r[0]["username"]
#     field = {}
#     session_id = request.session.get('session_id')






    
#     companies = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
#     companies = json.loads(companies)
#     # print(companies)
#     result = []
#     current_user = request.session.get('current_user')
#     c_id = []

#     field1 = {"Username": username }
#     a = dowellconnection("login","bangalore","login","registration","registration","10004545","ABCDE","fetch",field1,"nil")
#     a = json.loads(a)
#     try:
#         # if 'Admin' in current_user['role'] or 'client_admin' in  current_user['role'] :
#         #     result = companies['data']    
#         # if 'company_lead@' in current_user['role']:
#         #     print(current_user["role"])
#         #     user_company = current_user['role'].split("@",1)[1]
#         #     for company in companies['data']:
#         #         for k,v in company.items():
#         #             if user_company == v:
#         #                 result.append(company)
#         #             else:
#         #                 pass
#         for company in companies['data']:
#             for k,v in company.items():
#                 if k == 'owner' and username in v:
#                     result.append(company)
#                     c_id.append(company["_id"])
#                 else:
#                     pass    

#         # print(result)
#         username = current_user['username']
#         field1 = {"Username":username}
        
#         request.session["companies"] = result
#         a = dowellconnection("login","bangalore","login","registration","registration","10004545","ABCDE","find",field1,"nil")
#         a = json.loads(a)
#         a = a["data"]["Role"]
#         roles = a
#         # print(type(roles))
#         if type(roles) is str:
#             messages.error(request,"No data found")
#             # print(roles)

#         brands = []
#         if type(roles) is list:
#             for role in roles:
#                 brand = role.split("@")[-1]
#                 brands.append(brand)
#         field= {"owner":username,"type":"level1"}
#         print(username)
#         f = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","fetch",field,"nil")
#         print(f)
#         level1_name = "level1"
#         if f["data"]:
#             level1_name = f["data"]["name"]


#         if request.method == "POST" and "savelevel_btn" in request.POST:
#             level1_name = request.POST.get("level1_name")
#             if level1_name and len(f["data"] == 1):
#                 field_add = {"type":"level","name":level1_name, "owner":username}
#                 add = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","insert",field_add,"nil")
#                 messages.success("Successfully Added Level1")

#             else:
#                 messages.error("Problem adding level")
#                 context = {"data":r[0],"companies":result}
#                 return render(request,"client_admin_new/index.html",context)

            

#     except :
#         print("some error")
#         pass
    
#     context = {"data":r[0],"companies":result,"level1":level1_name}
#     return render(request,"client_admin_new/index.html",context)



@authenticationrequired
def home(request):
    context = {}
    session_id = request.GET.get('session_id', '')

    url = "https://100014.pythonanywhere.com/api/userinfo/"
    r = requests.post(url = url,data={"session_id":session_id})
    r = json.loads(r.text)

    # request.session["userinfo"] = r

    username = r[0]["username"]
    field = {"document_name":username}
    s = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field,"nil")
    s = json.loads(s)
    s = s["data"][0]
    print(s)
    # print(s["data"][0])
    # print(s["profile_info"])#user info
    # print(s["products"]) #products tab
    # print(s["organisations"][username].keys())
    # print(s["portpolio"]["portfolio_name"])
    organisations = s["organisations"]
    org = organisations




    level1 = organisations["level1"]
    level2 = organisations["level2"]
    level3 = organisations["level3"]
    level4 = organisations["level4"]
    level5 = organisations["level5"]

    if not "level_name" in organisations["level1"]:
        org["level1"]["level_name"] = "level1"
        field= {"document_name":username}
        update_field = {"organisations":org}
        update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,update_field)
    elif not "level_name" in organisations["level2"]:
        org["level2"]["level_name"] = "level2"
        field= {"document_name":username}
        update_field = {"organisations":org}
        update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,update_field)       
    elif not "level_name" in organisations["level3"]:
        org["level3"]["level_name"] = "level3"
        field= {"document_name":username}
        update_field = {"organisations":org}
        update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,update_field)
    elif not "level_name" in organisations["level4"]:
        org["level4"]["level_name"] = "level4"
        field= {"document_name":username}
        update_field = {"organisations":org}
        update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,update_field) 
    elif not "level_name" in organisations["level5"]:
        org["level5"]["level_name"] = "level5"
        field= {"document_name":username}
        update_field = {"organisations":org}
        update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,update_field) 
    # print(organisations[username])
    # print(org)

    # print(items)

    if request.method == "POST" and "add_item1" in request.POST:
        s = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field,"nil")
        s = json.loads(s)
        s = s["data"][0]
        organisations = s["organisations"]
        item_name = request.POST.get("item1_name")
        items= s["organisations"]["level1"]["items"]
        if item_name :
            items.append(item_name)

        organisations["level1"]["items"] = items
        field= {"document_name":username}
        field_update = {"organisations":organisations}
        try: 
            update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,field_update)
            messages.success("item successfully added")
        except:
            pass


    if request.method == "POST" and "add_item2" in request.POST:
        s = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field,"nil")
        s = json.loads(s)
        s = s["data"][0]
        organisations = s["organisations"]
        item_name = request.POST.get("item2_name")
        items= s["organisations"]["level2"]["items"]
        if item_name :
            items.append(item_name)

        organisations["level2"]["items"] = items
        field= {"document_name":username}
        field_update = {"organisations":organisations}
        try: 
            update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,field_update)
            messages.success("item successfully added")
        except:
            pass


    if request.method == "POST" and "add_item3" in request.POST:
        s = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field,"nil")
        s = json.loads(s)
        s = s["data"][0]
        organisations = s["organisations"]
        item_name = request.POST.get("item3_name")
        items= s["organisations"]["level3"]["items"]
        if item_name :
            items.append(item_name)

        organisations["level3"]["items"] = items
        field= {"document_name":username}
        field_update = {"organisations":organisations}
        try: 
            update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,field_update)
            messages.success("item successfully added")
        except:
            pass

    
    if request.method == "POST" and "add_item4" in request.POST:
        s = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field,"nil")
        s = json.loads(s)
        s = s["data"][0]
        organisations = s["organisations"]
        item_name = request.POST.get("item4_name")
        items= s["organisations"]["level4"]["items"]
        if item_name :
            items.append(item_name)

        organisations["level4"]["items"] = items
        field= {"document_name":username}
        field_update = {"organisations":organisations}
        try: 
            update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,field_update)
            messages.success("item successfully added")
        except:
            pass

    if request.method == "POST" and "add_item5" in request.POST:
        s = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field,"nil")
        s = json.loads(s)
        s = s["data"][0]
        organisations = s["organisations"]
        item_name = request.POST.get("item5_name")
        items= s["organisations"]["level5"]["items"]
        if item_name :
            items.append(item_name)

        organisations["level5"]["items"] = items
        field= {"document_name":username}
        field_update = {"organisations":organisations}
        try: 
            update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,field_update)
            messages.success("item successfully added")
        except:
            pass


    if request.method == "POST" and "savelevel1_btn" in request.POST:
        level_name = request.POST.get("level1_name")
        field = {"document_name":username}
        s = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field,"nil")
        s = json.loads(s)
        s = s["data"][0]
        organisations = s["organisations"]
        org1 = organisations
        org1["level1"]["level_name"] = level_name
        field= {"document_name":username}
        field_update = {"organisations":org1}
        try: 
            update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,field_update)
            messages.success("item successfully added")
            return redirect(request.META['HTTP_REFERER'])            
            print("successfully updated level")
        except:
            pass

    if request.method == "POST" and "savelevel2_btn" in request.POST:
        level_name = request.POST.get("level2_name")
        field = {"document_name":username}
        s = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field,"nil")
        s = json.loads(s)
        s = s["data"][0]
        organisations = s["organisations"]
        org2 = organisations
        org2["level2"]["level_name"] = level_name
        field= {"document_name":username}
        field_update = {"organisations":org2}
        try: 
            update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,field_update)
            messages.success("item successfully added")
            return HttpResponseRedirect('/')            
            print("successfully updated level")
        except:
            pass

    if request.method == "POST" and "savelevel3_btn" in request.POST:
        level_name = request.POST.get("level3_name")
        field = {"document_name":username}
        s = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field,"nil")
        s = json.loads(s)
        s = s["data"][0]
        organisations = s["organisations"]
        org3 = organisations
        org3["level3"]["level_name"] = level_name
        field= {"document_name":username}
        field_update = {"organisations":org3}
        try: 
            update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,field_update)
            messages.success("item successfully added")
            return HttpResponseRedirect('/')            
            print("successfully updated level")
        except:
            pass

    if request.method == "POST" and "savelevel4_btn" in request.POST:
        level_name = request.POST.get("level4_name")
        field = {"document_name":username}
        s = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field,"nil")
        s = json.loads(s)
        s = s["data"][0]
        organisations = s["organisations"]
        org4 = organisations
        org4["level4"]["level_name"] = level_name
        field= {"document_name":username}
        field_update = {"organisations":org4}
        try: 
            update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,field_update)
            messages.success("item successfully added")
            return HttpResponseRedirect('/')            
            print("successfully updated level")
        except:
            pass

    if request.method == "POST" and "savelevel5_btn" in request.POST:
        level_name = request.POST.get("level5_name")
        field = {"document_name":username}
        s = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field,"nil")
        s = json.loads(s)
        s = s["data"][0]
        organisations = s["organisations"]
        org5 = organisations
        org5["level5"]["level_name"] = level_name
        field= {"document_name":username}
        field_update = {"organisations":org5}
        try: 
            update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,field_update)
            messages.success("item successfully added")
            return HttpResponseRedirect('/')            
            print("successfully updated level")
        except:
            pass
        


    #list out on products tab
    context = {"profile_info":s["profile_info"],"username":username,"products":s["products"],"portfolio":s["portpolio"],"organisations":s["organisations"],"level1":level1,"level2":level2,"level3":level3,"level4":level4,"level5":level5}

    return render(request,"client_admin_new/index.html",context)
    # context["products"] = s["products"]


def form(request):

    if request.method == "POST":
        portfolio = request.POST.get("portfolio_name")
        product = request.POST.get("product_name")
        s = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field,"nil")
        s = json.loads(s)
        s = s["data"][0]
        name =s["portpolio"][portfolio]
        dict = {}
        for item in s:
            print(item)
            if(item["portfolio_name"] == portfolio):
                dict = item

            # dict["portfolio"] = item["portfolio_name"]
        
        return redirect(f'https://workflow-ai.flutterflow.app/?portfolio={dict}&session_id={request.session.get["userinfo"]}')

        #fetch portfolio name and product name


    return render(request,"client_admin_new/form.html")
