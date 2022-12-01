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
from django.core.mail import EmailMessage

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
    # org = organisations
    org_dict= organisations[0]
    members = s["members"]
    members_dict = s["members"]["team_members"]
    guest_dict = s["members"]["guest_members"]
    pending_members = members_dict["pending_members"]
    accept_members = members_dict["accept_members"]
    pending_members_g = guest_dict["pending_members"]
    accept_members_g = guest_dict["accept_members"]

    level1 = org_dict["level1"]
    level2 = org_dict["level2"]
    level3 = org_dict["level3"]
    level4 = org_dict["level4"]
    level5 = org_dict["level5"]

    if not "level_name" in org_dict["level1"]:
        org_dict["level1"]["level_name"] = "level1"
        organisations.append(org_dict)          

        field= {"document_name":username}
        update_field = {"organisations":organisations}
        update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,update_field)
    elif not "level_name" in org_dict["level2"]:
        org_dict["level2"]["level_name"] = "level2"
        organisations.append(org_dict)          

        field= {"document_name":username}
        update_field = {"organisations":organisations}
        update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,update_field)       
    elif not "level_name" in org_dict["level3"]:
        org_dict["level3"]["level_name"] = "level3"
        organisations.append(org_dict)          

        field= {"document_name":username}
        update_field = {"organisations":organisations}
        update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,update_field)
    elif not "level_name" in org_dict["level4"]:
        org_dict["level4"]["level_name"] = "level4"
        organisations.append(org_dict)          

        field= {"document_name":username}
        update_field = {"organisations":organisations}
        update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,update_field) 
    elif not "level_name" in org_dict["level5"]:
        org_dict["level5"]["level_name"] = "level5"
        organisations.append(org_dict)          

        field= {"document_name":username}
        update_field = {"organisations":organisations}
        update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,update_field) 
    # print(organisations[username])
    # print(org)

    # print(items)

    if request.method == "POST" and "add_item1" in request.POST:
        s = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field,"nil")
        s = json.loads(s)
        s = s["data"][0]
        organisations = s["organisations"]
        org_dict= organisations[0]

        item_name = request.POST.get("item1_name")
        items= org_dict["level1"]["items"]
        if item_name :
            items.append(item_name)

        org_dict["level1"]["items"] = items
        organisations.append(org_dict)          
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
        org_dict= organisations[0]

        item_name = request.POST.get("item2_name")
        items= org_dict["level2"]["items"]
        if item_name :
            items.append(item_name)

        org_dict["level2"]["items"] = items
        organisations.append(org_dict)          

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
        org_dict= organisations[0]

        item_name = request.POST.get("item3_name")
        items= org_dict["level3"]["items"]
        if item_name :
            items.append(item_name)

        org_dict["level3"]["items"] = items
        organisations.append(org_dict)          

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
        org_dict= organisations[0]

        item_name = request.POST.get("item4_name")
        items= org_dict["level4"]["items"]
        if item_name :
            items.append(item_name)

        org_dict["level4"]["items"] = items
        organisations.append(org_dict)          

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
        org_dict= organisations[0]

        item_name = request.POST.get("item5_name")
        items= org_dict["level5"]["items"]
        if item_name :
            items.append(item_name)

        org_dict["level5"]["items"] = items
        organisations.append(org_dict)          

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
        
        org1 = organisations[0]
        org1["level1"]["level_name"] = level_name
        organisations.append(org1)          

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
        org2 = organisations[0]
        org2["level2"]["level_name"] = level_name
        organisations.append(org2)          

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
        org3 = organisations[0]
        org3["level3"]["level_name"] = level_name
        organisations.append(org3)          

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
        org4 = organisations[0]
        org4["level4"]["level_name"] = level_name
        organisations.append(org4)          
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
        org5 = organisations[0]
        org5["level5"]["level_name"] = level_name
        organisations.append(org5)          

        field= {"document_name":username}
        field_update = {"organisations":org5}
        try: 
            update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,field_update)
            messages.success("item successfully added")
            return HttpResponseRedirect('/')            
            print("successfully updated level")
        except:
            pass
            
    if request.method == "POST" and "invite_member_btn" in request.POST:
        email = request.POST.get("member_email")
        if email in str(members):
            messages.error(request, 'Email Already Invited' )
            context = {"profile_info":s["profile_info"],"username":username,"products":s["products"],"portfolio":s["portpolio"],"organisations":s["organisations"],"level1":level1,"level2":level2,"level3":level3,"level4":level4,"level5":level5,"pending_members":pending_members,"accept_members":accept_members,"pending_members_g":pending_members_g,"accept_members_g":accept_members_g}
            return render(request,"client_admin_new/index.html",context)  

        
        if not '@' in email:
            messages.error(request, 'Email Not Entered' )
            context = {"profile_info":s["profile_info"],"username":username,"products":s["products"],"portfolio":s["portpolio"],"organisations":s["organisations"],"level1":level1,"level2":level2,"level3":level3,"level4":level4,"level5":level5,"pending_members":pending_members,"accept_members":accept_members,"pending_members_g":pending_members_g,"accept_members_g":accept_members_g}
            return render(request,"client_admin_new/index.html",context)            
            

        url = 'https://100014.pythonanywhere.com/api/listusers/'
        data={"pwd":"d0wellre$tp@$$"}

        sess = requests.session()
        p = sess.post(url, data=data)
        r = p.text
        r = json.loads(r)
        users = r
        found_users = []
        invited_user = {}
        # print(users)
        for user in users:
            if user["email"] == email:
                # print(user["email"])
                invited_user["name"] = user["username"]
                invited_user["email"] = user["email"]
                invited_user["first_name"] = user["first_name"]
                invited_user["last_name"] = user["last_name"]
                found_users.append(invited_user)
            #     flag = True
            # else: 
            #     flag = False    
        context = {"found_users":found_users}
        return render(request,"client_admin_new/select_members.html",context)
        
    if request.method == "POST" and "invite_member" in request.POST:
        selected_member = {}
        to_member = request.POST.get("flexRadio").split('#')
        selected_member["name"] = to_member[0]
        selected_member["email"] = to_member[1]
        selected_member["first_name"] = to_member[2]
        selected_member["last_name"] = to_member[3]
        print(selected_member)
        email = to_member[1]
        username = selected_member["name"]
        first_name = selected_member["first_name"]
        last_name = selected_member["last_name"]

        messages.success(request, 'Invitation Sent' )  
        # htmlgen = f'You have been invited by {current_user["username"]} for joining his/her brand  {brand}<br> Click on this <a href="https://100079.pythonanywhere.com/linklogin/?company={brand[0]}&email={email}"> link </a>'
        # # send_mail('Email','jaheer@alfotechindia.com','sending email',email, fail_silently=False, html_message=htmlgen)
        # send_mail(
        #     subject='Invitation to Join Brand',
        #     message=htmlgen,
        #     from_email='coolguyjazz365@gmail.com',
        #     recipient_list=[email],
        #     fail_silently=False
        # )

                # import html message.html file
        # html_template = 'invitation_email.html'

        email_body = """\
        <table class="body-wrap" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; width: 100%; background-color: #f6f6f6; margin: 0;" bgcolor="#f6f6f6">
            <tbody>
                <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                    <td style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0;" valign="top"></td>
                    <td class="container" width="600" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; display: block !important; max-width: 600px !important; clear: both !important; margin: 0 auto;"
                        valign="top">
                        <div class="content" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; max-width: 600px; display: block; margin: 0 auto; padding: 20px;">
                            <table class="main" width="100%" cellpadding="0" cellspacing="0" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; border-radius: 3px; background-color: #fff; margin: 0; border: 1px solid #e9e9e9;"
                                bgcolor="#fff">
                                <tbody>
                                    <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                        <td class="" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 16px; vertical-align: top; color: #fff; font-weight: 500; text-align: center; border-radius: 3px 3px 0 0; background-color: #38414a; margin: 0; padding: 20px;"
                                            align="center" bgcolor="#71b6f9" valign="top">
                                            <a href="#" style="font-size:32px;color:#fff;"> Dowell</a> <br>
                                            <span style="margin-top: 10px;display: block;">Hello, You have been Invited to Join the Brand {{brand}}.</span>
                                        </td>
                                    </tr>
                                    <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                        <td class="content-wrap" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 20px;" valign="top">
                                            <table width="100%" cellpadding="0" cellspacing="0" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                <tbody>
                                                    <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                        <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
                                                
                                                        </td>
                                                    </tr>
                                                    <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                        <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
                                                            Please click on the link below to Join the Brand.
                                                        </td>
                                                    </tr>
                                                    <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                        <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
                                                            <a href="https://100079.pythonanywhere.com/join/?company={{brand}}&email={{email}}&username={{username}}&first_name={{first_name}}&last_name={{last_name}}" class="btn-primary" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; color: #FFF; text-decoration: none; line-height: 2em; font-weight: bold; text-align: center; cursor: pointer; display: inline-block; border-radius: 5px; text-transform: capitalize; background-color: #f1556c; margin: 0; border-color: #f1556c; border-style: solid; border-width: 8px 16px;">
                                            Join</a> </td>
                                            </tr>
                                            <tr>
                                            <td> https://100079.pythonanywhere.com/join/?company={{brand}}&email={{email}}&username={{username}}&first_name={{first_name}}&last_name={{last_name}} You can also copy and paste this link to browser.
                                        
                                                        </td>
                                                    </tr>
                                                    <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                        <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
                                                            Thanks for choosing <b>Dowell</b> .
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <div class="footer" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; width: 100%; clear: both; color: #999; margin: 0; padding: 20px;">
                                <table width="100%" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                    <tbody>
                                        <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">

                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </td>
                    <td style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0;" valign="top"></td>
                </tr>
            </tbody>
        </table>
        """

        email_body = email_body.replace('{{brand}}',username).replace('{{email}}',email).replace('{{username}}',username).replace('{{first_name}}',first_name).replace('{{last_name}}',last_name)
        # html_template = get_template('invitation_email.html')
        # html_message = render_to_string(html_template, { 'context': context, })
        subject='Invitation to Join Organization'
        from_email='coolguyjazz365@gmail.com'
        to_email = email
        message = EmailMessage(subject, email_body, from_email, [to_email])
        message.content_subtype = 'html' # this is required because there is no plain text email message

        message.send()

        members["team_members"]["pending_members"].append(selected_member)
        field_update = {"members":members}
        update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,field_update)

    if request.method == "POST" and "invite_guest_btn" in request.POST:
        email = request.POST.get("guest_email")
        if email in str(members):
            messages.error(request, 'Email Already Invited' )
            context = {"profile_info":s["profile_info"],"username":username,"products":s["products"],"portfolio":s["portpolio"],"organisations":s["organisations"],"level1":level1,"level2":level2,"level3":level3,"level4":level4,"level5":level5,"pending_members":pending_members,"accept_members":accept_members,"pending_members_g":pending_members_g,"accept_members_g":accept_members_g}
            return render(request,"client_admin_new/index.html",context)  

        
        if not '@' in email:
            messages.error(request, 'Email Not Entered' )
            context = {"profile_info":s["profile_info"],"username":username,"products":s["products"],"portfolio":s["portpolio"],"organisations":s["organisations"],"level1":level1,"level2":level2,"level3":level3,"level4":level4,"level5":level5,"pending_members":pending_members,"accept_members":accept_members,"pending_members_g":pending_members_g,"accept_members_g":accept_members_g}
            return render(request,"client_admin_new/index.html",context)            
            

        # url = 'https://100014.pythonanywhere.com/api/listusers/'
        # data={"pwd":"d0wellre$tp@$$"}

        to_member = request.POST.get("guest_email")

        # htmlgen = f'You have been invited by {current_user["username"]} for joining his/her brand  {brand}<br> Click on this <a href="https://100079.pythonanywhere.com/linklogin/?company={brand[0]}&email={email}"> link </a>'
        # # send_mail('Email','jaheer@alfotechindia.com','sending email',email, fail_silently=False, html_message=htmlgen)
        # send_mail(
        #     subject='Invitation to Join Brand',
        #     message=htmlgen,
        #     from_email='coolguyjazz365@gmail.com',
        #     recipient_list=[email],
        #     fail_silently=False
        # )

                # import html message.html file
        # html_template = 'invitation_email.html'

        email_body = """\
        <table class="body-wrap" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; width: 100%; background-color: #f6f6f6; margin: 0;" bgcolor="#f6f6f6">
            <tbody>
                <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                    <td style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0;" valign="top"></td>
                    <td class="container" width="600" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; display: block !important; max-width: 600px !important; clear: both !important; margin: 0 auto;"
                        valign="top">
                        <div class="content" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; max-width: 600px; display: block; margin: 0 auto; padding: 20px;">
                            <table class="main" width="100%" cellpadding="0" cellspacing="0" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; border-radius: 3px; background-color: #fff; margin: 0; border: 1px solid #e9e9e9;"
                                bgcolor="#fff">
                                <tbody>
                                    <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                        <td class="" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 16px; vertical-align: top; color: #fff; font-weight: 500; text-align: center; border-radius: 3px 3px 0 0; background-color: #38414a; margin: 0; padding: 20px;"
                                            align="center" bgcolor="#71b6f9" valign="top">
                                            <a href="#" style="font-size:32px;color:#fff;"> Dowell</a> <br>
                                            <span style="margin-top: 10px;display: block;">Hello, You have been Invited to Join the Brand {{brand}}.</span>
                                        </td>
                                    </tr>
                                    <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                        <td class="content-wrap" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 20px;" valign="top">
                                            <table width="100%" cellpadding="0" cellspacing="0" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                <tbody>
                                                    <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                        <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
                                                
                                                        </td>
                                                    </tr>
                                                    <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                        <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
                                                            Please click on the link below to Join the Brand.
                                                        </td>
                                                    </tr>
                                                    <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                        <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
                                                            <a href="https://100079.pythonanywhere.com/guest-join/?company={{brand}}&email={{email}}" class="btn-primary" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; color: #FFF; text-decoration: none; line-height: 2em; font-weight: bold; text-align: center; cursor: pointer; display: inline-block; border-radius: 5px; text-transform: capitalize; background-color: #f1556c; margin: 0; border-color: #f1556c; border-style: solid; border-width: 8px 16px;">
                                            Join</a> </td>
                                            </tr>
                                            <tr>
                                            <td> https://100079.pythonanywhere.com/guest-join/?company={{brand}}&email={{email}} You can also copy and paste this link to browser.
                                        
                                                        </td>
                                                    </tr>
                                                    <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                        <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
                                                            Thanks for choosing <b>Dowell</b> .
                                                        </td>
                                                    </tr>
                                                </tbody>
                                            </table>
                                        </td>
                                    </tr>
                                </tbody>
                            </table>
                            <div class="footer" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; width: 100%; clear: both; color: #999; margin: 0; padding: 20px;">
                                <table width="100%" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                    <tbody>
                                        <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">

                                            </td>
                                        </tr>
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </td>
                    <td style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0;" valign="top"></td>
                </tr>
            </tbody>
        </table>
        """

        email_body = email_body.replace('{{brand}}',username).replace('{{email}}',email)
        # html_template = get_template('invitation_email.html')
        # html_message = render_to_string(html_template, { 'context': context, })
        subject='Invitation to Join Organization'
        from_email='coolguyjazz365@gmail.com'
        to_email = email
        message = EmailMessage(subject, email_body, from_email, [to_email])
        message.content_subtype = 'html' # this is required because there is no plain text email message

        message.send()

        members["guest_members"]["pending_members"].append(to_member)
        field_update = {"members":members}
        update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,field_update)
        messages.success(request, 'Invitation Sent' )  


    # if flag == False:
    #     messages.error(request, 'Email Not Found' )
    #     context = {"profile_info":s["profile_info"],"username":username,"products":s["products"],"portfolio":s["portpolio"],"organisations":s["organisations"],"level1":level1,"level2":level2,"level3":level3,"level4":level4,"level5":level5,"pending_members":pending_members}
    #     return render(request,"client_admin_new/index.html",context)                  

    # if flag == False:
    #     messages.error(request, 'Email Not Found' )
    # elif flag == True:
    #     messages.success(request, 'Email Found' )  
    # if flag == True:

        

    #list out on products tab
    context = {"profile_info":s["profile_info"],"username":username,"products":s["products"],"portfolio":s["portpolio"],"organisations":s["organisations"],"level1":level1,"level2":level2,"level3":level3,"level4":level4,"level5":level5,"pending_members":pending_members,"accept_members":accept_members,"pending_members_g":pending_members_g,"accept_members_g":accept_members_g}

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



def linklogin_new(request):
    email = str(request.GET.get('email'))
    brand = request.GET.get('company')
    username = request.GET.get('username')
    first_name = request.GET.get('first_name')
    last_name = request.GET.get('last_name')

    # session_id = request.session.get('session_id')

    dict = {'name': username, 'email': email, 'first_name': first_name, 'last_name': last_name}
    # print(dict)
    # field={}
    username = brand
    field = {"document_name":username}
    s = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field,"nil")
    s = json.loads(s)
    s = s["data"][0]    
    organisations = s["organisations"]
    # org = organisations
    org_dict= organisations[0]
    members = s["members"]
    members_dict = s["members"]["team_members"]
    pending_members = members_dict["pending_members"]
    accept_members = members_dict["accept_members"]
    # print(pending_members)
    # print(accept_members)
    if email in str(accept_members):
        flag = 0
        return render(request,'client_admin_new/success.html',{"flag":flag})

    accept_members.append(dict)
    flag = 1
    if not email in str(pending_members):
        flag = 2
        return render(request,'client_admin_new/success.html',{"flag":flag})

    members["team_members"]["accept_members"] = accept_members
    # field_update = {"members":members}
    # update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,field_update)    

    # for d in pending_members:
    #     if type(d) is dict:
    #         for k,v in d.items():
    #             if "abcd@gmail.com" in v:
    #                 pending_members.remove(d)
    
    p_m = [p for p in pending_members if not email in str(p) and type(p) is dict]
    # print(pending_members)
    print(p_m)
    members["team_members"]["pending_members"] = p_m
    field_update = {"members":members}
    print(members)
    update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,field_update)    

    # org_dict = s["members"]

    #Use registration collection
    context = {}

    return render(request,'client_admin_new/success.html',{"flag":flag})


def guestlogin(request):
    email = str(request.GET.get('email'))
    brand = request.GET.get('company')
    # session_id = request.session.get('session_id')

    # print(dict)
    # field={}
    username = brand
    field = {"document_name":username}
    s = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field,"nil")
    s = json.loads(s)
    s = s["data"][0]    
    organisations = s["organisations"]
    # org = organisations
    org_dict= organisations[0]
    members = s["members"]
    members_dict = s["members"]["guest_members"]
    pending_members = members_dict["pending_members"]
    accept_members = members_dict["accept_members"]
    # print(pending_members)
    # print(accept_members)
    if email in str(accept_members):
        flag = 0
        return render(request,'client_admin_new/success.html',{"flag":flag})

    accept_members.append(email)
    flag = 1
    if not email in str(pending_members):
        flag = 2
        return render(request,'client_admin_new/success.html',{"flag":flag})

    members["guest_members"]["accept_members"] = accept_members
    # field_update = {"members":members}
    # update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,field_update)    

    # for d in pending_members:
    #     if type(d) is dict:
    #         for k,v in d.items():
    #             if "abcd@gmail.com" in v:
    #                 pending_members.remove(d)
    
    p_m = [p for p in pending_members if not email in str(p)]
    # print(pending_members)
    print(p_m)
    members["guest_members"]["pending_members"] = p_m
    field_update = {"members":members}
    print(members)
    update = dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,field_update)    

    # org_dict = s["members"]

    #Use registration collection
    context = {}

    return render(request,'client_admin_new/success.html',{"flag":flag})

def get_user_info(request,email):
    url = 'https://100014.pythonanywhere.com/api/listusers/'
    data={"pwd":"d0wellre$tp@$$"}

    sess = requests.session()
    p = sess.post(url, data=data)
    r = p.text
    r = json.loads(r)
    users = r
    found_users = []
    invited_user = {}
    # print(users)
    for user in users:
        if user["email"] == email:
            # print(user["email"])
            invited_user["name"] = user["username"]
            invited_user["email"] = user["email"]
            invited_user["first_name"] = user["first_name"]
            invited_user["last_name"] = user["last_name"]
            found_users.append(invited_user)
    
    return found_users