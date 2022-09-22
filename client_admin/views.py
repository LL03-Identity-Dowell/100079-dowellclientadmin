from distutils import unixccompiler
from multiprocessing.spawn import old_main_modules
from sqlite3 import connect
from unicodedata import category
from django.db import connection
from django.shortcuts import render, HttpResponse,redirect
from .forms import AddDepartment, AddOrganisation, AddProject, RegisterClient,LoginClient,AddCompany,EditCompany
import requests
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import user_passes_test
import json
import base64
from .decorators import authenticationrequired, is_client_admin, is_client_and_super_admin, is_super_admin, loginrequired, unauthenticated_user
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .login import get_user_profile
from .dowellconnection import dowellconnection 
from copy import copy
from collections import defaultdict
import re
# from rest_framework.decorators import api_view, schema



# Create your views here.

# @unauthenticated_user
def loginuser(request):

    form = LoginClient()

    context=  {'form': form}
    #posts = TestForm.objects.all()
    # data = {}

    if request.method == "POST":
        form = LoginClient(request.POST)
        username = form.data['loginusername']
        password = form.data['loginpassword']
        location = form.data['location']
        device = form.data['device']
        os = form.data['useros']
        browser = form.data['browser']
        time = form.data['usertime']
        ip = form.data['userip']
        conn = form.data['conn']
        request.session['password'] = password
        request.session['location'] = location
        request.session['device'] = device
        request.session['os'] = os
        request.session['browser'] = browser
        request.session['time'] = time
        request.session['ip'] = ip
        request.session['conn'] = conn

        p = Dowell_Login(request,username,password,location,device,os,browser,time,ip,conn)
        # print(p)
        # b = p[0]
        # decoded_data = base64.b64decode(b)
        # print (decoded_data)
        data = json.loads(p)
        # print(data)
        # b = data['jwt']
        # b+= "=" * ((4 - len(b) % 4) % 4)
        # decoded_data = base64.urlsafe_b64decode(b)
        # print (decoded_data)            
        # print(type(decoded_data))
        # print(decoded_data['id'])
        if 'username' in data:
            request.session['userdata'] = data
            username = data['username']
            request.session['username'] = username
            messages.success(request, "You Have Logged In "+username+"")
            # print(data)
            return HttpResponseRedirect('/home/') 
        messages.success(request, "Sorry Login Failed. Try Again") 
        return HttpResponseRedirect('/login/')
 


        return JsonResponse(p, safe=False)


    return render(request, 'login.html',context) 





def logout(request):
    # del request.session['jwt']

    # request.session.modified = True
    # for key in request.session.keys():
    #     del request.session[key]

    return HttpResponseRedirect('/')  



    
@loginrequired
def home(request):
    userdata = request.session.get('userdata')
    jwt_value = str( request.session.get('jwt_value'))
    # print(jwt_value)
    headers = {"Authorization" : "Token "+jwt_value+""}
    # print(headers)
    response=requests.get('https://100014.pythonanywhere.com/api/user/',headers).json()
    # print(response)
    # print(Dowell_Login("username","password","location","device","os","browser","time","ip","type_of_conn"))
    return render(request,'home.html',{'userdata':userdata,'jwt':jwt_value})
    # if jwt is None:
    #     return HttpResponseRedirect('/login/')  

def registeruser(request):
    form = RegisterClient()

    context=  {'form': form}
    response_data = {}

    if request.method == "POST":
        form = RegisterClient(request.POST)



    return render(request, 'register.html', context) 
    


def Dowell_Login(request,username,password,location,device,os,browser,time,ip,type_of_conn):
    url="https://100014.pythonanywhere.com/api/login/"
    userurl="http://100014.pythonanywhere.com/api/user/"
    usersurl="http://100014.pythonanywhere.com/api/users/"
    users = []
    payload = {
        'username': username,
        'password': password,
        'location':location,
        'device':device,
        'os':os,
        'browser':browser,
        'time':time,
        'ip':ip,
        'type_of_conn':type_of_conn
    }
    with requests.Session() as s:
        p = s.post(url, data=payload)
        r = p.text
        # jwt = json.loads(r)
        # print(jwt)
        # request.session['jwt_value'] = jwt['jwt']
  
        if "Username" in p.text:
            Dowell_Users(request,users)
            return p.text
        else:
            user = s.get(userurl)
            users = s.get(usersurl)
            users = users.text
            users = json.loads(users)
            Dowell_Users(request,users)
            return user.text


def Dowell_Users(request,users):
    # usersurl="http://100014.pythonanywhere.com/api/users/"
    user_data = users
    request.session['user_data'] = user_data
    # print(user_data)



@loginrequired
def get_userdata(request):

    userdata = request.session.get('userdata')
    # jwt_value = str( request.session.get('jwt_value'))
    # print(jwt_value)
    headers = {"HTTP_AUTHORIZATION" : "Token "+jwt_value+""}
    # print(headers)
    response=requests.get('https://100014.pythonanywhere.com/api/user/', headers=headers).json()
    # print(response)
    # print(Dowell_Login("username","password","location","device","os","browser","time","ip","type_of_conn"))
    return render(request, 'user.html', response) 



@authenticationrequired
def get_all_users(request):
    session_id = request.session.get('session_id')

    current_user = request.session.get('current_user')
    access_granted = 0
    try:
        if 'Admin' in current_user['role']:
            access_granted = 1

    
    except :
        return HttpResponse('No suitable role to access the page.')    
    # context = {'session_id':session_id,'access_granted':access_granted}         
    url = 'https://100014.pythonanywhere.com/api/listusers/'
    data={"pwd":"d0wellre$tp@$$"}

    s = requests.session()
    p = s.post(url, data=data)
    r = p.text
    r = json.loads(r)
    users = r
    context = {'session_id':session_id,'users':users,'access_granted':access_granted}         

    # print(Dowell_Login("username","password","location","device","os","browser","time","ip","type_of_conn"))
    return render(request, 'new_users.html', context) 

@authenticationrequired
def get_organisation_lead(request):
    session_id = request.session.get('session_id')

    current_user = request.session.get('current_user')
    access_granted = 0
    try:
        if 'Admin' in current_user['role']:
            access_granted = 1

    
    except :
        return HttpResponse('No suitable role to access the page.')    
    # context = {'session_id':session_id,'access_granted':access_granted}         
    url = 'https://100014.pythonanywhere.com/api/listusers/'
    data={"pwd":"d0wellre$tp@$$"}

    s = requests.session()
    p = s.post(url, data=data)
    r = p.text  
    r = json.loads(r)
    users = r
 
    context = {'session_id':session_id,'users':users,'access_granted':access_granted}         

    # print(Dowell_Login("username","password","location","device","os","browser","time","ip","type_of_conn"))
    return render(request, 'organisation_leads.html', context) 

# @loginrequired
# def index(request):
#     key = request.GET.get('session_id', '')
#     print("Key is "+ key)
#     if key == '':
#         return HttpResponseRedirect("https://100014.pythonanywhere.com/")
#     usernames = []
#     firstnames=[]
#     lastnames = []
#     emails = []
#     users=[]
#     user_data = request.session.get('user_data')
#     user_data_tup = tuple(user_data)

#     users = user_data['data']
#     users_tup = tuple(users)
#     try:
#         user = get_user_profile(key)
#         print(user)
#     except ValueError:
#         return HttpResponseRedirect("https://100014.pythonanywhere.com/")

#     for i in range(2,len(users)):
#         usernames.append(user_data['data'][i]['Username'])

#     for i in range(2,len(users)):
#         firstnames.append(user_data['data'][i]['Firstname'])

#     for i in range(2,len(users)):
#         lastnames.append(user_data['data'][i]['Lastname'])

#     for i in range(2,len(users)):
#         emails.append(user_data['data'][i]['Email'])
#     # print(user_data)

#     page = request.GET.get('page', 1)

#     paginator = Paginator(users, 10)
#     try:
#         users_tup= paginator.page(page)
#     except PageNotAnInteger:
#         users_tup = paginator.page(1)
#     except EmptyPage:   
#         users_tup = paginator.page(paginator.num_pages)


#     return render(request, 'users.html',{'user_data': user_data,'users':users, 'usernames': usernames, 'lastnames': lastnames, 'emails': emails, 'users_tup':users_tup})



# def index(request):
#     usersurl="http://100014.pythonanywhere.com/api/users/"
#     key = request.GET.get('session_id', '')
#     # print("Key is "+ key)
#     if key == '':
#         return HttpResponseRedirect("https://100014.pythonanywhere.com/")

#     try:
#         user = get_user_profile(key)
#         print(user)
#         s = requests.session()
#         users = s.get(usersurl)
#         users = users.text
#         print(users)
#         if user['role'] == 'User':
#             return HttpResponse("Your Role Does Not Have Permission To Access Admin Panel. Please Login with Authorized Credentials <a href ='https://100014.pythonanywhere.com/'> Here </a>")

#     except ValueError:
#         return HttpResponseRedirect("https://100014.pythonanywhere.com/")

#     return render(request, 'index.html',{'users':users})

@authenticationrequired
def index(request):
    session_id = request.session.get('session_id')
    current_user = request.session.get('current_user')
    username = current_user['username']
    hit0 =get_company(request)
    hit = get_organisation(request)
    hit1 = get_department(request)
    hit2 = get_project(request)
    context = {'session_id':session_id}
    company_number = request.session.get('company_number')
    organisation_number = request.session.get('organisation_number')
    department_number = request.session.get('department_number')
    project_number = request.session.get('project_number')
    context = {'session_id':session_id,'company_number':company_number,'organisation_number':organisation_number,"department_number":department_number, "project_number":project_number,"username":username}

    return render(request, 'new_base.html',context)

@authenticationrequired
def add_user(request):

    current_user = request.session.get('current_user')
    access_granted = 0
    try:
        if 'Admin' in current_user['role']:
            access_granted = 1

    
    except :
        return HttpResponse('No suitable role to access the page.')    
    registerurl = 'https://100014.pythonanywhere.com/api/register/'

    session_id = request.session.get('session_id')

    response_data = {}
    if request.method == "POST":
            username = request.POST.get('username')
            email = request.POST.get('inputEmail4')
            firstname = request.POST.get('firstname')
            lastname = request.POST.get('lastname')
            password = request.POST.get('inputPassword4')
            phonecode = request.POST.get('phonecode')
            phone = request.POST.get('phone')
            teamcode = request.POST.get('teamcode')
            s = requests.session()

            payload = {
            'username': username,
            'password': password,
            'email':email,
            'first_name':firstname,
            'last_name':lastname,
            'teamcode':teamcode,
            'phonecode':phonecode,
            'phone':phone,
                }
            p = s.post(registerurl, data=payload)
            r = p.text
            r = json.loads(r)
            # print(r)
            if len(r) > 2:
                messages.success(request, "User Has Been Successfully Added with Username : "+username+"")
            else:
                messages.error(request, "User with Username : "+username+" Already Existis")
                return HttpResponseRedirect('/add_user/?session_id='+session_id) 
    

    context=  {"session_id":session_id,'access_granted':access_granted}

    return render(request, 'add_user.html',context)


@authenticationrequired
def edit_user(request):
    u_id=int(request.GET.get('user_id',''))
    username = request.GET.get('user_username','')
    email = request.GET.get('user_email','')
    firstname = request.GET.get('user_firstname','')
    lastname = request.GET.get('user_lastname','')
    role = request.GET.get('user_role','')
    phone = request.GET.get('user_phone','')
    teamcode = request.GET.get('user_teamcode','')
    current_user = request.session.get('current_user')
    access_granted = 0
    try:
        if 'Admin' in current_user['role'] or 'client_admin' in  current_user['role'] :
            access_granted = 1

    
    except :
        return HttpResponse('No suitable role to access the page.')    
    registerurl = 'https://100014.pythonanywhere.com/api/register/'

    session_id = request.session.get('session_id')

    response_data = {}
    if request.method == "POST":
            # username = request.POST.get('username')
            email = request.POST.get('inputEmail4')
            fname = request.POST.get('firstname')
            lname = request.POST.get('lastname')
            password = request.POST.get('inputPassword4')
            phcode = request.POST.get('phonecode')
            ph = request.POST.get('phone')
            tcode = request.POST.get('teamcode')
            update_url = "https://100014.pythonanywhere.com/api/update/"+str(u_id)
            update_data={
                "email":email,
            "role": role,
            "first_name":fname,
            "last_name":lname,
            "phone":ph,
            "phonecode":phcode,
            "teamcode":tcode,

                }
            s = requests.session()
            p=s.put(update_url,data=update_data)
            r = p.text
            r = json.loads(r)
            print(r)
            if len(r) > 2:
                messages.success(request, "User Has Been Successfully updated with Username : "+username+"")
                return HttpResponseRedirect('/users/?session_id='+session_id) 

            else:
                messages.error(request, "Problem updating user : "+username+"")
                return HttpResponseRedirect('/add_user/?session_id='+session_id) 
    

    context=  {"session_id":session_id,'access_granted':access_granted,'username':username,'email':email,'firstname':firstname,'lastname':lastname,'role':role,'phone':phone,'teamcode':teamcode}

    return render(request, 'edit_user.html',context)


@authenticationrequired
def add_organisation(request):
    field = {}
    session_id = request.session.get('session_id')
    companies = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
    companies = json.loads(companies)
    result = []
    current_user = request.session.get('current_user')


    access_granted = 0
  


    result = []
    current_user = request.session.get('current_user')
    try:
        if 'Admin' in current_user['role'] or 'client_admin' in  current_user['role'] :
            result = companies['data']   
            access_granted = 1
 
        elif 'company_lead@' in current_user['role']:
            user_company = current_user['role'].split("@",1)[1]
            for comp in companies['data']:
                for k,v in comp.items():
                    if user_company == v:
                        result.append(comp)
                        access_granted = 1

                    else:
                        pass
        # else: 
        #     return HttpResponse('No suitable role to access the page.')
    
    except :
        return HttpResponse('No suitable role to access the page.')

    # context = {'session_id':session_id,'organisations':result,'access_granted':access_granted}



    # access_granted = 0

    # try:
    #     if 'Admin' in current_user['role']:   
    #         result = companies['data']    
    #         access_granted = 0

    #     else:
    #         user_company = current_user['role'].split("@",1)[1]
    #         print(user_company)
    #         for company in companies['data']:
    #             for k,v in company.items():
    #                 if user_company == v:
    #                     result.append(company)
    #                     access_granted = 0

    #                 else:
    #                     pass
    
    # except ValueError:
    #     print('No suitable role to access the page.')


    context = {'session_id':session_id,'companies':result,'access_granted':access_granted}
    # print(request.session.get('current_user'))


    if request.method == "POST":
            field= {}
            # organisation = form.data['org_name']
            organisation = request.POST.get('org_name')
            # company = form.data['companyName']
            if request.POST.get('companyName') is None:
                messages.error(request, "No Companies Assigned")
                return HttpResponseRedirect('/add_organisation/?session_id='+session_id) 

            if len(request.POST.get('org_name')) < 2:
                messages.error(request, "Please Enter 2 or More Characters ")
                return HttpResponseRedirect('/add_organisation/?session_id='+session_id) 

            company = int(request.POST.get('companyName'))
            layer = request.POST.get('layers')
            layer_dict = {"layer1":0,"layer2":0,"layer3":0,"layer4":0,"layer5":0,"layer6":0}
            # print(layer)
            if layer:
                for i in range(1,7):
                    if str(i) in layer:
                        layer_dict['layer%s' % i]  = 1
                        layer = 'layer' +str(i+1)
                        # layer+ str(i) = 1
            r = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","fetch",field,"nil")
            r = json.loads(r)
            # print(company)
            result = r['data']
            organisation_length = len(result)
            field_add = {"name": organisation,"company_id" : company,"organization_id": organisation_length}
            field_add = {**field_add, **layer_dict}
            add = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","insert",field_add,"nil")
            r1 = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","fetch",field,"nil")
            r1 = json.loads(r1)
            result1 = r1['data']
            new_company_length = len(result1)
            if new_company_length == organisation_length + 1:
                messages.success(request, "Organisation Successfully added with Organisation  Name : "+organisation)
            else:
                messages.error(request, "Problem Adding Organisation")
                return HttpResponseRedirect('/add_organisation/?session_id='+session_id) 
            
            

    return render(request, 'new_add_organisation.html',context)



@authenticationrequired
def edit_organisation(request):
    field= {}
    session_id = request.session.get('session_id')
    context = {'session_id':session_id}
    o_id=int(request.GET.get('organisation_id',''))
    c_id=request.GET.get('company_id')
    c_id = int(c_id)
    # company_placeholder = 0
    r = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","fetch",field,"nil")
    r = json.loads(r)
    result = r['data']
    r1 = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
    r1 = json.loads(r1)
    result1 = r1['data']
    company = []
    access_granted = 0
    current_user = request.session.get('current_user')
    try:
        if 'Admin' or 'client_Admin' in current_user['role']:
            company = result1 
            access_granted = 1
 
        elif 'company_lead@' in current_user['role']:
            user_company = current_user['role'].split("@",1)[1]
            for comp in r1['data']:
                for k,v in comp.items():
                    if user_company == v:
                        company.append(comp)
                        access_granted = 1

                    else:
                        pass
        elif 'company_lead@' in current_user['role']:
            access_granted = 0

        # else: 
        #     return HttpResponse('No suitable role to access the page.')
    
    except :
        return HttpResponse('No suitable role to access the page.')



    # print(result1)
    for r in result:
        if r['organization_id'] == o_id:
            organisation_placeholder = r['name']

    for r in result1:
        if r['company_id'] == c_id:
            company_placeholder = r['company']
            # print(r['company'])

    # print(company_placeholder)
    if request.method == "POST":
            field= {}
            organisation = request.POST.get('org_name')
            new_company_id = request.POST.get('companyName')
            field = {"organization_id": o_id}
            update_field={"name":organisation,"company_id": new_company_id}
            update_id = {"company_id": new_company_id}
            update1 = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","update",field,update_field)
            # update2 = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","update",field,update_id)

            return HttpResponseRedirect('/display_organisation/?session_id='+session_id)         



    context = {'session_id':session_id,"organisation_placeholder":organisation_placeholder,"company_placeholder":company_placeholder,"company_id":c_id,"company":company,'access_granted':access_granted}


    return render(request, 'new_edit_organisation.html',context)


@authenticationrequired
def edit_department(request):
    field= {}
    session_id = request.session.get('session_id')
    context = {'session_id':session_id}
    d_id=int(request.GET.get('department_id',''))
    o_id=request.GET.get('organisation_id')
    o_id = int(o_id)
    # company_placeholder = 0
    r = dowellconnection("login","bangalore","login","department","department","1085","ABCDE","fetch",field,"nil")
    r = json.loads(r)
    result = r['data']
    r1 = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","fetch",field,"nil")
    r1 = json.loads(r1)
    result1 = r1['data']
    organisation = []


    co = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
    co = json.loads(co)
    # result = organisations['data']  
    access_granted = 0

    orgs = []

    current_user = request.session.get('current_user')
    try:
        if 'Admin' in current_user['role'] or 'client_admin' in  current_user['role'] :
            organisation = result1 
            access_granted = 1
 
        elif 'organisation_lead@' in current_user['role']:
            user_org = current_user['role'].split("@",1)[1]
            for org in r1['data']:
                for k,v in org.items():
                    if user_org == v:
                        organisation.append(org)
                        access_granted = 1

                    else:
                        pass

        elif 'company_lead@' in current_user['role']:
            user_comp = current_user['role'].split("@",1)[1]
            # print(user_company)
            for comp in co['data']:
                if user_comp == comp['company']:
                    comp_id = int(comp['company_id'])

            for org in r1['data']:
                if comp_id == int(org['company_id']):
                    organisation.append(org)      
                    access_granted = 1


            # for org in orgs:
            #     for dept in r['data']:
            #         if org['organization_id'] == dept['organization_id']:
            #             result.append(dept)
        # else: 
        #     return HttpResponse('No suitable role to access the page.')
    
    except IndexError as I:
        return HttpResponse('No suitable role to access the page.')




    # print(result1)
    for r in result:
        if r['department_id'] == d_id:
            department_placeholder = r['department']

    for r in result1:
        if r['organization_id'] == o_id:
            organisation_placeholder = r['name']
            # print(r['company'])

    # print(company_placeholder)
    if request.method == "POST":
            field= {}
            department = request.POST.get('department_name')
            new_o_id = request.POST.get('orgName')
            field = {"department_id": d_id}
            update_field={"department":department,"organization_id": new_o_id}
            update = dowellconnection("login","bangalore","login","department","department","1085","ABCDE","update",field,update_field)
            return HttpResponseRedirect('/display_department/?session_id='+session_id)         
    

    context = {'session_id':session_id,"department_placeholder":department_placeholder,"organisation_placeholder":organisation_placeholder,"organisation_id":o_id,"organisation":organisation,"access_granted":access_granted}


    return render(request, 'new_edit_department.html',context)


@authenticationrequired
def edit_project(request):
    field= {}
    session_id = request.session.get('session_id')
    context = {'session_id':session_id}
    p_id=int(request.GET.get('project_id',''))
    d_id=request.GET.get('department_id')
    d_id = int(d_id)
    # company_placeholder = 0
    r = dowellconnection("login","bangalore","login","project","project","1086","ABCDE","fetch",field,"nil")
    r = json.loads(r)
    result = r['data']
    r1 = dowellconnection("login","bangalore","login","department","department","1085","ABCDE","fetch",field,"nil")
    r1 = json.loads(r1)
    result1 = r1['data']
    department = []


    orgo = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","fetch",field,"nil")
    orgo = json.loads(orgo)
    co = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
    co = json.loads(co)
    # result = departments['data']    
    orgs= []
    access_granted = 0

    current_user = request.session.get('current_user')  
    try:
        if 'Admin' in current_user['role'] or 'client_admin' in  current_user['role'] :
            department = r1['data']    
            access_granted = 1
        elif 'department_lead@' in current_user['role']:
            user_dept = current_user['role'].split("@",1)[1]
            for dept in r1['data']:
                for k,v in dept.items():
                    if user_dept == v:
                        department.append(dept)
                        access_granted = 1

                    else:
                        pass

        elif 'organisation_lead@' in current_user['role']:
            user_org = current_user['role'].split("@",1)[1]
            # print(user_company)
            for org in orgo['data']:
                if user_org == org['name']:
                    org_id = int(org['organization_id'])

            for dept in r1['data']:
                if org_id == int(dept['organization_id']):
                    department.append(dept)     
                    access_granted = 1


        elif 'company_lead@' in current_user['role']:
            user_comp = current_user['role'].split("@",1)[1]
            # print(user_company)
            for comp in co['data']:
                if user_comp == comp['company']:
                    comp_id = int(comp['company_id'])

            for org in orgo['data']:
                if comp_id == int(org['company_id']):
                    orgs.append(org)      

            for org in orgs:
                for dept in r1['data']:
                    if int(org['organization_id'] )== int(dept['organization_id']):
                        department.append(dept) 
                        access_granted = 1

        # else: 
        #     return HttpResponse('No suitable role to access the page.')
    
    except :
        return HttpResponse('No suitable role to access the page.')




    # print(result1)
    for r in result:
        if r['project_id'] == p_id:
            project_placeholder = r['project']

    for r in result1:
        if r['department_id'] == d_id:
            department_placeholder = r['department']
            # print(r['company'])

    # print(company_placeholder)
    if request.method == "POST":
            field= {}
            project = request.POST.get('project_name')
            new_d_id = request.POST.get('department_name')
            field = {"project_id": p_id}
            update_field={"project":project,"department_id": new_d_id}
            update = dowellconnection("login","bangalore","login","project","project","1086","ABCDE","update",field,update_field)
            return HttpResponseRedirect('/display_project/?session_id='+session_id)   



    context = {'session_id':session_id,"department_placeholder":department_placeholder,"project_placeholder":project_placeholder,"department_id":d_id,"department":department,"access_granted":access_granted}


    return render(request, 'new_edit_project.html',context)

@authenticationrequired
def add_company(request):
    session_id = request.session.get('session_id')

    access_granted = 0
  


    result = []
    current_user = request.session.get('current_user')
    try:
        if 'Admin' in current_user['role'] or 'client_admin' in  current_user['role'] :
            # result = organisations['data']   
            access_granted = 1
 
        # elif 'organisation_lead@' in current_user['role']:
        #     user_org = current_user['role'].split("@",1)[1]
        #     for org in organisations['data']:
        #         for k,v in org.items():
        #             if user_org == v:
        #                 result.append(org)
        #                 access_granted = 1

        #             else:
        #                 pass
        # else: 
        #     return HttpResponse('No suitable role to access the page.')
    
    except :
        return HttpResponse('No suitable role to access the page.')



    if request.method == "POST":
            field= {}
            company = request.POST.get('addCompany')
            layer = request.POST.get('layers')
            layer_dict = {"layer1":0,"layer2":0,"layer3":0,"layer4":0,"layer5":0,"layer6":0}
            # print(layer)
            if layer:
                for i in range(1,7):
                    if str(i) in layer:
                        layer_dict['layer%s' % i]  = 1
                        layer = 'layer' +str(i+1)
                        # layer+ str(i) = 1
            r = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
            r = json.loads(r)
            result = r['data']
            company_length = len(result)
            field_add = {"company": company, "company_id" : company_length+1}
            field_add = {**field_add, **layer_dict}
            add = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","insert",field_add,"nil")
            r1 = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
            r1 = json.loads(r1)
            result1 = r1['data']
            new_company_length = len(result1)
            if new_company_length == company_length + 1:
                messages.success(request, "Company Successfully added with Company  Name : "+company )
            else:
                messages.error(request, "Problem Adding Company")
                return HttpResponseRedirect('/add_company/?session_id='+session_id) 

    company_number = request.session.get('company_number')
    organisation_number = request.session.get('organisation_number')
    department_number = request.session.get('department_number')
    project_number = request.session.get('project_number')

    context = {'session_id':session_id,'access_granted':access_granted,'company_number':company_number,'organisation_number':organisation_number,"department_number":department_number, "project_number":project_number}

    return render(request, 'new_add_company.html',context)

@authenticationrequired
def edit_company(request):
    current_user = request.session.get('current_user')
    access_granted = 0
    try:
        if 'Admin' in current_user['role'] or 'client_admin' in  current_user['role'] :
            # result = organisations['data']   
            access_granted = 1
 
        # elif 'organisation_lead@' in current_user['role']:
        #     user_org = current_user['role'].split("@",1)[1]
        #     for org in organisations['data']:
        #         for k,v in org.items():
        #             if user_org == v:
        #                 result.append(org)
        #                 access_granted = 1

        #             else:
        #                 pass
        # else: 
        #     return HttpResponse('No suitable role to access the page.')
    
    except :
        return HttpResponse('No suitable role to access the page.')


    field= {}
    session_id = request.session.get('session_id')
    context = {'session_id':session_id}
    c_id=int(request.GET.get('company_id',''))
    r = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
    r = json.loads(r)
    result = r['data']
    # print(result)
    for r in result:
        if r['company_id'] == c_id:
            company_placeholder = r['company']

    # print(c_id)
    if request.method == "POST":
            field= {}
            company = request.POST.get('addCompany')
            field = {"company_id": c_id}
            update_field={"company":company}
            update = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","update",field,update_field)
            return HttpResponseRedirect('/display_company/?session_id='+session_id)         



    context = {'session_id':session_id,"company_placeholder":company_placeholder,"access_granted":access_granted}


    return render(request, 'new_edit_company.html',context)


# def add_project(request):
#     session_id = request.session.get('session_id')
#     form = AddCompany()
#     context = {'session_id':session_id,'form':form}

#     if request.method == "POST":
#             field= {}
#             form = AddCompany(request.POST)
#             company = form.data['company']
#             r = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
#             r = json.loads(r)
#             result = r['data']
#             company_length = len(result)
#             field_add = {"company": company, "company_id" : company_length+1}
#             add = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","insert",field_add,"nil")
#             r1 = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
#             r1 = json.loads(r1)
#             result1 = r1['data']
#             new_company_length = len(result1)
#             if new_company_length == company_length + 1:
#                 messages.success(request, "Company Successfully added with Company  Name : "+company+"")
#             else:
#                 messages.success(request, "Problem Adding Company")
#                 return HttpResponseRedirect('/add_company/') 


#     return render(request, 'add_company.html',context)

@authenticationrequired
def get_company(request):
    # field= {}
    # session_id = request.session.get('session_id')
    # r = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
    # r = json.loads(r)
    # company = r
    # result = r['data']
    # # print(result)
    # context = {"company":result,"session_id":session_id}


    field = {}
    session_id = request.session.get('session_id')
    companies = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
    companies = json.loads(companies)
    print(companies)
    result = []
    current_user = request.session.get('current_user')
    try:
        if 'Admin' in current_user['role'] or 'client_admin' in  current_user['role'] :
            result = companies['data']    
        elif 'company_lead@' in current_user['role']:
            user_company = current_user['role'].split("@",1)[1]
            for company in companies['data']:
                for k,v in company.items():
                    if user_company == v:
                        result.append(company)
                    else:
                        pass
    
    except :
        return HttpResponse('No suitable role to access the page.')
    
    request.session['company_number'] = len(result)
 
    context = {'session_id':session_id,'company':result}
    return render(request, 'new_display_company.html',context)

@authenticationrequired
def get_organisation(request):
    field= {}
    session_id = request.session.get('session_id')
    r = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","fetch",field,"nil")
    r1 = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
    r1 = json.loads(r1)
    r = json.loads(r)
    result = []
    result1 = []



    current_user = request.session.get('current_user')
    print(current_user['role'])
    try:
        if 'Admin' in current_user['role'] or 'client_admin' in  current_user['role'] :
            result = r['data']    
            result1 = r1['data']
            print(current_user['role'])

        elif 'organisation_lead@' in current_user['role']:
            user_org = current_user['role'].split("@",1)[1]

            roles = re.findall(r'@([^\s@]+)', current_user['role'])
            # print(user_company)
            for org in r['data']:
                if user_org == org['name']:
                    result.append(org)
                else:
                    pass
            
            for r in result:
                for c in r1['data']:
                    if int(r['company_id']) == int(c['company_id']):
                        result1.append(c)


        elif 'company_lead@' in current_user['role']:
            user_comp = current_user['role'].split("@",1)[1]
            print(user_comp)
            print(current_user['role'])

            # print(user_company)
            for comp in r1['data']:
                if user_comp == comp['company']:
                    comp_id = int(comp['company_id'])

            for org in r['data']:
                if comp_id == int(org['company_id']):
                    result.append(org)                       
            for r in result:
                for c in r1['data']:
                    if int(r['company_id']) == int(c['company_id']):
                        result1.append(c)

    
    except IndexError as I:
            return HttpResponse('Error No suitable role to access the page.')


    organisations = result
    request.session['organisation_number'] = len(result)
    companies = result1
    company_ids = []
    union =[]
    c_id =[]
    keys = []
    key = 'company_name'
    # for i in companies:
    #     for ii in organisations:
    #         if i["company_id"]==ii["company_id"]:
    #             union.append(i["company"])
    #         else:
    #             pass 

    for i in organisations:
        for ii in companies:
            if int(i["company_id"])==int(ii["company_id"]):
                union.append(ii["company"])
            else:
                pass

    for i in range(len(organisations)):
        keys.append(key)



    for i in range(len(organisations)):
        dc1 = {'company_name' : union[i]}
        organisations[i].update(dc1)        
    # print(companies)
    # d = defaultdict(dict)

    # for item in organisations + companies:
    #     d[item['company_id']].update(item)
    # list(d.values())
    # print(d)

    # organisations.extend(list(map(lambda x,y: y if x.get('company_id') != y.get('company_id') else x.update(y), organisations, companies)))
    # organisations = list(filter(None, organisations))
    # print(organisations)

    # create a list of company_ids from organisation list
    for k in range(len(organisations)):
        company_ids.append(organisations[k]['company_id'])

    #convert to integer
    for element in company_ids:
        c_id.append(int(element))

    # print(c_id)


    # for c in companies:
    #     for k in c_id:
    #         if c['company_id'] ==  c_id[k]:
    #             c_comp.append(c['company'])
        
    # print(c_comp)
    # result = []
    # for item in organisations:
    #     for item2 in companies:
    #         if item['company_id'] == item2['company_id']:
    #             new_item = copy(item)
    #             new_item['company_name'] = item2['company']
    # print(result)

    context = {"session_id":session_id, "organisations":organisations, "companies":companies,"union":union}
    # print(add)
    # context = {"company":result,"session_id":session_id}
    return render(request, 'new_display_organisation.html', context)

@authenticationrequired
def get_department(request):
    field= {}
    union =[]
    c_id =[]
    session_id = request.session.get('session_id')
    r = dowellconnection("login","bangalore","login","department","department","1085","ABCDE","fetch",field,"nil")
    r = json.loads(r)
    result = r['data']
    r1 = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","fetch",field,"nil")
    r1 = json.loads(r1)
    # result1 = r1['data']
    co = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
    co = json.loads(co)



    result = []
    result1 = []
    orgs = []


    current_user = request.session.get('current_user')
    try:
        if 'Admin' in current_user['role'] or 'client_admin' in  current_user['role'] :
            result = r['data']    
            result1 = r1['data']
        elif 'department_lead@' in current_user['role']:
            user_dept = current_user['role'].split("@",1)[1]
            # print(user_company)
            for dept in r['data']:
                if user_dept == dept['department']:
                    result.append(dept)
                else:
                    pass
            
            for r in result:
                for r1 in r1['data']:
                    if int(r['organization_id']) == int(r1['organization_id']):
                        result1.append(r1)


        elif 'organisation_lead@' in current_user['role']:
            user_org = current_user['role'].split("@",1)[1]

            roles = re.findall(r'@([^\s@]+)', current_user['role'])
            # print(user_company)
            for org in r1['data']:
                if user_org == org['name']:
                    org_id = int(org['organization_id'])
            
            for dept in r['data']:
                if org_id == int(dept['organization_id']):
                    result.append(dept)

            for r in result :
                for o in r1['data']:
                    if int(r['organization_id']) == int(o['organization_id']):
                        result1.append(o)


        elif 'company_lead@' in current_user['role']:
            user_comp = current_user['role'].split("@",1)[1]
            # print(user_company)
            for comp in co['data']:
                if user_comp == comp['company']:
                    comp_id = int(comp['company_id'])

            for org in r1['data']:
                if comp_id == int(org['company_id']):
                    orgs.append(org)      
  
            for org in orgs:
                for dept in r['data']:
                    if int(org['organization_id']) == int(dept['organization_id']):
                        result.append(dept)
            for r in result:
                for o in r1['data']:
                    if int(r['organization_id']) == int(o['organization_id']):
                        result1.append(o)


    
    except IndexError as I:
            return HttpResponse('Error No suitable role to access the page.')


    # print(result)
    departments = result
    request.session['department_number'] = len(result)
    organisations = result1
    for i in departments:
        for ii in organisations:
            if int(i["organization_id"])==int(ii["organization_id"]):
                union.append(ii["name"])
            else:
                    pass

    for i in range(len(departments)):
        dc1 = {'organisation_name' : union[i]}
        departments[i].update(dc1)

    context = {"session_id":session_id, "departments":departments, "union":union,"organisations":organisations}

    # context = {"company":result,"session_id":session_id}
    return render(request, 'new_display_department.html',context)

# @authenticationrequired
def get_project(request):
    field= {}
    union =[]
    session_id = request.session.get('session_id')
    r = dowellconnection("login","bangalore","login","project","project","1086","ABCDE","fetch",field,"nil")
    r = json.loads(r)
    result = r['data']
    r1 = dowellconnection("login","bangalore","login","department","department","1085","ABCDE","fetch",field,"nil")
    r1 = json.loads(r1)

    orgo = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","fetch",field,"nil")
    orgo = json.loads(orgo)
    co = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
    co = json.loads(co)
    # result1 = r1['data']


    depts = []
    orgs= []
    result = []
    result1 = []



    current_user = request.session.get('current_user')
    try:
        if 'Admin' in current_user['role'] or 'client_admin' in  current_user['role'] :
            result = r['data']    
            result1 = r1['data']
        elif 'project_lead@' in current_user['role']:
            user_proj = current_user['role'].split("@",1)[1]
            # print(user_company)
            for proj in r['data']:
                if user_proj == proj['project']:
                    result.append(proj)
                else:
                    pass

            for r in result:
                for r1 in r1['data']:
                    if int(r['department_id']) == int(r1['department_id']):
                        result1.append(r1)


        elif 'department_lead@' in current_user['role']:
            user_dept = current_user['role'].split("@",1)[1]

            for dept in r1['data']:
                if user_dept == dept['department']:
                    dept_id = int(dept['department_id'])
            
            for proj in r['data']:
                if dept_id == int(proj['department_id']):
                    result.append(proj)

            for r in result :
                for d in r1['data']:
                    if int(r['department_id']) == int(d['department_id']):
                        result1.append(d)


        elif 'organisation_lead@' in current_user['role']:
            user_org = current_user['role'].split("@",1)[1]
            # print(user_company)
            for org in orgo['data']:
                if user_org == org['name']:
                    org_id = int(org['organization_id'])

            for dept in r1['data']:
                if org_id == int(dept['organization_id']):
                    depts.append(dept)      
#
            for dept in depts:
                for proj in r['data']:
                    if int(dept['department_id']) == int(proj['department_id']):
                        result.append(proj)
      
            for r in result:
                for d in r1['data']:
                    if int(r['department_id']) == int(d['department_id']):
                        result1.append(d)


        elif 'company_lead@' in current_user['role']:
            user_comp = current_user['role'].split("@",1)[1]
            # print(user_company)
            for comp in co['data']:
                if user_comp == comp['company']:
                    comp_id = int(comp['company_id'])

            for org in orgo['data']:
                if comp_id == int(org['company_id']):
                    orgs.append(org)      

            for org in orgs:
                for dept in r1['data']:
                    if int(org['organization_id']) == int(dept['organization_id']):
                        depts.append(dept) 

            for dept in depts:
                for proj in r['data']:
                    if int(dept['department_id']) == int(proj['department_id']):
                        result.append(proj)     
      
            for r in result:
                for d in r1['data']:
                    if int(r['department_id']) == int(d['department_id']):
                        result1.append(d)
    
    except IndexError as I:
            return HttpResponse('Error No suitable role to access the page.')




    # print(result)
    projects = result
    request.session['project_number'] = len(result)
    departments = result1


    for i in projects:
            for ii in departments:
                if int(i["department_id"])==int(ii["department_id"]):
                    union.append(ii["department"])
                else:
                        pass

    for i in range(len(projects)):
        dc1 = {'department_name' : union[i]}
        projects[i].update(dc1)

    context = {"session_id":session_id, "projects":projects,"union":union,"departments":departments}
    # context = {"company":result,"session_id":session_id}
    return render(request, 'new_display_project.html',context)

@authenticationrequired
def add_department(request):
    field = {}
    session_id = request.session.get('session_id')
    context = {'session_id':session_id}
    organisations = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","fetch",field,"nil")
    organisations = json.loads(organisations)
    co = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
    co = json.loads(co)
    # result = organisations['data']  
    access_granted = 0
  


    result = []
    orgs = []

    current_user = request.session.get('current_user')
    try:
        if 'Admin' in current_user['role'] or 'client_admin' in  current_user['role'] :
            result = organisations['data']   
            access_granted = 1
 
        elif 'organisation_lead@' in current_user['role']:
            user_org = current_user['role'].split("@",1)[1]
            for org in organisations['data']:
                for k,v in org.items():
                    if user_org == v:
                        result.append(org)
                        access_granted = 1

                    else:
                        pass

        elif 'company_lead@' in current_user['role']:
            user_comp = current_user['role'].split("@",1)[1]
            # print(user_company)
            for comp in co['data']:
                if user_comp == comp['company']:
                    comp_id = comp['company_id']

            for org in organisations['data']:
                if comp_id == org['company_id']:
                    result.append(org)      
                    access_granted = 1


            # for org in orgs:
            #     for dept in r['data']:
            #         if org['organization_id'] == dept['organization_id']:
            #             result.append(dept)
        # else: 
        #     return HttpResponse('No suitable role to access the page.')
    
    except IndexError as I:
        return HttpResponse('No suitable role to access the page.')

    context = {'session_id':session_id,'organisations':result,'access_granted':access_granted}

    if request.method == "POST":
            field= {}
            department = request.POST.get('department_name')
            layer = request.POST.get('layers')
            layer_dict = {"layer1":0,"layer2":0,"layer3":0,"layer4":0,"layer5":0,"layer6":0}
            # print(layer)
            if layer:
                for i in range(1,7):
                    if str(i) in layer:
                        layer_dict['layer%s' % i]  = 1
                        layer = 'layer' +str(i+1)
                        # layer+ str(i) = 1

            if request.POST.get('orgName') is None:
                messages.error(request, "No Organisations Assigned")
                return HttpResponseRedirect('/add_department/?session_id='+session_id) 

            if len(request.POST.get('department_name')) < 2:
                messages.error(request, "Please Enter 2 or More Characters ")
                return HttpResponseRedirect('/add_department/?session_id='+session_id) 

            organisation = int(request.POST.get('orgName'))
            # print("Orgname is"+organisation)
            r = dowellconnection("login","bangalore","login","department","department","1085","ABCDE","fetch",field,"nil")
            r = json.loads(r)
            result = r['data']
            company_length = len(result)
            field_add = {"department": department,"organization_id":organisation , "department_id" : company_length+1}
            field_add = {**field_add, **layer_dict}
            add = dowellconnection("login","bangalore","login","department","department","1085","ABCDE","insert",field_add,"nil")
            r1 = dowellconnection("login","bangalore","login","department","department","1085","ABCDE","fetch",field,"nil")
            r1 = json.loads(r1)
            result1 = r1['data']
            new_company_length = len(result1)
            if new_company_length == company_length + 1:
                messages.success(request, "Department Successfully added with  Name : "+department )
            else:
                messages.error(request, "Problem Adding Department")
                return HttpResponseRedirect('/add_department/?session_id='+session_id) 

    return render(request, 'new_add_department.html',context)

@authenticationrequired
def add_project(request):
    field = {}
    session_id = request.session.get('session_id')
    context = {'session_id':session_id}
    departments = dowellconnection("login","bangalore","login","department","department","1085","ABCDE","fetch",field,"nil")
    departments = json.loads(departments)
    orgo = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","fetch",field,"nil")
    orgo = json.loads(orgo)
    co = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
    co = json.loads(co)
    # result = departments['data']    
    result = []
    orgs= []
    access_granted = 0

    current_user = request.session.get('current_user')  
    try:
        if 'Admin' in current_user['role'] or 'client_admin' in  current_user['role'] :
            result = departments['data']    
            access_granted = 1
        elif 'department_lead@' in current_user['role']:
            user_dept = current_user['role'].split("@",1)[1]
            for dept in departments['data']:
                for k,v in dept.items():
                    if user_dept == v:
                        result.append(dept)
                        access_granted = 1

                    else:
                        pass

        elif 'organisation_lead@' in current_user['role']:
            user_org = current_user['role'].split("@",1)[1]
            # print(user_company)
            for org in orgo['data']:
                if user_org == org['name']:
                    org_id = int(org['organization_id'])

            for dept in departments['data']:
                if org_id == int(dept['organization_id']):
                    result.append(dept)     
                    access_granted = 1


        elif 'company_lead@' in current_user['role']:
            user_comp = current_user['role'].split("@",1)[1]
            # print(user_company)
            for comp in co['data']:
                if user_comp == comp['company']:
                    comp_id = int(comp['company_id'])

            for org in orgo['data']:
                if comp_id == int(org['company_id']):
                    orgs.append(org)      

            for org in orgs:
                for dept in departments['data']:
                    if int(org['organization_id']) == int(dept['organization_id']):
                        result.append(dept) 
                        access_granted = 1

        # else: 
        #     return HttpResponse('No suitable role to access the page.')
    
    except :
        return HttpResponse('No suitable role to access the page.')


    context = {'session_id':session_id,'departments':result,'access_granted':access_granted}

    if request.method == "POST":
            field= {}
            project = request.POST.get('project_name')
            # print(project)
            department = int(request.POST.get('department_name'))
            layer = request.POST.get('layers')
            layer_dict = {"layer1":0,"layer2":0,"layer3":0,"layer4":0,"layer5":0,"layer6":0}
            # print(layer)
            if layer:
                for i in range(1,7):
                    if str(i) in layer:
                        layer_dict['layer%s' % i]  = 1
                        layer = 'layer' +str(i+1)
                        # layer+ str(i) = 1
            r = dowellconnection("login","bangalore","login","project","project","1086","ABCDE","fetch",field,"nil")
            r = json.loads(r)
            result = r['data']
            company_length = len(result)
            field_add = {"project": project,"department_id":department , "project_id" : company_length+1}
            field_add = {**field_add, **layer_dict}
            add = dowellconnection("login","bangalore","login","project","project","1086","ABCDE","insert",field_add,"nil")
            r1 = dowellconnection("login","bangalore","login","project","project","1086","ABCDE","fetch",field,"nil")
            r1 = json.loads(r1)
            result1 = r1['data']
            new_company_length = len(result1)
            if new_company_length == company_length + 1:
                messages.success(request, "Project Successfully added with  Name : "+project )
            else:
                messages.error(request, "Problem Adding Project")
                return HttpResponseRedirect('/add_project/?session_id='+session_id) 
    return render(request, 'new_add_project.html',context)


def get_all_data(request):
    session_id = request.session.get('session_id')
    field = {}
    companies = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
    companies = json.loads(companies)
    companies = companies['data']    


    organisations = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","fetch",field,"nil")
    organisations = json.loads(organisations)
    organisations = organisations['data']    

    departments = dowellconnection("login","bangalore","login","department","department","1085","ABCDE","fetch",field,"nil")
    departments = json.loads(departments)
    departments = departments['data']    


    projects = dowellconnection("login","bangalore","login","project","project","1086","ABCDE","fetch",field,"nil")
    projects = json.loads(projects)
    projects = projects['data']    

    context = {"companies": companies, "organisations":organisations, "departments":departments, "projects":projects}


    return JsonResponse(context, safe=False) 




@authenticationrequired
@is_client_and_super_admin
def assign_roles(request):
    current_user = request.session.get('current_user')
    access_granted = 0
    field ={}
    access_level = 0
    # r =dowellconnection("login","bangalore","login","roles","roles","1089","ABCDE","fetch",field,"nil")
    # print(r)
    try:
        if 'Admin' in current_user['role'] or 'client_admin' in  current_user['role'] :
            access_granted = 1
            access_level = 'Admin'
        elif 'project_lead@' in current_user['role']:
            access_granted = 1
            access_level = 'project_lead'

        elif 'department_lead@' in current_user['role']:
            access_granted = 1
            access_level = 'department_lead'


        elif 'organisation_lead@' in current_user['role']:
            access_granted = 1
            access_level = 'organisation_lead'

        elif 'company_lead@' in current_user['role']:
            access_granted = 1
            access_level = 'company_lead'

    
    except :
        return HttpResponse('No suitable role to access the page.')    

    session_id = request.session.get('session_id')
    field = {}
    field1 = {}
    url = 'https://100014.pythonanywhere.com/api/listusers/'
    data={"pwd":"d0wellre$tp@$$"}



    # field = {}
    # companies = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
    # companies = json.loads(companies)
    # companies = companies['data']    


    # organisations = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","fetch",field,"nil")
    # organisations = json.loads(organisations)
    # organisations = organisations['data']    

    # departments = dowellconnection("login","bangalore","login","department","department","1085","ABCDE","fetch",field,"nil")
    # departments = json.loads(departments)
    # departments = departments['data']    


    # projects = dowellconnection("login","bangalore","login","project","project","1086","ABCDE","fetch",field,"nil")
    # projects = json.loads(projects)
    # projects = projects['data']    

    s = requests.session()
    p = s.post(url, data=data)
    r = p.text
    r = json.loads(r)
    # f = dowellconnection("login","bangalore","login","roles","roles","1089","ABCDE","fetch",field,"nil")
    roles = dowellconnection("login","bangalore","login","roles","roles","1089","ABCDE","fetch",field,"nil")
    roles = json.loads(roles)
    roles_list = roles['data']
    designations = dowellconnection("login","bangalore","login","designation","designation","1120","ABCDE","fetch",field1,"nil")
    designations = json.loads(designations)
    designations_list = designations['data']
    print(designations_list)
    users = r


    if request.method == "POST" and 'add_roles_btn' in request.POST:
        field= {}
        role = request.POST.get('addRole')
        roles = dowellconnection("login","bangalore","login","roles","roles","1089","ABCDE","fetch",field,"nil")
        r = json.loads(roles)
        result = r['data']
        role_length = len(result) + 100
        print(role_length)
        field_add = {"id": role_length+1,"role": role }
        # add = dowellconnection("login","bangalore","login","roles","roles","1089","ABCDE","insert",field_add,"nil")
        messages.success(request, "Role Successfully Added" )
        return HttpResponseRedirect('/assign_roles/?session_id='+session_id) 

    if request.method == "POST" and 'add_designation_btn' in request.POST:
        field= {}
        designation = request.POST.get('addDesignation')
        designations = dowellconnection("login","bangalore","login","designation","designation","1120","ABCDE","fetch",field,"nil")
        r = json.loads(designations)
        result = r['data']
        designation_length = len(result) + 1000
        field_add = {"id": designation_length+1,"designation": designation }
        # add = dowellconnection("login","bangalore","login","designation","designation","1120","ABCDE","insert",field_add,"nil")
        messages.success(request, "Designation Successfully Added" )
        return HttpResponseRedirect('/assign_roles/?session_id='+session_id) 



    if request.method == "POST" and 'assign_roles_btn' in request.POST:
        role_assigned = 0
        data = request.POST.dict()
        print(data)
        selected_users = request.POST.getlist('users')
        print(selected_users)
        user_id = int(data['users'])    
        role = data['roles']
        datatype = data['data_type']
        category = data['category']
        role_String = f'{role}@{category}'
        for user in selected_users:           
            user_id = int(user)
            update_url = "https://100014.pythonanywhere.com/api/update/"+str(user_id)
            update_data={
            "role": role_String,
            "datatype": datatype
                }
            response=s.put(update_url,data=update_data)
        response= json.loads(response.text)

        for k,v in response.items():
            if v == user_id:
                role_assigned = 1

            
        if role_assigned == 1:
            messages.success(request, "Role Successfully Assigned for User : "+response["username"] )
            return HttpResponseRedirect('/assign_roles/?session_id='+session_id) 

        else:
            messages.error(request, "Problem Assigning Role" )



    context = {'access_level':access_level,'session_id':session_id,'users':users,'access_granted':access_granted,"roles_list":roles_list,"designations_list":designations_list}

    return render(request, 'assign_roles.html',context)



@authenticationrequired
@is_client_and_super_admin
def add_roles(request):
    session_id = request.session.get('session_id')

    access_granted = 0
  
    result = []
    current_user = request.session.get('current_user')
    try:
        if 'Admin' in current_user['role'] or 'client_admin' in  current_user['role'] :
            # result = organisations['data']   
            access_granted = 1
 
        # elif 'organisation_lead@' in current_user['role']:
        #     user_org = current_user['role'].split("@",1)[1]
        #     for org in organisations['data']:
        #         for k,v in org.items():
        #             if user_org == v:
        #                 result.append(org)
        #                 access_granted = 1

        #             else:
        #                 pass
        # else: 
        #     return HttpResponse('No suitable role to access the page.')
    
    except :
        return HttpResponse('No suitable role to access the page.')



    if request.method == "POST":
        field= {}
        role = request.POST.get('addRole')
        role = role.replace(" ", "_")
        print(role)
        roles = dowellconnection("login","bangalore","login","roles","roles","1089","ABCDE","fetch",field,"nil")
        r = json.loads(roles)
        result = r['data']
        role_length = len(result)
        field_add = {"id": role_length+1,"role": role }
        add = dowellconnection("login","bangalore","login","roles","roles","1089","ABCDE","insert",field_add,"nil")
        messages.success(request, "Role Successfully Added" )



    context = {'session_id':session_id,'access_granted':access_granted}

    return render(request, 'add_roles.html',context)




@authenticationrequired
def profile(request):
    session_id = request.session.get('session_id')
    current_user = request.session.get('current_user')
    url = 'https://100014.pythonanywhere.com/api/listusers/'
    data={"pwd":"d0wellre$tp@$$"}

    s = requests.session()
    p = s.post(url, data=data)
    r = p.text
    r = json.loads(r)
    users = r

    context =   {'session_id':session_id,'users':users,'current_user':current_user}

    return render(request, 'profile.html',context)




@authenticationrequired
def change_password(request):
    url="https://100014.pythonanywhere.com/api/login/"
    userurl="http://100014.pythonanywhere.com/api/user/"
    usersurl="http://100014.pythonanywhere.com/api/users/"
    users = []
    payload = {
        'username': 'Jazz3650',
        'password': 'Jazz@Fiverr@91',
            }
    with requests.Session() as s:
        p = s.post(url, data=payload)
        r = p.text
        # jwt = json.loads(r)
        # print(jwt)
        # request.session['jwt_value'] = jwt['jwt']
  
        # if "Username" in p.text:
        #     Dowell_Users(request,users)
        #     print( p.text)
        # else:
        user = s.get(userurl)
        users = s.get(usersurl)
        users = users.text
        users = json.loads(users)
        Dowell_Users(request,users)
        all_users = users['data']

    current_user = request.session.get('current_user')
  
    registerurl = 'https://100014.pythonanywhere.com/api/register/'

    session_id = request.session.get('session_id')

    if request.method == "POST":
        old_password = request.POST.get('old')
        password = request.POST.get('new')
        print(old_password)
        print(password)
        password_change = 0

        ss = requests.session()
        payload = {
         'username' : current_user['username'] ,
        'password': password,
            }
        for dict in all_users:
            if dict['Username'] == current_user['username'] and dict['Password'] == old_password:
                p = ss.post(registerurl, data=payload)
                print(p.text)
                password_change = 1
        # messages.success(request, "Problem changing password")


        print(password_change)
        if password_change == 1 :
            messages.success(request, "Password has been updated successfully")
        elif password_change == 0:
            messages.error(request, "Problem changing password")
                


    

    
    
    context=  {"session_id":session_id,'current_user': current_user}

    return render(request, 'change_password.html',context)



@authenticationrequired
def main(request):
    session_id = request.session.get('session_id')
    context = {'session_id':session_id}

    return render(request, 'main.html',context)

# @loginrequired
# def get_userdata(request):
#     jwt = request.session.get('token')
#     jwt_key = 'jwt'
#     jwt_value = jwt['jwt']
#     print(jwt_value)
#     headers = {"HTTP_AUTHORIZATION" : "Bearer "+ jwt_value +""}
#     response=requests.get('https://100014.pythonanywhere.com/api/user/',headers).json()
#     print(response)
#     return render(request,'home.html',{'response':response})


# def get_userdata_func(jwt_key,jwt_value):
#     url="https://100014.pythonanywhere.com/api/login/"
#     payload = {
#         'jwt': jwt_value,
#     }

#     with requests.Session() as s:
#         p = s.get(url, headers=payload)
#     return p


# def loginuser(request):


#     form = LoginClient()

#     context=  {'form': form}
#     #posts = TestForm.objects.all()
#     response_data = {}

#     if request.method == "POST":
#         form = LoginClient(request.POST)
#         username = form.data['loginusername']
#         password = form.data['loginpassword']
#         location = form.data['location']
#         device = form.data['device']
#         os = form.data['useros']
#         browser = form.data['browser']
#         time = form.data['usertime']
#         ip = form.data['userip']
#         conn = form.data['conn']
#         p = Dowell_Login(username,password,location,device,os,browser,time,ip,conn)
#         data = json.loads(p)
#         if 'jwt' in data:
#             return HttpResponseRedirect('/home/')
#         return HttpResponseRedirect('/login/')



#         return JsonResponse(p, safe=False)


#     return render(request, 'login.html', context) 



@authenticationrequired
@is_client_and_super_admin
def add_device(request):
    session_id = request.session.get('session_id')
    access_granted = 0
    context = {'session_id':session_id}
    result = []
    current_user = request.session.get('current_user')

    if request.method == "POST":
        field= {}
        device = request.POST.get('devicename')
        if len(device) <= 1:
            messages.error(request, "Enter more than 1 character" )
        elif len(device) > 1:
            devices = dowellconnection("login","bangalore","login","devices","devices","1106","ABCDE","fetch",field,"nil")
            r = json.loads(devices)
            result = r['data']
            device_length = len(result)
            # field_add = {"user":current_user['username'],"id": device_length+1,"device": device }
            field_add = {"id": device_length+1,"device": device }
            add = dowellconnection("login","bangalore","login","devices","devices","1106","ABCDE","insert",field_add,"nil")
            messages.success(request, "Device Successfully Added" )
            return HttpResponseRedirect('/display_device/?session_id='+session_id) 

    return render(request, 'add_device.html',context)


@authenticationrequired
@is_client_and_super_admin
def display_device(request):
    session_id = request.session.get('session_id')  
    result = []
    current_user = request.session.get('current_user')
    field= {}
    devices = dowellconnection("login","bangalore","login","devices","devices","1106","ABCDE","fetch",field,"nil")
    r = json.loads(devices)
    result = r['data']


    context = {'session_id':session_id,'devices':result,'current_user':current_user}

    return render(request, 'display_device.html',context)






@authenticationrequired
@is_client_and_super_admin
def add_location(request):
    session_id = request.session.get('session_id')  
    result = []
    current_user = request.session.get('current_user')
    context = {'session_id':session_id}

    if request.method == "POST":
        field= {}
        location = request.POST.get('locname')
        if len(location) <= 1:
            messages.error(request, "Enter more than 1 character" )
        elif len(location)> 1:
            locations = dowellconnection("login","bangalore","login","locations","locations","1107","ABCDE","fetch",field,"nil")
            r = json.loads(locations)
            result = r['data']
            location_length = len(result)
            # field_add = {"user":current_user['username'],"id": location_length+1,"location": location }
            field_add = {"id": location_length+1,"location": location }
            add = dowellconnection("login","bangalore","login","locations","locations","1107","ABCDE","insert",field_add,"nil")
            messages.success(request, "Location Successfully Added" )
            return HttpResponseRedirect('/display_location/?session_id='+session_id) 


    return render(request, 'add_location.html',context)



@authenticationrequired
@is_client_and_super_admin
def display_location(request):
    session_id = request.session.get('session_id')  
    result = []
    current_user = request.session.get('current_user')
    field= {}
    locations = dowellconnection("login","bangalore","login","locations","locations","1107","ABCDE","fetch",field,"nil")
    r = json.loads(locations)
    result = r['data']
    context = {'session_id':session_id,'locations':result,'current_user':current_user}

    return render(request, 'display_location.html',context)





@authenticationrequired
@is_client_and_super_admin
def add_os(request):
    session_id = request.session.get('session_id')  
    result = []
    current_user = request.session.get('current_user')
    context = {'session_id':session_id}

    if request.method == "POST":
        field= {}
        os = request.POST.get('osname')
        if len(os) <=1 :
            messages.error(request, "Enter more than 1 character" )
        elif len(os)>1:
            oses = dowellconnection("login","bangalore","login","os","os","1108","ABCDE","fetch",field,"nil")
            r = json.loads(oses)
            result = r['data']
            os_length = len(result)
            # field_add = {"user":current_user['username'],"id": os_length+1,"os": os }
            field_add = {"id": os_length+1,"os": os }

            add = dowellconnection("login","bangalore","login","os","os","1108","ABCDE","insert",field_add,"nil")
            messages.success(request, "OS Successfully Added" )
            return HttpResponseRedirect('/display_os/?session_id='+session_id) 

    return render(request, 'add_os.html',context)



@authenticationrequired
@is_client_and_super_admin
def display_os(request):
    session_id = request.session.get('session_id')  
    result = []
    current_user = request.session.get('current_user')
    field= {}
    oses = dowellconnection("login","bangalore","login","os","os","1108","ABCDE","fetch",field,"nil")
    r = json.loads(oses)
    result = r['data']


    context = {'session_id':session_id,'oses':result,'current_user':current_user}

    return render(request, 'display_os.html',context)



@authenticationrequired
@is_client_and_super_admin
def add_connection(request):
    session_id = request.session.get('session_id')  
    result = []
    current_user = request.session.get('current_user')
    context = {'session_id':session_id}

    if request.method == "POST":
        field= {}
        connection = request.POST.get('connection_name')
        if len(connection) <=1 :
            messages.error(request, "Enter more than 1 character" )
        elif len(connection) >1:
            connections = dowellconnection("login","bangalore","login","connections","connections","1110","ABCDE","fetch",field,"nil")
            r = json.loads(connections)
            result = r['data']
            connection_length = len(result)
            # field_add = {"user":current_user['username'],"id": connection_length+1,"connection": connection}
            field_add = {"id": connection_length+1,"connection": connection}

            add = dowellconnection("login","bangalore","login","connections","connections","1110","ABCDE","insert",field_add,"nil")
            messages.success(request, "Connection Successfully Added" )
            return HttpResponseRedirect('/display_connection/?session_id='+session_id) 

    return render(request, 'add_connection.html',context)



@authenticationrequired
@is_client_and_super_admin
def display_connection(request):
    session_id = request.session.get('session_id')  
    result = []
    current_user = request.session.get('current_user')
    field= {}
    connections = dowellconnection("login","bangalore","login","connections","connections","1110","ABCDE","fetch",field,"nil")
    r = json.loads(connections)
    result = r['data']


    context = {'session_id':session_id,'connections':result,'current_user':current_user}

    return render(request, 'display_connection.html',context)




@authenticationrequired
@is_client_and_super_admin
def add_browser(request):
    session_id = request.session.get('session_id')  
    result = []
    current_user = request.session.get('current_user')
    context = {'session_id':session_id}

    if request.method == "POST":
        field= {}
        browser = request.POST.get('browsername')
        if len(browser) <=1:
            messages.error(request, "Enter more than 1 character" )
        elif len(browser) > 1 :         
            browsers = dowellconnection("login","bangalore","login","browsers","browsers","1109","ABCDE","fetch",field,"nil")
            r = json.loads(browsers)
            result = r['data']
            browser_length = len(result)
            # field_add = {"user":current_user['username'],"id": browser_length+1,"browser": browser}
            field_add = {"id": browser_length+1,"browser": browser}

            add = dowellconnection("login","bangalore","login","browsers","browsers","1109","ABCDE","insert",field_add,"nil")
            messages.success(request, "Browser Successfully Added" )
            return HttpResponseRedirect('/display_browser/?session_id='+session_id) 

    return render(request, 'add_browser.html',context)


@authenticationrequired
@is_client_and_super_admin
def display_browser(request):
    session_id = request.session.get('session_id')  
    result = []
    current_user = request.session.get('current_user')
    field= {}
    browsers = dowellconnection("login","bangalore","login","browsers","browsers","1109","ABCDE","fetch",field,"nil")
    r = json.loads(browsers)
    result = r['data']


    context = {'session_id':session_id,'browsers':result,'current_user':current_user}

    return render(request, 'display_browser.html',context)






@authenticationrequired
@is_client_and_super_admin
def add_process(request):
    session_id = request.session.get('session_id')  
    result = []
    current_user = request.session.get('current_user')
    context = {'session_id':session_id}

    if request.method == "POST":
        field= {}
        process = request.POST.get('processname')
        if len(process) <= 1 :
            messages.error(request, "Enter more than 1 character" )
        elif len(process) >1 : 
            processes = dowellconnection("login","bangalore","login","processes","processes","1111","ABCDE","fetch",field,"nil")
            r = json.loads(processes)
            result = r['data']
            process_length = len(result)
            # field_add = {"user":current_user['username'],"id": process_length+1,"process": process}
            field_add = {"id": process_length+1,"process": process}

            add = dowellconnection("login","bangalore","login","processes","processes","1111","ABCDE","insert",field_add,"nil")
            messages.success(request, "Process Successfully Added" )
            return HttpResponseRedirect('/display_process/?session_id='+session_id) 




    return render(request, 'add_process.html',context)


  

@authenticationrequired
@is_client_and_super_admin
def display_process(request):
    session_id = request.session.get('session_id')  
    result = []
    current_user = request.session.get('current_user')
    field= {}
    processes = dowellconnection("login","bangalore","login","processes","processes","1111","ABCDE","fetch",field,"nil")
    r = json.loads(processes)
    result = r['data']
    context = {'session_id':session_id,'processes':result,'current_user':current_user}

    return render(request, 'display_process.html',context)



@authenticationrequired
@is_client_and_super_admin
def add_youtube_playlist(request):
    current_user = request.session.get('current_user')
    session_id = request.session.get('session_id')  
    result = []
    context = {'session_id':session_id}


    if request.method == "POST":
        field= {}
        playlist = request.POST.get('playlistname')
        if len(playlist) <=1:
             messages.error(request, "Enter more than 1 character" )
        elif len(playlist) > 1:           
            playlists = dowellconnection("login","bangalore","login","youtube_playlist","youtube_playlist","1112","ABCDE","fetch",field,"nil")
            r = json.loads(playlists)
            result = r['data']
            list_length = len(result)
            # field_add = {"user":current_user['username'],"id": list_length+1,"playlist": playlist}
            field_add = {"id": list_length+1,"playlist": playlist}
            add = dowellconnection("login","bangalore","login","youtube_playlist","youtube_playlist","1112","ABCDE","insert",field_add,"nil")
            messages.success(request, "Playlist Successfully Added" )
            return HttpResponseRedirect('/display_youtube_playlist/?session_id='+session_id) 




    return render(request, 'add_youtube_playlist.html',context)



@authenticationrequired
@is_client_and_super_admin
def display_youtube_playlist(request):
    session_id = request.session.get('session_id')  
    result = []
    current_user = request.session.get('current_user')
    field= {}
    playlists = dowellconnection("login","bangalore","login","youtube_playlist","youtube_playlist","1112","ABCDE","fetch",field,"nil")
    r = json.loads(playlists)
    result = r['data']


    context = {'session_id':session_id,'playlists':result,'current_user':current_user}

    return render(request, 'display_youtube_playlist.html',context)




@authenticationrequired
@is_client_and_super_admin
def add_rights(request):
    session_id = request.session.get('session_id')  
    result = []
    current_user = request.session.get('current_user')
    field = {}
    url = 'https://100014.pythonanywhere.com/api/listusers/'
    data={"pwd":"d0wellre$tp@$$"}
    s = requests.session()
    p = s.post(url, data=data)
    r = p.text
    r = json.loads(r)
    users = r
    devices = dowellconnection("login","bangalore","login","devices","devices","1106","ABCDE","fetch",field,"nil")
    devices = json.loads(devices)
    devices = devices['data']
    locations = dowellconnection("login","bangalore","login","locations","locations","1107","ABCDE","fetch",field,"nil")
    locations = json.loads(locations)
    locations = locations['data']
    oses = dowellconnection("login","bangalore","login","os","os","1108","ABCDE","fetch",field,"nil")
    oses= json.loads(oses)
    oses = oses['data']
    connections = dowellconnection("login","bangalore","login","connections","connections","1110","ABCDE","fetch",field,"nil")
    connections = json.loads(connections)
    connections = connections['data']
    browsers = dowellconnection("login","bangalore","login","browsers","browsers","1109","ABCDE","fetch",field,"nil")
    browsers = json.loads(browsers)
    browsers = browsers['data']
    processes = dowellconnection("login","bangalore","login","processes","processes","1111","ABCDE","fetch",field,"nil")
    processes = json.loads(processes)
    processes = processes['data']
    playlists = dowellconnection("login","bangalore","login","youtube_playlist","youtube_playlist","1112","ABCDE","fetch",field,"nil")
    playlists = json.loads(playlists)
    playlists = playlists['data']
    projects = dowellconnection("login","bangalore","login","project","project","1086","ABCDE","fetch",field,"nil")
    projects = json.loads(projects)
    projects = projects['data']    

    if request.method == "POST":
            field= {}
            field_add= {}
            user_id = int(request.POST.get('users'))
            os = request.POST.getlist('oses')
            device = request.POST.getlist('devices')
            location = request.POST.getlist('locations')
            browser = request.POST.getlist('browsers')
            process = request.POST.getlist('processes')
            playlist = request.POST.getlist('playlists')
            connection = request.POST.getlist('connections')
            project = request.POST.getlist('projects')

            fetch = dowellconnection("login","bangalore","login","rights","rights","1113","ABCDE","fetch",field,"nil")
            r = json.loads(fetch)
            result = r['data']
            list_length = len(result)
            username = current_user['username']
            user_found = 0
            for r in result:
                if r['user'] == user_id :
                    user_found = 1 
                    break
                
            if user_found == 0 :
                field_add = {"id": list_length+1,'user':user_id,'project':project,'os':os,'device':device,'location':location,'browser':browser,'process':process,'playlist':playlist,'connection':connection}
                add = dowellconnection("login","bangalore","login","rights","rights","1113","ABCDE","insert",field_add,"nil")
                messages.success(request, 'Added rights' )   
            elif user_found ==1:
                messages.error(request, 'Already Exist' )   

            fetch_again = dowellconnection("login","bangalore","login","rights","rights","1113","ABCDE","fetch",field,"nil")
            r1 = json.loads(fetch_again)
            # print(result1)


            storage = get_messages(request)
            print(storage)
            for message in storage:
                print(message)


    context = {'session_id':session_id,'users':users,'oses':oses,'locations':locations,'devices':devices,'connections':connections,'browsers':browsers,'processes':processes,'playlists':playlists,'projects':projects}

    return render(request, 'rights.html',context)



@authenticationrequired
@is_client_and_super_admin
def add_layers(request):
    session_id = request.session.get('session_id')  
    result = []
    current_user = request.session.get('current_user')
    context = {'session_id':session_id}

    if request.method == "POST":
        pass

    return render(request, 'add_layers.html',context)


def access_denied(request):
    session_id = request.session.get('session_id')  
    context = {'session_id':session_id}

    return render(request,'access_denied.html',context)