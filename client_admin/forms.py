from django import forms
from django.core.exceptions import ValidationError
from django.contrib.sessions.backends.db import SessionStore
from django.shortcuts import render, HttpResponse
from django.views import View


class RegisterClient(forms.Form):
    choice_designation = [('User','User'),('TeamMember','TeamMember'),('Company_lead','Company_lead'),('Organisation_lead','Organisation_lead'),('Department_lead','Department_lead'),('Project_lead','Project_lead')]


    role = forms.CharField(required = False, label='Role :', widget=forms.Select(choices=choice_designation,attrs={'class': "form-control"}))
    teamcode = forms.FloatField(widget=forms.TextInput(attrs={'class': "form-control"}))
    first_name = forms.CharField(required = False,label='First Name :',max_length = 20,widget=forms.TextInput(attrs={'class': "form-control"}))
    last_name = forms.CharField(required = False,label='Last Name :',max_length = 20,widget=forms.TextInput(attrs={'class': "form-control"}))
    username = forms.CharField(required = False,label='Username :',max_length = 20, widget=forms.TextInput(attrs={'class': "form-control"}))
    email = forms.EmailField(required = False,label='Email :',widget=forms.TextInput(attrs={'class': "form-control"}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': "form-control"})) 
    phonecode = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control"})) 
    phone = forms.IntegerField(widget=forms.NumberInput(attrs={'class': "form-control"})) 
    # profilepic      = forms.FileField(required=False) 


class LoginClient(forms.Form):
    loginusername = forms.CharField(required = False,label='Username :',max_length = 20)
    loginpassword = forms.CharField(label='Password :',max_length = 20, widget=forms.PasswordInput) 
    device = forms.CharField(widget=forms.HiddenInput())
    location = forms.CharField(widget=forms.HiddenInput())
    useros = forms.CharField(widget=forms.HiddenInput())
    browser = forms.CharField(widget=forms.HiddenInput())
    usertime = forms.CharField(widget=forms.HiddenInput())
    conn = forms.CharField(widget=forms.HiddenInput())
    userip = forms.CharField(widget=forms.HiddenInput())


class AddCompany(forms.Form):
    company = forms.CharField(required = True,label='Company :',max_length = 20,widget=forms.TextInput(attrs={'class': "form-control",'placeholder': 'Company'}) )


class EditCompany(forms.Form):
    company = forms.CharField(required = True,label='Company :',max_length = 20,widget=forms.TextInput(attrs={'class': "form-control",'placeholder': 'Company'}) )

class AddOrganisation(forms.Form):
    choices_company = []
    organisation = forms.CharField(required = True,label='Organisation :',max_length = 20,widget=forms.TextInput(attrs={'class': "form-control",'placeholder': 'Organisation'}) )


class AddDepartment(forms.Form):
    choices_company = []
    department = forms.CharField(required = True,label='Departmenet :',max_length = 20,widget=forms.TextInput(attrs={'class': "form-control",'placeholder': 'Department'}) )


class AddProject(forms.Form):
    choices_company = []
    project = forms.CharField(required = True,label='Project :',max_length = 20,widget=forms.TextInput(attrs={'class': "form-control",'placeholder': 'Project'}) )
    #CPunit1=forms.CharField(label='Unit', widget=forms.RadioSelect(choices=CHOICESCP, attrs={'class': ''}))

    # pressure = forms.FloatField()
    # PSunit= forms.CharField(label='pressure Unit :', widget=forms.Select(choices=CHOICESPS))

    # #PSunit1=forms.CharField(label='Unit', widget=forms.RadioSelect(choices=CHOICESPS, attrs={'class': ''}), )

    # efficiency = forms.FloatField()

    # rpm =  forms.FloatField(required = False, initial=1440)
    # temperature = forms.FloatField(required = False,initial=40)
    # fosp = forms.CharField(required = False, label='FOSP :',initial= '1.1', widget=forms.Select(choices=safety_factor) )
    # fosod = forms.CharField(required = False,label='FOSOD :',initial= '1.1', widget=forms.Select(choices=safety_factor))
    # fan_inlet_velocity = forms.FloatField(required = False,initial=35)
    # fan_outlet_velocity = forms.FloatField(required = False,initial=20)