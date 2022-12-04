
from django.shortcuts import render,HttpResponse
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse
# Create your views here.
from rest_framework.response import Response
import json
from rest_framework.views import APIView
from client_admin.dowellconnection import dowellconnection 
import jwt
import datetime
from client_admin.decorators import authenticationrequired, is_client_admin, is_client_and_super_admin, is_super_admin, loginrequired, unauthenticated_user
from client_admin.login import get_user_profile
from client_admin_new.models import ClientAdmin
from django.core import serializers



class CompanyView(APIView):


    def get_jwt(self,request):
        key = request.GET.get('session_id', '')
        # print("Key is "+ key)
        if key == '':
            return HttpResponseRedirect("https://100014.pythonanywhere.com/")

        user = get_user_profile(key)        
        print(user)
        if user is None:
            return JsonResponse({"msg":"not allowed"})
        payload={
            'id':user["username"],
            'exp':datetime.datetime.utcnow()+datetime.timedelta(minutes=60),
            'iat':datetime.datetime.utcnow()
            }
        token=jwt.encode(payload,'dowell_secret',algorithm='HS256')
        # token = jwt.encode({"some": "payload"}, "secret", algorithm="HS256")
        print(token)
        response=Response()
        response.set_cookie(key="jwt", value=token)
        response.data={
            'jwt':token
            }
        return response

    def get(self,request):
        r  = self.get_jwt(request)
        if r is not None:
            field ={}
            companies = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","fetch",field,"nil")
            companies = json.loads(companies)
            return Response(companies)   
        return JsonResponse({"msg":"not allowed"})
    def post(self,request):
        a = request.data

        return Response(a)
        # field_add ={a}
        # companies = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","insert",field_add,"nil")
        # companies = json.loads(companies)
        # return Response(companies)      

class OrganisationView(APIView):
    def get(self,request):
        field ={}
        organisations = dowellconnection("login","bangalore","login","organization","organization","1084","ABCDE","fetch",field,"nil")
        organisations = json.loads(organisations)
        return Response(organisations)        
    def post(self,request):
        a = request.data
        return Response(a)
        # field_add ={a}
        # companies = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","insert",field_add,"nil")
        # companies = json.loads(companies)
        # return Response(companies)      


class DepartmentView(APIView):
    def get(self,request):
        field ={}
        departments = dowellconnection("login","bangalore","login","department","department","1085","ABCDE","fetch",field,"nil")
        departments = json.loads(departments)
        return Response(departments)        
    def post(self,request):
        a = request.data
        return Response(a)
        # field_add ={a}
        # companies = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","insert",field_add,"nil")
        # companies = json.loads(companies)
        # return Response(companies)     


class ProjectView(APIView):
    def get(self,request):
        field ={}
        projects = dowellconnection("login","bangalore","login","project","project","1086","ABCDE","fetch",field,"nil")
        projects = json.loads(projects)
        return Response(projects)        
    def post(self,request):
        a = request.data
        return Response(a)
        # field_add ={a}
        # companies = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","insert",field_add,"nil")
        # companies = json.loads(companies)
        # return Response(companies)     


class DeviceView(APIView):
    def get(self,request):
        field ={}
        devices = dowellconnection("login","bangalore","login","devices","devices","1106","ABCDE","fetch",field,"nil")
        devices = json.loads(devices)
        return Response(devices)        
    def post(self,request):
        a = request.data
        return Response(a)
        # field_add ={a}
        # companies = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","insert",field_add,"nil")
        # companies = json.loads(companies)
        # return Response(companies)     

class LocationView(APIView):
    def get(self,request):
        field ={}
        ocations = dowellconnection("login","bangalore","login","locations","locations","1107","ABCDE","fetch",field,"nil")
        locations = json.loads(locations)
        return Response(locations)        
    def post(self,request):
        a = request.data
        return Response(a)
        # field_add ={a}
        # companies = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","insert",field_add,"nil")
        # companies = json.loads(companies)
        # return Response(companies)     


class OsView(APIView):
    def get(self,request):
        field ={}
        oses = dowellconnection("login","bangalore","login","os","os","1108","ABCDE","fetch",field,"nil")
        oses = json.loads(oses)
        return Response(oses)        
    def post(self,request):
        a = request.data
        return Response(a)
        # field_add ={a}
        # companies = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","insert",field_add,"nil")
        # companies = json.loads(companies)
        # return Response(companies)     


class ConnectionView(APIView):
    def get(self,request):
        field ={}
        connections = dowellconnection("login","bangalore","login","connections","connections","1110","ABCDE","fetch",field,"nil")
        connections = json.loads(connections)
        return Response(connections)        
    def post(self,request):
        a = request.data
        return Response(a)
        # field_add ={a}
        # companies = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","insert",field_add,"nil")
        # companies = json.loads(companies)
        # return Response(companies)     


class BrowserView(APIView):
    def get(self,request):
        field ={}
        browsers = dowellconnection("login","bangalore","login","browsers","browsers","1109","ABCDE","fetch",field,"nil")
        browsers = json.loads(browsers)
        return Response(browsers)        
    def post(self,request):
        a = request.data
        return Response(a)
        # field_add ={a}
        # companies = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","insert",field_add,"nil")
        # companies = json.loads(companies)
        # return Response(companies)     

class ProcessView(APIView):
    def get(self,request):
        field ={}
        processes = dowellconnection("login","bangalore","login","processes","processes","1111","ABCDE","fetch",field,"nil")
        processes = json.loads(processes)
        return Response(processes)        
    def post(self,request):
        a = request.data
        return Response(a)
        # field_add ={a}
        # companies = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","insert",field_add,"nil")
        # companies = json.loads(companies)
        # return Response(companies)  



class YoutubeplaylistView(APIView):
    def get(self,request):
        field ={}
        playlists = dowellconnection("login","bangalore","login","youtube_playlist","youtube_playlist","1112","ABCDE","fetch",field,"nil")
        playlists = json.loads(playlists)
        return Response(playlists)        
    def post(self,request):
        a = request.data
        return Response(a)
        # field_add ={a}
        # companies = dowellconnection("login","bangalore","login","company","company","1083","ABCDE","insert",field_add,"nil")
        # companies = json.loads(companies)
        # return Response(companies)  


class Organisations(APIView):
    def get(self,request):
        organisations = list(ClientAdmin.objects.values_list('organisations',flat=True))
        print(organisations)
        # organisations = organisations_
        # data = serializers.serialize('json', organisations)

        return JsonResponse({"organisations":organisations},safe=False)
        # return HttpResponse(data, content_type='application/json')


class Profile(APIView):
    def get(self,request):
        profile = list(ClientAdmin.objects.values_list('profile',flat=True))
        # print(organisations)
        # organisations = organisations_
        # data = serializers.serialize('json', organisations)

        return JsonResponse({"profile":profile},safe=False)

class Members(APIView):
    def get(self,request):
        members = list(ClientAdmin.objects.values_list('members',flat=True))
        # print(organisations)
        # organisations = organisations_
        # data = serializers.serialize('json', organisations)

        return JsonResponse({"members":members},safe=False)
