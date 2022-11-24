from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
from .login import get_user_profile
import requests


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        username = request.session.get('username')
        # jwt = request.session.get('jwt_value')
        if username is None:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')
    
    return wrapper_func


def loginrequired(view_func):
    def wrapper_func(request, *args, **kwargs):
        username = request.session.get('username')
        # jwt = request.session.get('jwt_value')
        if username is None:
            return redirect('loginuser')
        return view_func(request, *args, **kwargs)
    return wrapper_func
    

# def api(view_func):
#     def wrapper_func(request, *args, **kwargs):
#         username = request.session.get('username')
#         # jwt = request.session.get('jwt_value')
#         if username is None:
#             return redirect('loginuser')
#         return view_func(request, *args, **kwargs)
#     return wrapper_func

def authenticationrequired(view_func):
    def wrapper_func(request, *args, **kwargs):
        usersurl="http://100014.pythonanywhere.com/api/users/"
        key = request.GET.get('session_id', '')
        request.session['session_id'] = key
        # print("Key is "+ key)
        if key == '':
            return HttpResponseRedirect("https://100014.pythonanywhere.com/")

        try:
            user = get_user_profile(key)
            # print(user)
            s = requests.session()
            users = s.get(usersurl)
            users = users.text
            request.session['current_user'] = user
            # print(users)
            # if user['role'] == 'User':
            #     return HttpResponse("Your Role Does Not Have Permission To Access Admin Panel. Please Login with Authorized Credentials <a href ='https://100014.pythonanywhere.com/'> Here </a>")
        except ValueError:
            return HttpResponseRedirect("https://100014.pythonanywhere.com/")
        return view_func(request, *args, **kwargs)
    return wrapper_func


def is_super_admin(view_func):
    def wrapper_func(request, *args, **kwargs):
        key = request.session.get('session_id')
        user = get_user_profile(key)
        # jwt = request.session.get('jwt_value')
        if user['role'] == 'Admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('access_denied')
    
    return wrapper_func

def is_client_admin(view_func):
    def wrapper_func(request, *args, **kwargs):
        # key = request.GET.get('session_id', '')
        key = request.session.get('session_id')
        user = get_user_profile(key)
        # jwt = request.session.get('jwt_value')
        if user['role'] == 'client_admin':
            return view_func(request, *args, **kwargs)
        else:
            return redirect('access_denied')
    
    return wrapper_func



def is_client_and_super_admin(view_func):
    def wrapper_func(request, *args, **kwargs):
        # key = request.GET.get('session_id', '')
        key = request.session.get('session_id')
        user = get_user_profile(key)
        # jwt = request.session.get('jwt_value')
        if 'client_admin' in user['role'] or 'Admin' in user['role']:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('access_denied')
    
    return wrapper_func