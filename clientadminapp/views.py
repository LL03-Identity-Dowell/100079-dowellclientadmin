from django.shortcuts import render,redirect,HttpResponse
from .models import UserInfo,UserPortfolio,UserOrg,Urls,UserData,publiclink,Devices,OperatingSystems,Browsers,InternetConnection,LoginType,PasswordStrength,IdVerification
from clientadminapp.dowellconnection import dowellconnection
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.core.files.storage import default_storage
import datetime
import json
from . import qrcodegen,passgen
import base64
import urllib

import requests
def Home(request):
    if request.session.get("session_id"):
        session=request.session["session_id"]
        # print(context["datalav"])
        return redirect(f'/new?session_id={session}')
    else:
        return redirect("https://100014.pythonanywhere.com/?redirect_url=https://100093.pythonanywhere.com/new")
def Home1(request):
    context={}
    var1 = Devices.objects.all()
    # context["devices"] = var1[0]
    context["devicess"]  = "Hello"
    # try:
    #     s=request.session.get("session_id")
    # except:
    #     s=False
    # if s:
    #     #return HttpResponse(s)
    
    #     return render(request,"index.html")

    # else:
    redirect_url=request.GET.get('session_id',None)
    #code=request.GET.get('code',None)
    # if code=="100093":
    #     url="https://100093.pythonanywhere.com/api/userinfo/"
    # else:
    #     url="https://100014.pythonanywhere.com/api/userinfo/"
    if redirect_url is not None:
        request.session["session_id"]=redirect_url

        url="https://100014.pythonanywhere.com/api/userinfo/"
        resp=requests.post(url,data={"session_id":redirect_url})
        try:
            user=json.loads(resp.text)
        except:
            return HttpResponse('<style>body{background-color: rgba(0,0,0, 0.4);}.close-btn {position: absolute;bottom: 12px;right: 25px;}.content {position: absolute;width: 250px;height: 200px;background: #fff;top: 0%;left: 50%;transform: translate(-50%, -50%)scale(0.1);visibility: hidden;transition: transform 0.4s, top 0.4s;}.open-popup {visibility: visible;top: 50%;transform: translate(-50%, -50%)scale(1);}.header {height: 50px;background: #efea53;overflow: hidden;text-align: center;}p {padding-top: 40px;text-align: center;}</style><div class="content open-popup" id="popup"><div class="header"><h2>Alert!</h2></div><p>Some thing went wrong pl <a href="logout" >logout </a> <a href="/">login</a> again</p><div><button type="button" onclick="history.back();" class="close-btn">close</button></div></div>')

        obj, created = UserInfo.objects.update_or_create(username=user["userinfo"]["username"],defaults={'userinfo': json.dumps(user["userinfo"])})
        field={"document_name":user["userinfo"]["username"]}
        login=dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field,"update")
        r=json.loads(login)
        request.session["username"]=user["userinfo"]["username"]
        obj, created = UserOrg.objects.update_or_create(username=user["userinfo"]["username"],defaults={'org': json.dumps(r["data"][0])})
        context["img"]=r["data"][0]["profile_info"]["profile_img"]
        context["first"]=r["data"][0]["profile_info"]["first_name"]
        context["last"]=r["data"][0]["profile_info"]["last_name"]
        context["time"]=user["userinfo"]["dowell_time"]
        context["location"]=user["userinfo"]["city"]
        lori=[r["data"][0]["organisations"][0]["org_name"]]
        for l in r["data"][0]["other_organisation"]:
            lori.append(l["org_name"])
        context["col"]=[*set(lori)]
        request.session["orgname"]=r["data"][0]["organisations"][0]["org_name"]
        request.session["present_org"]=r["data"][0]["organisations"][0]["org_name"]
        #pr=r["data"][0]["products"]
        pls=[]
        for i in r["data"][0]["portpolio"]:
            if i["username"]==user["userinfo"]["username"]:
                pls.append(i)
        obj, created = UserPortfolio.objects.update_or_create(username=user["userinfo"]["username"],defaults={'portfolio': json.dumps(pls)})
        context["pid"]=["workflow-ai","digital-q","wifi-qr-code","chat"]

        context["products"]=r["data"][0]["products"]
        aiport=[]
        dqport=[]
        qrport=[]
        chatport=[]
        for i in r["data"][0]["portpolio"]:
            if "workflow" in i["product"] or "all" in i["product"] or "owner" in i["product"]:
                aiport.append(i["portfolio_name"])
            if "digital" in i["product"] or "all" in i["product"] or "owner" in i["product"]:
                dqport.append(i["portfolio_name"])
            if "wifi" in i["product"] or "all" in i["product"] or "owner" in i["product"]:
                qrport.append(i["portfolio_name"])
            if "chat" in i["product"] or "all" in i["product"] or "owner" in i["product"]:
                chatport.append(i["portfolio_name"])
            if i["username"]==user["userinfo"]["username"]:
                context["opr"]=i["operations_right"]
                context["data"]=i["data_type"]
        #context["port"]=port
        context["aiport"]=aiport
        context["dqport"]=dqport
        context["qrport"]=qrport
        context["chatport"]=chatport
        context["org"]=r["data"][0]["organisations"][0]["org_name"]
        context["datalav"]=r["data"][0]
        br = base64.b64encode(bytes(r["data"][0]["organisations"][0]["org_name"], 'utf-8')) # bytes
        brc=br.decode("utf-8")
        context["brc"]=br.decode("utf-8")
        #context["turl"]=f'https://100093.pythonanywhere.com/invitesocial?next={brc}&type=team_member'
        context["gurl"]=f'https://100093.pythonanywhere.com/invitesocial?next={brc}&type=guest_member'
        context["purl"]=f'https://100093.pythonanywhere.com/invitesocial?next={brc}&type=public_member'
        #base64_str = b.decode('utf-8')
        # context["level1item"]=r["data"][0]["organisations"][0]["level1"]["items"]
        # context["level2item"]=r["data"][0]["organisations"][0]["level2"]["items"]
        # context["level3item"]=r["data"][0]["organisations"][0]["level3"]["items"]
        # context["level4item"]=r["data"][0]["organisations"][0]["level4"]["items"]
        # context["level5item"]=r["data"][0]["organisations"][0]["level5"]["items"]
        # context["level1"]=r["data"][0]["organisations"][0]["level1"]["level_name"]
        # context["level1"]=r["data"][0]["organisations"][0]["level1"]["level_name"]
        # context["level1"]=r["data"][0]["organisations"][0]["level1"]["level_name"]
        # context["level1"]=r["data"][0]["organisations"][0]["level1"]["level_name"]
        #request.session.modified = True
        context["public"]=publiclink.objects.all().filter(username=user["userinfo"]["username"])

        print(context["datalav"])
        return render(request,"index.html",context)
    else:
        return redirect("https://100014.pythonanywhere.com/?redirect_url=https://100093.pythonanywhere.com")

def portfolio(request):
    re=request.POST
    r=[k for k,v in re.items() if v ==k]
    portf=request.POST["portfl"]
    product=request.POST["product"]
    user=request.session["username"]
    orl=request.session["present_org"]
    session=request.session["session_id"]
    lo=UserOrg.objects.all().filter(username=orl)
    for rd in lo:
        lo1=rd.org
        lrf=json.loads(lo1)
    ro=UserInfo.objects.all().filter(username=user)
    ro1=UserOrg.objects.all().filter(username=user)

    mydict={}

    for i in ro:
        rofield=i.userinfo
        #s = rofield.replace("\'", "\"")
        s=json.loads(rofield)
        mydict["userinfo"]=s

    for ii in ro1:
        pfield=ii.org
        #s = rofield.replace("\'", "\"")
        ss=json.loads(pfield)
        rr=ss["other_organisation"]
        rr1=ss["organisations"]
    #
    for iii in rr:
        if iii["org_name"]==request.session["present_org"]:
            try:
                if iii["portfolio_name"]==portf:
                    mydict["portfolio_info"]=[iii]

                else:
                    pass
            except:
                pass
    try:
        selected_role=mydict["portfolio_info"]["role"]
    except:
        pass
    level1={}
    level2={}
    level3={}
    level4={}
    level5={}
    try:
        for items in lrf["roles"]:
            if selected_role==items["role_name"]:
                if items["level1_item"]:
                    level1["level1name"]=lrf["organisations"][0]["level1"]["level_name"]
                    level1["level1items"]=lrf["organisations"][0]["level1"]["items"]
                if items["level2_item"]:
                    level2["level1name"]=lrf["organisations"][0]["level2"]["level_name"]
                    level2["level1items"]=lrf["organisations"][0]["level2"]["items"]
                if items["level3_item"]:
                    level2["level3name"]=lrf["organisations"][0]["level3"]["level_name"]
                    level2["level3items"]=lrf["organisations"][0]["level3"]["items"]
                if items["level4_item"]:
                    level2["level4name"]=lrf["organisations"][0]["level4"]["level_name"]
                    level2["level4items"]=lrf["organisations"][0]["level4"]["items"]
                if items["level5_item"]:
                    level2["level5name"]=lrf["organisations"][0]["level5"]["level_name"]
                    level2["level5items"]=lrf["organisations"][0]["level5"]["items"]
    except:
        pass
    if "portfolio_info" not in mydict:
        #return HttpResponse(f'{rr1}')
        mydict["portfolio_info"]=[ss["portpolio"][0]]
    productport=[]
    for product2 in lrf["portpolio"]:
        if product==product2["product"]:
            productport.append(product2)

    mydict["organisations"]=[{"orgname":lrf["document_name"],"orgowner":lrf["document_name"]}]
    mydict["selected_product"]={"product_id":1,"product_name":product,"platformpermissionproduct":[{"type":"member","operational_rights":["view","add","edit","delete"],"role":"admin"}],"platformpermissiondata":["real","learning","testing","archived"],"orgid":lrf["_id"],"orglogo":"","ownerid":"","userportfolio":productport,"payment_status":"paid"}
    mydict["selected_portfoliolevel"]=level1
    mydict["selected_portfolioleve2"]=level2
    mydict["selected_portfolioleve3"]=level3
    mydict["selected_portfolioleve4"]=level4
    mydict["selected_portfolioleve5"]=level5
    mydict["portfolio_info"][0]["org_id"]=lrf["_id"]
    mydict["portfolio_info"][0]["owner_name"]=lrf["document_name"]
    obj, created = UserData.objects.update_or_create(username=user,sessionid=session,defaults={'alldata': json.dumps(mydict)})
    if "Workflow AI" in product or "workflow" in product:
        # return redirect(f'https://ll04-finance-dowell.github.io/100018-dowellWorkflowAi-testing/?session_id={request.session["session_id"]}&id=100093')
        return redirect(f'https://ll04-finance-dowell.github.io/100018-dowellWorkflowAi-testing/#/?session_id={request.session["session_id"]}&id=100093')
    else:
        return HttpResponse(f"<h1 align='center'>Redirect the URL of this {product} product not avail in database<br><a href='/'>Home</a></h1>")
@csrf_exempt
def sessiondetails(request):
    if request.method=="POST":
        s=request.POST["session_id"]
        ro1=UserPortfolio.objects.all().filter(sessionid=s)
        for i in ro1:
            r=i.alldata
            rj=json.loads(r)
        return JsonResponse(rj)
def levels(request):
    #level1="raju"
        r=""
        ls=[]
    #try:
        level=request.POST.keys()
        if "level_name1" in  level:
            level1=request.POST["level_name1"]
            ls.append(level1)
            r="level1"
        if "level_name2" in  level:
            level2=request.POST["level_name2"]
            ls.append(level2)
            r="level2"
        if "level_name3" in  level:
            level3=request.POST["level_name3"]
            ls.append(level3)
            r="level3"
        if "level_name4" in  level:
            level4=request.POST["level_name4"]
            ls.append(level4)
            r="level4"
        if "level_name5" in  level:
            level5=request.POST["level_name5"]
            ls.append(level5)
            r="level5"

        userorg=UserOrg.objects.all().filter(username=request.session["username"])
        if userorg:
            for i in userorg:
                o=i.org
                odata=json.loads(o)
            org=odata["organisations"]
            print(type(org))
            org[0][r]["level_name"]=ls[0]
            #return HttpResponse(f'{org} is list')
            field={"document_name":request.session["username"]}
            update={"organisations":org}
            login=dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,update)
            print(login)
            return redirect(f'/?session_id={request.session["session_id"]}')
        else:
            return HttpResponse("no values")
    #except:
        pass
def items(request):
    #level1="raju"
        r=""
        ls=[]
        imageurl=""
        barurl=""
        imageurl1=""
    #try:
        level=request.POST.keys()
        if "item_name1" in  level:
            level1=request.POST["item_name1"]
            ls.append(level1)
            itemcode=request.POST["item_code1"]
            itemdet=request.POST["item_det1"]
            itemuni=request.POST["item_u_code1"]
            itemspec=request.POST["item_spec1"]
            itembar=request.FILES.get("item_barcode1",None)
            try:
                file_name = default_storage.save(f'itemimages/{itembar.name}', itembar)
                barurl=default_storage.url(file_name)
            except:
                pass
            itemimage1=request.FILES.get("item_image1",None)
            try:
                file_name1 = default_storage.save(f'itemimages/{itemimage1.name}', itemimage1)
                imageurl=default_storage.url(file_name1)
            except:
                pass
            itemimage2=request.FILES.get("item_image2",None)
            try:

                file_name2 = default_storage.save(f'itemimages/{itemimage2.name}',itemimage2)
                imageurl1=default_storage.url(file_name2)
            except:
                pass
            r="level1"
        if "item_name2" in  level:
            level2=request.POST["item_name2"]
            ls.append(level2)
            itemcode=request.POST["item_code2"]
            itemdet=request.POST["item_det2"]
            itemuni=request.POST["item_u_code2"]
            itemspec=request.POST["item_spec2"]
            itembar=request.FILES.get("item_barcode1",None)
            try:
                file_name = default_storage.save(f'itemimages/{itembar.name}', itembar)
                barurl=default_storage.url(file_name)
            except:
                pass
            itemimage1=request.FILES.get("item_image1",None)
            try:
                file_name1 = default_storage.save(f'itemimages/{itemimage1.name}', itemimage1)
                imageurl=default_storage.url(file_name1)
            except:
                pass
            itemimage2=request.FILES.get("item_image2",None)
            try:
                file_name2 = default_storage.save(f'itemimages/{itemimage2.name}',itemimage2)
                imageurl1=default_storage.url(file_name2)
            except:
                pass
            r="level2"
        if "item_name3" in  level:
            level3=request.POST["item_name3"]
            ls.append(level3)
            itemcode=request.POST["item_code3"]
            itemdet=request.POST["item_det3"]
            itemuni=request.POST["item_u_code3"]
            itemspec=request.POST["item_spec3"]
            itembar=request.FILES.get("item_barcode1",None)
            try:

                file_name = default_storage.save(f'itemimages/{itembar.name}', itembar)
                barurl=default_storage.url(file_name)
            except:
                pass
            itemimage1=request.FILES.get("item_image1",None)
            try:
                file_name1 = default_storage.save(f'itemimages/{itemimage1.name}', itemimage1)
                imageurl=default_storage.url(file_name1)
            except:
                pass
            itemimage2=request.FILES.get("item_image2",None)
            try:
                file_name2 = default_storage.save(f'itemimages/{itemimage2.name}',itemimage2)
                imageurl1=default_storage.url(file_name2)
            except:
                pass
            r="level3"
        if "item_name4" in  level:
            level4=request.POST["item_name4"]
            ls.append(level4)
            itemcode=request.POST["item_code4"]
            itemdet=request.POST["item_det4"]
            itemuni=request.POST["item_u_code4"]
            itemspec=request.POST["item_spec4"]
            itembar=request.FILES.get("item_barcode1",None)
            try:
                file_name = default_storage.save(f'itemimages/{itembar.name}', itembar)
                barurl=default_storage.url(file_name)
            except:
                pass
            itemimage1=request.FILES.get("item_image1",None)
            try:
                file_name1 = default_storage.save(f'itemimages/{itemimage1.name}', itemimage1)
                imageurl=default_storage.url(file_name1)
            except:
                pass
            itemimage2=request.FILES.get("item_image2",None)
            try:
                file_name2 = default_storage.save(f'itemimages/{itemimage2.name}',itemimage2)
                imageurl1=default_storage.url(file_name2)
            except:
                pass
            r="level4"
        if "item_name5" in  level:
            level5=request.POST["item_name5"]
            ls.append(level5)
            itemcode=request.POST["item_code5"]
            itemdet=request.POST["item_det5"]
            itemuni=request.POST["item_u_code5"]
            itemspec=request.POST["item_spec5"]
            itembar=request.FILES.get("item_barcode1",None)
            try:
                file_name = default_storage.save(f'itemimages/{itembar.name}', itembar)
                barurl=default_storage.url(file_name)
            except:
                pass
            itemimage1=request.FILES.get("item_image1",None)
            try:
                file_name1 = default_storage.save(f'itemimages/{itemimage1.name}', itemimage1)
                imageurl=default_storage.url(file_name1)
            except:
                pass
            itemimage2=request.FILES.get("item_image2",None)
            try:
                file_name2 = default_storage.save(f'itemimages/{itemimage2.name}',itemimage2)
                imageurl1=default_storage.url(file_name2)
            except:
                pass
            r="level5"

        userorg=UserOrg.objects.all().filter(username=request.session["username"])
        if userorg:
            for i in userorg:
                o=i.org
                odata=json.loads(o)
            org=odata["organisations"]
            if ls[0] in org[0][r]["items"]:
                return HttpResponse('<style>body{background-color: rgba(0,0,0, 0.4);}.close-btn {position: absolute;bottom: 12px;right: 25px;}.content {position: absolute;width: 250px;height: 200px;background: #fff;top: 0%;left: 50%;transform: translate(-50%, -50%)scale(0.1);visibility: hidden;transition: transform 0.4s, top 0.4s;}.open-popup {visibility: visible;top: 50%;transform: translate(-50%, -50%)scale(1);}.header {height: 50px;background: #efea53;overflow: hidden;text-align: center;}p {padding-top: 40px;text-align: center;}</style><div class="content open-popup" id="popup"><div class="header"><h2>Alert!</h2></div><p>Item name <b> ' + ls[0] + '</b> <br> already exists..</p><div><button type="button" onclick="history.back();" class="close-btn">close</button></div></div>')
            else:
                org[0][r]["items"].append({"item_name":ls[0],"item_code":itemcode,"item_details":itemdet,"item_universal_code":itemuni,"item_specification":itemspec,"item_barcode":barurl,"item_image1":imageurl,"item_image2":imageurl1})
                #return HttpResponse(f'{org}')
                field={"document_name":request.session["username"]}
                update={"organisations":org}
                login=dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,update)
                return redirect(f'/?session_id={request.session["session_id"]}')
        else:
            return HttpResponse("no values")
def edititems(request):
        r=""
        ls=[]
    #try:
        level=request.POST.keys()
        if "item_name1" and "edit_item1" in level:
            level1=request.POST["item_name1"]
            editl=request.POST["edit_item1"]
            ls.append(level1)
            ls.append(editl)
            r="level1"
        if "item_name2" and "edit_item2" in level:
            level2=request.POST["item_name2"]
            edit2=request.POST["edit_item2"]
            ls.append(level2)
            ls.append(edit2)
            r="level2"
        if "item_name3" and "edit_item3" in level:
            level3=request.POST["item_name3"]
            edit3=request.POST["edit_item3"]
            ls.append(level3)
            ls.append(edit3)
            r="level3"
        if "item_name4" and "edit_item4" in level:
            level4=request.POST["item_name4"]
            edit4=request.POST["edit_item4"]
            ls.append(level4)
            ls.append(edit4)
            r="level4"
        if "item_name5" and "edit_item5" in level:
            level5=request.POST["item_name5"]
            edit5=request.POST["edit_item5"]
            ls.append(level5)
            ls.append(edit5)
            r="level5"
        userorg=UserOrg.objects.all().filter(username=request.session["username"])
        if userorg:
            for i in userorg:
                o=i.org
                odata=json.loads(o)
            org=odata["organisations"]
            if ls[1] in org[0][r]["items"]:
                return HttpResponse('<style>body{background-color: rgba(0,0,0, 0.4);}.close-btn {position: absolute;bottom: 12px;right: 25px;}.content {position: absolute;width: 250px;height: 200px;background: #fff;top: 0%;left: 50%;transform: translate(-50%, -50%)scale(0.1);visibility: hidden;transition: transform 0.4s, top 0.4s;}.open-popup {visibility: visible;top: 50%;transform: translate(-50%, -50%)scale(1);}.header {height: 50px;background: #efea53;overflow: hidden;text-align: center;}p {padding-top: 40px;text-align: center;}</style><div class="content open-popup" id="popup"><div class="header"><h2>Alert!</h2></div><p>Item name <b> ' + ls[0] + '</b> <br> already exists..</p><div><button type="button" onclick="history.back();" class="close-btn">close</button></div></div>')

            else:

                org[0][r]["items"]=[item.replace(ls[0], ls[1]) for item in org[0][r]["items"]]
                #return HttpResponse(f"old : {org1} <br> new :{org}")
                field={"document_name":request.session["username"]}
                update={"organisations":org}
                login=dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,update)
                return redirect(f'/?session_id={request.session["session_id"]}')
        else:
            return HttpResponse("no values")
def addroles(request):
    if request.method=="POST":
        level1=request.POST["level1"]
        level2=request.POST["level2"]
        level3=request.POST["level3"]
        level4=request.POST["level4"]
        level5=request.POST["level5"]
        security=request.POST["security"]

        role=request.POST["rolename"]
        role_code=request.POST["rolecode"]
        role_det=request.POST["role_det"]
        roleucode=request.POST["role_u_code"]
        role_spec=request.POST["role_spec"]
        userorg=UserOrg.objects.all().filter(username=request.session["username"])
        for i in userorg:
                o=i.org
                odata=json.loads(o)
        roles=odata["roles"]
        for checkroles in roles:
            if checkroles["role_name"]==role:
                return HttpResponse('<style>body{background-color: rgba(0,0,0, 0.4);}.close-btn {position: absolute;bottom: 12px;right: 25px;}.content {position: absolute;width: 250px;height: 200px;background: #fff;top: 0%;left: 50%;transform: translate(-50%, -50%)scale(0.1);visibility: hidden;transition: transform 0.4s, top 0.4s;}.open-popup {visibility: visible;top: 50%;transform: translate(-50%, -50%)scale(1);}.header {height: 50px;background: #efea53;overflow: hidden;text-align: center;}p {padding-top: 40px;text-align: center;}</style><div class="content open-popup" id="popup"><div class="header"><h2>Alert!</h2></div><p>Role name <b> ' + role + '</b> <br> already exists..</p><div><button type="button" onclick="history.back();" class="close-btn">close</button></div></div>')

        r={"level1_item":level1,"level2_item":level2,"level3_item":level3,"level4_item":level4,"level5_item":level5,"security_layer":security,"role_name":role,"role_code":role_code,"role_details":role_det,"role_uni_code":roleucode,"role_specification":role_spec}
        roles.append(r)
        #return HttpResponse(f'{roles}')
        field={"document_name":request.session["username"]}
        update={"roles":roles}
        login=dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,update)
        return redirect(f'/?session_id={request.session["session_id"]}')
def invitemembers(request):
    if request.method=="POST":
        email=request.POST["email"]
        org=request.POST["org"]
        member_type=""
        keys=request.POST.keys()
        if "team_members" in keys:
            member_type="team_members"
        if "guest_members" in keys:
            member_type="guest_members"
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
                                                <a href="#" style="font-size:32px;color:#fff;">DoWell UX Living Lab</a> <br>
                                                <span style="margin-top: 10px;display: block; color:yellow">Hi ,you have been invited by <b> {{brand}} </b>  to join in <b>{{brand}}</b>.</span>
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
                                                                Please click on the link below to Join.
                                                            </td>
                                                        </tr>
                                                        <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                            <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
                                                                <a href="https://100093.pythonanywhere.com/invitelink?org={{brand}}&email={{email}}&type={{team}}" class="btn-primary" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; color: #FFF; text-decoration: none; line-height: 2em; font-weight: bold; text-align: center; cursor: pointer; display: inline-block; border-radius: 5px; text-transform: capitalize; background-color: #f1556c; margin: 0; border-color: #f1556c; border-style: solid; border-width: 8px 16px;">
                                                Join</a> </td>
                                                </tr>
                                                <tr>
                                                <td> https://100093.pythonanywhere.com/invitelink?org={{brand}}&email={{email}}&type={{team}} You can also copy and paste this link to browser.

                                                            </td>
                                                        </tr>
                                                        <tr style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; margin: 0;">
                                                            <td class="content-block" style="font-family: 'Helvetica Neue',Helvetica,Arial,sans-serif; box-sizing: border-box; font-size: 14px; vertical-align: top; margin: 0; padding: 0 0 20px;" valign="top">
                                                                Thanks for choosing <b>DoWell UX Living Lab</b> .
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
        orgen = base64.b64encode(bytes(org, 'utf-8')) # bytes
        orgen1=orgen.decode("utf-8")
        type_en = base64.b64encode(bytes(member_type, 'utf-8')) # bytes
        type_en1=type_en.decode("utf-8")
        email_body = email_body.replace('{{brand}}',orgen1).replace('{{email}}',email).replace('{{team}}',type_en1)

        o=request.session["orgname"]
        subject=f'Invitation to Join {o}'
        from_email='dowelllogintest@gmail.com'
        to_email = email
        send_mail(subject, "lav", from_email, [email], fail_silently=False,html_message=email_body)
        field={"document_name":org}
        login=dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field,"nil")
        rl=json.loads(login)
        mydata=rl["data"][0]
        mymembers=mydata["members"]
        mymembers[member_type]["pending_members"].append({"email":email})

        field={"document_name":org}
        update={"members":mymembers}
        login=dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,update)
        return redirect(f'/?session_id={request.session["session_id"]}')
def invitelink(request):
    context={}
    import datetime
    org2=request.GET.get("org",None)
    email=request.GET.get("email",None)
    member_type2=request.GET.get("type",None)
    con=org2.encode("utf-8")
    base64_str = base64.b64decode(con)
    org=base64_str.decode("utf-8")
    con1=member_type2.encode("utf-8")
    base64_str1 = base64.b64decode(con1)
    member_type=base64_str1.decode("utf-8")
    context["org"]=org
    context["time"]=datetime.datetime.now()
    userfield={"Email":email}
    userresp=dowellconnection("login","bangalore","login","registration","registration","10004545","ABCDE","fetch",userfield,"nil")
    user=json.loads(userresp)
    myusers=[]

    for i in user["data"]:
        if i["Email"]==email:
            myusers.append(i["Username"])
    context["len"]=len(myusers)
    context["users"]=myusers
    if request.method=="POST":
        u=request.POST["username"]
        #try:
        userfield={"Username":u}
        use=dowellconnection("login","bangalore","login","registration","registration","10004545","ABCDE","fetch",userfield,"nil")
        us=json.loads(use)
        userna=us["data"][0]["Username"]
        first=us["data"][0]["Firstname"]
        last=us["data"][0]["Lastname"]
        email1=us["data"][0]["Email"]
        user_org={"org_name":org,"portfolio":[]}

        r={"name": userna, "first_name": first, "last_name": last, "email": email1}
        userorg=UserOrg.objects.all().filter(username=org)
        if userorg:
            for i in userorg:
                o=i.org
                odata=json.loads(o)
        mem=odata["members"]
        for checkusr in mem[member_type]["accept_members"]:
            if checkusr["name"]==u:
                return HttpResponse(f'<script>alert("You already exist in {org} organisation <br> go to home page");window.location.href = "https://100093.pythonanywhere.com";</script>')
            else:
                other_org=[]
                mem[member_type]["accept_members"].append(r)
                userorg1=UserOrg.objects.all().filter(username=u)
                if userorg1 is not None:
                    for i in userorg1:
                        o=i.org
                        odata=json.loads(o)
                        other_org=odata["other_organisation"]
                other_org.append(user_org)

                field={"document_name":org}
                update={"members":mem}
                login=dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,update)
                field1={"document_name":u}
                update1={"other_organisation":other_org}
                login1=dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field1,update1)
                return redirect("/")
        #except:
            #return HttpResponse("somethein wrong")
    return render(request,"email.html",context)
def addpublic(request):
    if request.method=="POST":
        number=request.POST["public"]
        br = base64.b64encode(bytes(request.session["present_org"], "utf-8")) # bytes
        brc=br.decode("utf-8")
        br1 = base64.b64encode(bytes(request.session["username"], "utf-8")) # bytes
        brc1=br1.decode("utf-8")
        for i in range(int(number)):
            code=passgen.generate_random_password1(7)
            path=f'https://100093.pythonanywhere.com/invitesocial?next={brc}&type=public_member&s={brc1}&code={code}'
            rt=publiclink.objects.create(link=path, linkcode=code,dateof=datetime.datetime.now(),org=request.session["present_org"],username=request.session["username"],linkstatus="unused",productstatus="unused")

        return redirect(f'/?session_id={request.session["session_id"]}')
def invitesocial(request):
    context={}
    mtype=request.GET.get("type",None)
    if mtype=="public_member":

        org1=request.GET.get("next",None)
        con=org1.encode("utf-8")
        base64_str = base64.b64decode(con)
        org=base64_str.decode("utf-8")
        code=request.GET.get("code",None)
        username1=request.GET.get("s",None)
        base64_str1 = base64.b64decode(username1)
        username=base64_str1.decode("utf-8")
        url=request.GET.get("redirect_url",None)
        path=request.build_absolute_uri()
        if request.method == 'POST':
            loc=request.POST["loc"]
            device=request.POST["dev"]
            osver=request.POST["os"]
            brow=request.POST["brow"]
            ltime=request.POST["time"]
            ipuser=request.POST["ip"]
            mobconn=request.POST["conn"]
            r=UserOrg.objects.all().filter(username=org)
            for i in r:
                userorg=i.org
                usero=json.loads(userorg)
            if usero["document_name"]==org:
                orl=publiclink.objects.all().filter(linkcode=code,username=username,linkstatus="unused")
                if orl:
                    user=passgen.generate_random_password1(12)
                    userorgs=usero["members"]
                    userorgs["public_members"]["accept_members"].append({"username":user,"link":path,"qrcodeid":user,"product_status":"enable","status":"enable"})
                    field={"document_name":usero["document_name"]}
                    update={"members":userorgs}
                    login=dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,update)
                    field1={"Username":user,"OS":osver,"Device":device,"Browser":brow,"Location":loc,"Time":str(ltime),"SessionID":"linkbased","Connection":mobconn,"qrcode_id":user,"IP":ipuser}
                    qrcodegen.qrgen1(user,user,f"clientadmin/media/userqrcodes/{user}.png")
                    orl.update(qrcodeid=user,linkstatus="used",other=json.dumps(field1))
                    context["org"]=usero["document_name"]
                    return render(request,"social.html",context)
                else:
                    #rt=publiclink.objects.create(link=path, linkcode=code,dateof=datetime.datetime.now(),org=org,username=username,other=json.dumps(field))
                    context["org"]=org
                    return HttpResponse('<h1 align="center">Link is already used</h1>')
            return HttpResponse('<h1 align="center">Unknown Link</h1>')
    else:
        return HttpResponse(f'<h1 align="center">Link is modified give proper link</h1>')
    return render(request,"linkbased.html",context)
    #return render(request,"social.html",context)
def addportfolio(request):
    if request.method=="POST":
        member_type=request.POST["member_type"]
        member_name=request.POST["member"]
        product=request.POST["product"]
        data_type=request.POST["data_type"]
        oprights=request.POST["op_rights"]
        role=request.POST["role"]
        portfolio=request.POST["portfolio_name"]
        pcode=request.POST["portfolio_code"]
        pdet=request.POST["portfolio_det"]
        pucode=request.POST["portfolio_u_code"]
        pspec=request.POST["portfolio_spec"]
        userorg=UserOrg.objects.all().filter(username=request.session["username"])
        for i in userorg:
                o=i.org
                odata=json.loads(o)
        ortname=odata["document_name"]
        portls=odata["portpolio"]
        for portcheck in portls:
            if portcheck["portfolio_name"]==portfolio:
                return HttpResponse('<style>body{background-color: rgba(0,0,0, 0.4);}.close-btn {position: absolute;bottom: 12px;right: 25px;}.content {position: absolute;width: 250px;height: 200px;background: #fff;top: 0%;left: 50%;transform: translate(-50%, -50%)scale(0.1);visibility: hidden;transition: transform 0.4s, top 0.4s;}.open-popup {visibility: visible;top: 50%;transform: translate(-50%, -50%)scale(1);}.header {height: 50px;background: #efea53;overflow: hidden;text-align: center;}p {padding-top: 40px;text-align: center;}</style><div class="content open-popup" id="popup"><div class="header"><h2>Alert!</h2></div><p>Portfolio name <b> ' + portfolio + '</b> <br> already exists..</p><div><button type="button" onclick="history.back();" class="close-btn">close</button></div></div>')

        portls.append({"username": member_name, "member_type": member_type, "product": product, "data_type": data_type, "operations_right": oprights, "role": role, "security_layer": "None", "portfolio_name": portfolio,"portfolio_code":pcode,"portfolio_details":pdet,"portfolio_uni_code":pucode,"portfolio_specification":pspec,"status":"enable"})
        #return HttpResponse(f'{portls}')
        field={"document_name":request.session["username"]}
        update={"portpolio":portls}
        login=dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,update)

        field1={"document_name":member_name}
        login1=dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field1,"update")
        r=json.loads(login1)
        try:
            lo=r["data"][0]["other_organisation"]

            lo.append({"org_name":ortname,"username": member_name, "member_type": member_type, "product": product, "data_type": data_type, "operations_right": oprights, "role": role, "security_layer": "None", "portfolio_name": portfolio,"portfolio_code":pcode,"portfolio_details":pdet,"portfolio_uni_code":pucode,"portfolio_specification":pspec,"status":"enable"})

            field={"document_name":member_name}
            update={"other_organisation":lo}
            login2=dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,update)
        except:
            pass
        return redirect(f'/?session_id={request.session["session_id"]}')
def otherorg(request):
    if request.session.get("username"):
        username=request.session['username']
        if request.method=="POST":
            context={}

            org=request.POST["org"]
            user_org=UserOrg.objects.all().filter(username=username)
            for it in user_org:
                    data12=it.org
                    data13=json.loads(data12)
            if request.session["username"]==org:
                return redirect(f"/?session_id={request.session['session_id']}")
            else:
                userorg=UserInfo.objects.all().filter(username=username)
                for i in userorg:
                    data1=i.userinfo
                    data=json.loads(data1)
                #return HttpResponse(f'{data}')
                request.session["present_org"]=org
                context["img"]=data13["profile_info"]["profile_img"]
                # context["first"]=data["userinfo"]["Firstname"]
                # context["last"]=data["userinfo"]["Lastname"]
                context["time"]=data["dowell_time"]
                context["location"]=data["city"]
                userorg=UserOrg.objects.all().filter(username=username)
                for i in userorg:
                    dataorg=i.org
                    dataorg1=json.loads(dataorg)
                ors=[]
                for lsr in dataorg1["organisations"]:
                    ors.append(lsr["org_name"])
                for lst in dataorg1["other_organisation"]:
                    ors.append(lst["org_name"])
                co=[]
                po=[]
                for i in dataorg1["other_organisation"]:
                    if i["org_name"]==org:
                        try:
                            co.append(i["product"])
                            if "disab" in i["status"]:
                                pass
                            else:
                                po.append(i["portfolio_name"])
                        except:
                            pass
                # userorg1=UserOrg.objects.all().filter(username=org)
                # for i in userorg1:
                #     datap=i.org
                #     datapro=json.loads(datap)
                # for ii in datapro["portpolio"]:
                #     if username in ii["username"]:
                #         co.append(ii["product"])
                # for i in userorg1:
                #     datap=i.org
                #     datapro=json.loads(datap)
                # for ii in dataorg1["other_organisation"]:
                #     if org in ii["org_name"]:
                #         ro=ii["portfolio"]
                context["aiport"]=[*set(po)]
                context["myorg"]=[*set(ors)]
                context["products"]=[*set(co)]
                return render(request,"other.html",context)
def disablep(request):
    if request.method=="POST":
        username=request.session['username']
        po=request.POST["portfolio"]
        st=request.POST["status"]
        if po=="default" or po=="owner":
            return HttpResponse('<style>body{background-color: rgba(0,0,0, 0.4);}.close-btn {position: absolute;bottom: 12px;right: 25px;}.content {position: absolute;width: 250px;height: 200px;background: #fff;top: 0%;left: 50%;transform: translate(-50%, -50%)scale(0.1);visibility: hidden;transition: transform 0.4s, top 0.4s;}.open-popup {visibility: visible;top: 50%;transform: translate(-50%, -50%)scale(1);}.header {height: 50px;background: #efea53;overflow: hidden;text-align: center;}p {padding-top: 40px;text-align: center;}</style><div class="content open-popup" id="popup"><div class="header"><h2>Alert!</h2></div><p>Portfolio name is <b> ' + po + '</b> you can not disable/enable it<br> ..</p><div><button type="button" onclick="history.back();" class="close-btn">close</button></div></div>')
        userorg=UserOrg.objects.all().filter(username=username)
        for i in userorg:
            dataorg=i.org
            dataorg1=json.loads(dataorg)
        rot=dataorg1["portpolio"]
        for ir in rot:
            if ir["portfolio_name"]==po:
                username1=ir["username"]
                ir["status"]=st

        #return HttpResponse(f'<h1 align="center">Page under maintainance pl wait {po} {rot}.......<h4> {username1}')
        field={"document_name":request.session["username"]}
        update={"portpolio":rot}
        login=dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,update)
        field1={"document_name":username1}
        login1=dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field1,"update")
        r=json.loads(login1)
        lo=r["data"][0]["other_organisation"]
        raj="raj"
        for irm in lo:
            try:
                if irm["portfolio_name"]==po:
                    irm["status"]=st
                    raj="raju"
            except:
                pass
        if raj=="raju":
            field={"document_name":username1}
            update={"other_organisation":lo}
            login2=dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,update)
            return redirect(f'/?session_id={request.session["session_id"]}')
        else:
            return HttpResponse('<style>body{background-color: rgba(0,0,0, 0.4);}.close-btn {position: absolute;bottom: 12px;right: 25px;}.content {position: absolute;width: 250px;height: 200px;background: #fff;top: 0%;left: 50%;transform: translate(-50%, -50%)scale(0.1);visibility: hidden;transition: transform 0.4s, top 0.4s;}.open-popup {visibility: visible;top: 50%;transform: translate(-50%, -50%)scale(1);}.header {height: 50px;background: #efea53;overflow: hidden;text-align: center;}p {padding-top: 40px;text-align: center;}</style><div class="content open-popup" id="popup"><div class="header"><h2>Alert!</h2></div><p>Something wrong try again<br> ..</p><div><button type="button" onclick="history.back();" class="close-btn">close</button></div></div>')

def Logout(request):
    d=request.session.get("session_id")
    #return HttpResponse(d)
    #equest.session.modified = True
    if d:
        try:
            del request.session["username"]
            del request.session["present_org"]
            del request.session["orgname"]
            del request.session["session_id"]
            return redirect("https://100014.pythonanywhere.com/sign-out")
        except:
            return redirect("https://100014.pythonanywhere.com/sign-out")
    else:
        return redirect("https://100014.pythonanywhere.com/sign-out")
# def testing(request):
#     if request.method="POST":
#         level=request.POST["itemname"]
#     return HttpResponse(level)


def Layers(request):
    if request.method == "POST" and "devicelayersetbtn" in request.POST:
        username=request.session['username']
        dict = {"laptop":request.POST.get('form_fields[laptoplayer]'),"phone":request.POST.get('form_fields[phonelayer]'),"tablet":request.POST.get('form_fields[tabletlayer]'),"others":request.POST.get('form_fields[otherdevicelayer]')}
        # print(username)
        obj, created = Devices.objects.update_or_create(username=username,defaults={'data': json.dumps(dict)})
    if request.method == "POST" and "oslayersetbtn" in request.POST:
        username=request.session['username']
        dict = {"windows":request.POST.get('form_fields[windowslayer]'),"macos":request.POST.get('form_fields[maclayer]'),"linux":request.POST.get('form_fields[linuxlayer]'),"android":request.POST.get('form_fields[androidlayer]'),"ios":request.POST.get('form_fields[iossecuritylayer]'),"others":request.POST.get('form_fields[otherslayeros]')}
        # print(username)
        obj, created = OperatingSystems.objects.update_or_create(username=username,defaults={'data': json.dumps(dict)})
    if request.method == "POST" and "browserlayersetbtn" in request.POST:
        username=request.session['username']
        dict = {"chrome":request.POST.get('form_fields[chromelayer]'),"safari":request.POST.get('form_fields[safarilayer]'),"bing":request.POST.get('form_fields[binglayer]'),"firefox":request.POST.get('form_fields[firefoxlayer]'),"edge":request.POST.get('form_fields[edgelayer]'),"opera":request.POST.get('form_fields[operalayer]'),"others":request.POST.get('form_fields[otherslayerbrowser]')}
        # print(username)
        obj, created = Browsers.objects.update_or_create(username=username,defaults={'data': json.dumps(dict)})
    if request.method == "POST" and "internetlayersetbtn" in request.POST:
        username=request.session['username']
        dict = {"mobiledata":request.POST.get('form_fields[mobiledatalayer]'),"officewifi":request.POST.get('form_fields[securedwifilayer]'),"publicwifi":request.POST.get('form_fields[publicwifilayer]'),"others":request.POST.get('form_fields[otherslayerinternet]')}
        # print(username)
        obj, created = InternetConnection.objects.update_or_create(username=username,defaults={'data': json.dumps(dict)})
    if request.method == "POST" and "passwordlayersetbtn" in request.POST:
        username=request.session['username']
        dict = {"chars8":request.POST.get('form_fields[password8loginlayer]'),"chars10":request.POST.get('form_fields[password10loginlayer]'),"chars12":request.POST.get('form_fields[password12loginayer]'),"chars16":request.POST.get('form_fields[password16loginlayer]'),"others":request.POST.get('form_fields[otherslayerpassword]')}
        # print(username)
        obj, created = PasswordStrength.objects.update_or_create(username=username,defaults={'data': json.dumps(dict)})
    if request.method == "POST" and "logintypelayersetbtn" in request.POST:
        username=request.session['username']
        dict = {"userpass":request.POST.get('form_fields[textloginlayer]'),"faceid":request.POST.get('form_fields[faceidloginlayer]'),"voiceid":request.POST.get('form_fields[voiceidloginayer]'),"biometric":request.POST.get('form_fields[biometricloginlayer]'),"videoid":request.POST.get('form_fields[videoIDlayer]'),"others":request.POST.get('form_fields[otherslayerlogintype]')}
        # print(username)
        obj, created = LoginType.objects.update_or_create(username=username,defaults={'data': json.dumps(dict)})
    if request.method == "POST" and "verifiedIDlayersetbtn" in request.POST:
        username=request.session['username']
        dict = {"verifiedid":request.POST.get('form_fields[verifiedIDlayer]'),"notverifiedid":request.POST.get('form_fields[notverifiedIDlayer]'),"phoneverified":request.POST.get('form_fields[verifiedphonelayer]'),"phonenotverified":request.POST.get('form_fields[notverifiedphonelayer]'),"verifiedemail":request.POST.get('form_fields[verifiedemaillayer]'),"notverifiedemail":request.POST.get('form_fields[notverifiedemaillayer]'),"others":request.POST.get('form_fields[otherslayerverifiedID]')}
        # print(username)
        obj, created = IdVerification.objects.update_or_create(username=username,defaults={'data': json.dumps(dict)})

    
    return redirect(f'/?session_id={request.session["session_id"]}')


def GeoSetting(request):
    if request.method == "POST" and "geosetting" in request.POST:
        print(request.POST.get("AUS"))

    return redirect(f'/?session_id={request.session["session_id"]}')
