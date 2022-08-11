from distutils import unixccompiler
from unicodedata import category
from django.db import connection
from django.shortcuts import render, HttpResponse,redirect
from .forms import AddDepartment, AddOrganisation, AddProject, RegisterClient,LoginClient,AddCompany,EditCompany
import requests
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth.decorators import user_passes_test
import json
import base64
from .decorators import authenticationrequired, loginrequired, unauthenticated_user
from django.contrib import messages
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
    del request.session['session_id']

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
    company_number = request.session.get('company_number')
    organisation_number = request.session.get('organisation_number')
    department_number = request.session.get('department_number')    
    project_number = request.session.get('project_number')
    context = {'session_id':session_id,'users':users,'access_granted':access_granted,'company_number':company_number,'organisation_number':organisation_number,"department_number":department_number, "project_number":project_number}         

    # print(Dowell_Login("username","password","location","device","os","browser","time","ip","type_of_conn"))
    return render(request, 'new_users.html', context) 


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

    hit0 =get_company(request)
    hit = get_organisation(request)
    hit1 = get_department(request)
    hit2 = get_project(request)
    context = {'session_id':session_id}
    company_number = request.session.get('company_number')
    organisation_number = request.session.get('organisation_number')
    department_number = request.session.get('department_number')
    project_number = request.session.get('project_number')
    context = {'session_id':session_id,'company_number':company_number,'organisation_number':organisation_number,"department_number":department_number, "project_number":project_number}

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
                messages.success(request, "User with Username : "+username+" Already Existis")
                return HttpResponseRedirect('/add_user/?session_id='+session_id) 
    
    company_number = request.session.get('company_number')
    organisation_number = request.session.get('organisation_number')
    department_number = request.session.get('department_number')
    project_number = request.session.get('project_number')

    context=  {"session_id":session_id,'access_granted':access_granted,'company_number':company_number,'organisation_number':organisation_number,"department_number":department_number, "project_number":project_number}

    return render(request, 'add_user.html',context)



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
        if 'Admin' in current_user['role']:
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
    company_number = request.session.get('company_number')
    organisation_number = request.session.get('organisation_number')
    department_number = request.session.get('department_number')
    project_number = request.session.get('project_number')

    context = {'session_id':session_id,'companies':result,'access_granted':access_granted,'company_number':company_number,'organisation_number':organisation_number,"department_number":department_number, "project_number":project_number}
    # print(request.session.get('current_user'))


    if request.method == "POST":
            field= {}
            # organisation = form.data['org_name']
            organisation = request.POST.get('org_name')
            # company = form.data['companyName']
            if request.POST.get('companyName') is None:
                messages.success(request, "No Companies Assigned")
                return HttpResponseRedirect('/add_organisation/?session_id='+session_id) 

            if len(request.POST.get('org_name')) < 4:
                messages.success(request, "Please Enter 4 or More Characters ")
                return HttpResponseRedirect('/add_organisation/?session_id='+session_id) 

            company = int(request.POST.get('companyName'))
            r = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","fetch",field,"nil")
            r = json.loads(r)
            # print(company)
            result = r['data']
            organisation_length = len(result)
            field_add = {"name": organisation,"company_id" : company,"organization_id": organisation_length}
            add = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","insert",field_add,"nil")
            r1 = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","fetch",field,"nil")
            r1 = json.loads(r1)
            result1 = r1['data']
            new_company_length = len(result1)
            if new_company_length == organisation_length + 1:
                messages.success(request, "Organisation Successfully added with Organisation  Name : "+organisation)
            else:
                messages.success(request, "Problem Adding Organisation")
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
        if 'Admin' in current_user['role']:
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


    company_number = request.session.get('company_number')
    organisation_number = request.session.get('organisation_number')
    department_number = request.session.get('department_number')
    project_number = request.session.get('project_number')

    context = {'session_id':session_id,"organisation_placeholder":organisation_placeholder,"company_placeholder":company_placeholder,"company_id":c_id,"company":company,'access_granted':access_granted,'company_number':company_number,'organisation_number':organisation_number,"department_number":department_number, "project_number":project_number}


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
        if 'Admin' in current_user['role']:
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
    
    company_number = request.session.get('company_number')
    organisation_number = request.session.get('organisation_number')
    department_number = request.session.get('department_number')
    project_number = request.session.get('project_number')

    context = {'session_id':session_id,"department_placeholder":department_placeholder,"organisation_placeholder":organisation_placeholder,"organisation_id":o_id,"organisation":organisation,"access_granted":access_granted,'company_number':company_number,'organisation_number':organisation_number,"department_number":department_number, "project_number":project_number}


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
        if 'Admin' in current_user['role']:
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


    company_number = request.session.get('company_number')
    organisation_number = request.session.get('organisation_number')
    department_number = request.session.get('department_number')
    project_number = request.session.get('project_number')      

    context = {'session_id':session_id,"department_placeholder":department_placeholder,"project_placeholder":project_placeholder,"department_id":d_id,"department":department,"access_granted":access_granted,
                'company_number':company_number,'organisation_number':organisation_number,"department_number":department_number, "project_number":project_number}


    return render(request, 'new_edit_project.html',context)

@authenticationrequired
def add_company(request):
    session_id = request.session.get('session_id')

    access_granted = 0
  


    result = []
    current_user = request.session.get('current_user')
    try:
        if 'Admin' in current_user['role']:
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
            r = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
            r = json.loads(r)
            result = r['data']
            company_length = len(result)
            field_add = {"company": company, "company_id" : company_length+1}
            add = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","insert",field_add,"nil")
            r1 = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
            r1 = json.loads(r1)
            result1 = r1['data']
            new_company_length = len(result1)
            if new_company_length == company_length + 1:
                messages.success(request, "Company Successfully added with Company  Name : "+company )
            else:
                messages.success(request, "Problem Adding Company")
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
        if 'Admin' in current_user['role']:
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

    company_number = request.session.get('company_number')
    organisation_number = request.session.get('organisation_number')
    department_number = request.session.get('department_number')
    project_number = request.session.get('project_number')

    context = {'session_id':session_id,"company_placeholder":company_placeholder,"access_granted":access_granted,'company_number':company_number,'organisation_number':organisation_number,"department_number":department_number, "project_number":project_number}


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
    result = []
    current_user = request.session.get('current_user')
    try:
        if 'Admin' in current_user['role']:
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
    company_number = request.session.get('company_number')
    organisation_number = request.session.get('organisation_number')
    department_number = request.session.get('department_number')
    project_number = request.session.get('project_number')
    context = {'session_id':session_id,'company':result,"company_number":company_number,'organisation_number':organisation_number,"department_number":department_number, "project_number":project_number}
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
    try:
        if 'Admin' in current_user['role']:
            result = r['data']    
            result1 = r1['data']
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
    company_number = request.session.get('company_number')
    department_number = request.session.get('department_number')
    project_number = request.session.get('project_number')
    organisation_number = request.session.get('organisation_number')
    context = {"session_id":session_id, "organisations":organisations, "companies":companies,"union":union, "company_number":company_number,"organisation_number":organisation_number,"department_number":department_number,"project_number":project_number}
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
        if 'Admin' in current_user['role']:
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

    company_number = request.session.get('company_number')
    department_number = request.session.get('department_number')
    project_number = request.session.get('project_number')
    organisation_number = request.session.get('organisation_number')
    context = {"session_id":session_id, "departments":departments, "union":union,"organisations":organisations,"company_number":company_number,"project_number":project_number,"department_number":department_number,"organisation_number":organisation_number}

    # context = {"company":result,"session_id":session_id}
    return render(request, 'new_display_department.html',context)

@authenticationrequired
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
        if 'Admin' in current_user['role']:
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

    company_number = request.session.get('company_number')
    department_number = request.session.get('department_number')
    project_number = request.session.get('project_number')
    organisation_number = request.session.get('organisation_number')
    context = {"session_id":session_id, "projects":projects,"union":union,"departments":departments,"organisation_number":organisation_number, "company_number": company_number,"department_number":department_number,"project_number":project_number}
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
        if 'Admin' in current_user['role']:
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

    company_number = request.session.get('company_number')
    organisation_number = request.session.get('organisation_number')
    department_number = request.session.get('department_number')
    project_number = request.session.get('project_number')

    context = {'session_id':session_id,'organisations':result,'access_granted':access_granted,"organisation_number":organisation_number, "company_number": company_number,"department_number":department_number,"project_number":project_number}

    if request.method == "POST":
            field= {}
            department = request.POST.get('department_name')

            if request.POST.get('orgName') is None:
                messages.success(request, "No Organisations Assigned")
                return HttpResponseRedirect('/add_department/?session_id='+session_id) 

            if len(request.POST.get('department_name')) < 4:
                messages.success(request, "Please Enter 4 or More Characters ")
                return HttpResponseRedirect('/add_department/?session_id='+session_id) 

            organisation = int(request.POST.get('orgName'))
            # print("Orgname is"+organisation)
            r = dowellconnection("login","bangalore","login","department","department","1085","ABCDE","fetch",field,"nil")
            r = json.loads(r)
            result = r['data']
            company_length = len(result)
            field_add = {"department": department,"organization_id":organisation , "department_id" : company_length+1}
            add = dowellconnection("login","bangalore","login","department","department","1085","ABCDE","insert",field_add,"nil")
            r1 = dowellconnection("login","bangalore","login","department","department","1085","ABCDE","fetch",field,"nil")
            r1 = json.loads(r1)
            result1 = r1['data']
            new_company_length = len(result1)
            if new_company_length == company_length + 1:
                messages.success(request, "Department Successfully added with  Name : "+department )
            else:
                messages.success(request, "Problem Adding Department")
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
        if 'Admin' in current_user['role']:
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


    company_number = request.session.get('company_number')
    organisation_number = request.session.get('organisation_number')
    department_number = request.session.get('department_number')
    project_number = request.session.get('project_number')

    context = {'session_id':session_id,'departments':result,'access_granted':access_granted,"organisation_number":organisation_number, "company_number": company_number,"department_number":department_number,"project_number":project_number}

    if request.method == "POST":
            field= {}
            project = request.POST.get('project_name')
            # print(project)
            department = int(request.POST.get('department_name'))
            r = dowellconnection("login","bangalore","login","project","project","1086","ABCDE","fetch",field,"nil")
            r = json.loads(r)
            result = r['data']
            company_length = len(result)
            field_add = {"project": project,"department_id":department , "project_id" : company_length+1}
            add = dowellconnection("login","bangalore","login","project","project","1086","ABCDE","insert",field_add,"nil")
            r1 = dowellconnection("login","bangalore","login","project","project","1086","ABCDE","fetch",field,"nil")
            r1 = json.loads(r1)
            result1 = r1['data']
            new_company_length = len(result1)
            if new_company_length == company_length + 1:
                messages.success(request, "Project Successfully added with  Name : "+project )
            else:
                messages.success(request, "Problem Adding Project")
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
def assign_roles(request):
    current_user = request.session.get('current_user')
    access_granted = 0
    try:
        if 'Admin' in current_user['role']:
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
    f = dowellconnection("login","bangalore","login","roles","roles","1089","ABCDE","fetch",field,"nil")
    users = r

    if request.method == "POST":
        role_assigned = 0
        data = request.POST.dict()
        user_id = int(data['users'])
        role = data['roles']
        category = data['category']
        role_String = f'{role}@{category}'
        update_url = "https://100014.pythonanywhere.com/api/update/"+str(user_id)
        update_data={
        "role": role_String
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
            messages.success(request, "Problem Assigning Role" )


    company_number = request.session.get('company_number')
    organisation_number = request.session.get('organisation_number')
    department_number = request.session.get('department_number')    
    project_number = request.session.get('project_number')
        

    context = {'access_level':access_level,'session_id':session_id,'users':users,'access_granted':access_granted,"organisation_number":organisation_number, "company_number": company_number,"department_number":department_number,"project_number":project_number}

    return render(request, 'assign_roles.html',context)

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