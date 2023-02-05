from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from clientadminapp.models import UserData,UserOrg,Devices,Browsers,IdVerification,InternetConnection,OperatingSystems,LoginType,PasswordStrength
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