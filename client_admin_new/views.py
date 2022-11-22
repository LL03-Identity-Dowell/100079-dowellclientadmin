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


@authenticationrequired
def home(request):
    session_id = request.session.get('session_id')
    with requests.Session() as s:
        url = "https://100014.pythonanywhere.com/api/userinfo/"
        r = s.post(url = url,data={"session_id":session_id})
        r = json.loads(r.text)
        # print (r[0])

    username = r[0]["username"]
    field = {}
    session_id = request.session.get('session_id')
    companies = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
    companies = json.loads(companies)
    # print(companies)
    result = []
    current_user = request.session.get('current_user')
    c_id = []

    field1 = {"Username": username }
    a = dowellconnection("login","bangalore","login","registration","registration","10004545","ABCDE","fetch",field1,"nil")
    a = json.loads(a)
    try:
        # if 'Admin' in current_user['role'] or 'client_admin' in  current_user['role'] :
        #     result = companies['data']    
        # if 'company_lead@' in current_user['role']:
        #     print(current_user["role"])
        #     user_company = current_user['role'].split("@",1)[1]
        #     for company in companies['data']:
        #         for k,v in company.items():
        #             if user_company == v:
        #                 result.append(company)
        #             else:
        #                 pass
        for company in companies['data']:
            for k,v in company.items():
                if k == 'owner' and username in v:
                    result.append(company)
                    c_id.append(company["_id"])
                else:
                    pass    

        # print(result)
        username = current_user['username']
        field1 = {"Username":username}
        
        request.session["companies"] = result
        a = dowellconnection("login","bangalore","login","registration","registration","10004545","ABCDE","find",field1,"nil")
        a = json.loads(a)
        a = a["data"]["Role"]
        roles = a
        # print(type(roles))
        if type(roles) is str:
            messages.error(request,"No data found")
            # print(roles)

        brands = []
        if type(roles) is list:
            for role in roles:
                brand = role.split("@")[-1]
                brands.append(brand)
        field= {"owner":username}
        print(username)
        f = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","fetch",field,"nil")
        print(f)

        # if request.method == "POST" and "savelevels_btn" in request.POST:
        #     level1_name = request.POST.get("level1_name")
        #     field_add = {"name":level1_name, "owner":username}
        #     add = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","insert",field_add,"nil")

            

    except :
        print("some error")
        pass
    
    context = {"data":r[0],"companies":result}
    return render(request,"client_admin_new/index.html",context)


