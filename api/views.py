from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from clientadminapp.models import UserData,UserOrg,Devices,Browsers,IdVerification,InternetConnection,OperatingSystems,LoginType,PasswordStrength,publiclink
from clientadminapp.dowellconnection import dowellconnection,loginrequired
from django.http import HttpResponse


import json
@api_view(["POST"])
def sessionView(request):
    mdata=request.data
    s=mdata["session_id"]
    ro1=UserData.objects.all().filter(sessionid=s)
    for i in ro1:
        r=i.alldata
        rj=json.loads(r)
    return Response(rj)
@api_view(["POST"])
def OrgsView(request):
    mdata=request.data
    org=mdata["org"]
    sec=mdata["scode"]
    #return Response({"msg":"ok"})
    if sec=="DoWell$0987":

        ro1=UserOrg.objects.all().filter(username=org)
        if ro1:
            for i in ro1:
                r=i.org
                rj=json.loads(r)
            return Response(rj)
        else:
            return Response({"message":"this org details not found"})
@api_view(["POST"])
def OrgView(request):
    mdata=request.data
    un=mdata["org_id"]
    ro1=UserOrg.objects.all()
    for i in ro1:
        rl=i.org
        rol=json.loads(rl)
        for ii in rol:
            try:
                if ii["_id"]==un:
                    rj=rol
            except:
                pass
    members=rj["members"]
    portl=rj["portpolio"]
    return Response({"members":members,"portfolio":portl})


@api_view(["GET"])
def DeviceLayers(request):

    ro1=Devices.objects.all()
    return Response({"data":json.loads(ro1[0].data)})


@api_view(["GET"])
def OsLayers(request):

    ro1=OperatingSystems.objects.all()
    return Response({"data":json.loads(ro1[0].data)})


@api_view(["GET"])
def BrowserLayers(request):

    ro1=Browsers.objects.all()
    return Response({"data":json.loads(ro1[0].data)})


@api_view(["GET"])
def ConnectionLayers(request):

    ro1=InternetConnection.objects.all()
    return Response({"data":json.loads(ro1[0].data)})

@api_view(["GET"])
def LoginLayers(request):

    ro1=LoginType.objects.all()
    return Response({"data":json.loads(ro1[0].data)})


@api_view(["GET"])
def IdVerificationLayers(request):

    ro1=IdVerification.objects.all()
    return Response({"data":json.loads(ro1[0].data)})


@api_view(["GET"])
def PasswordLayers(request):

    ro1=PasswordStrength.objects.all()
    return Response({"data":json.loads(ro1[0].data)})

@api_view(["POST"])
def GetPort(request):
    odata = request.data
    org = odata["org"]
    r1 = []
    if "portfolio" in odata.keys():
        print("first")
        port = odata["portfolio"]
        field1={"document_name":org}
        login1=dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field1,"update")
        r=json.loads(login1)
        
        for p in r["data"][0]["portpolio"]:
            if port in p["portfolio_name"]:
                r1.append(p)
            # else:
            #     return Response({"msg":"portfolio not found"})
    if "product" in odata.keys() and "portfolio" in odata.keys():
        r1.clear()
        print("second")
        port = odata["portfolio"]
        product = odata["product"]
        field1={"document_name":org}
        login1=dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field1,"update")
        r=json.loads(login1)
        r1 = []
        for p in r["data"][0]["portpolio"]:
            if p["portfolio_name"] == port and p["product"] == product:
                r1.append(p)
            # else:
            #     return Response({"msg":"portfolio not found"})

    else:
        field1={"document_name":org}
        login1=dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field1,"update")
        r=json.loads(login1)
        r1 = r["data"]

    return Response({"portfolio":r1})

@api_view(["POST"])
def userinfo(request):
    odata = request.data
    user = odata["user"]
    field1={"document_name":user}
    login1=dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field1,"update")
    r=json.loads(login1)
    r1 = r["data"]
    return Response({"data":r1})

@api_view(["POST"])
def UpdateQr(request):
    odata = request.data
    org = odata["org"]
    product = odata["product"]
    qrid = odata["qrcodeid"]
    q = {}
    field1={"document_name":org}
    l1=dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","fetch",field1,"update")
    l1 = json.loads(l1)
    members = l1["data"][0]["members"]
    print(members)
    q["qrcodeid"] = qrid
    # members["public_members"]["accept_members"].append(q)
    # print(members)
    for i in members["public_members"]["pending_members"]:
        if i.name == qrid:
            i.productstatus = "used"
            i.product = product
    field={"document_name":org}
    update={"members":members}
    # l2=dowellconnection("login","bangalore","login","client_admin","client_admin","1159","ABCDE","update",field,update)
    try:
        obj = publiclink.objects.filter(username = org,qrcodeid = qrid)
        for i in obj:
            # i.linkstatus = "used"
            i.productstatus = "used"
            i.save()
        print(obj)
    except:
        Response({"msg":"not found"})

    return Response({"msg":members})
