# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render , HttpResponse ,redirect
import datetime
from forms import signedup , login_form
from models import user_details ,session_token
from django.contrib.auth.hashers import make_password ,check_password
# Create your views here.


def sign_up(request):
    today=datetime.datetime.now()
    if request.method=='GET':
        signedup_obj = signedup()
    elif request.method=='POST':
        print 'POST called'
        signedup_obj=signedup(request.POST)

        if signedup_obj.is_valid():
            name = signedup_obj.cleaned_data.get('name') #.get('name')
            print name
            username=signedup_obj.cleaned_data.get('username') #.get('username')
            mail=signedup_obj.cleaned_data.get('email')  #.get('email')
            password=signedup_obj.cleaned_data.get('password')   #.get('password')
            user=user_details(name=name,username=username,password=make_password(password),email=mail)
            user.save()
            return  render(request,'sign_up_succes.html')
        else:
            print 'Validation failed'
    return render(request, 'sign_up.html',{'today':today,'signed_obj':signedup_obj})

def login(request):
    if request.method=='GET':
        login=login_form()

    if request.method=='POST':
        login=login_form(request.POST)
        print 'post called'
        if login.is_valid():
            print 'login valid'
            username=login.cleaned_data.get('username')
            password=login.cleaned_data.get('password')
            print username
            user=user_details.objects.filter(username=username).first()
            print user
            if user:
                if check_password(password,user.password):
                    print 'user valid'
                    token=session_token(username=user)
                    token.create_token()
                    token.save()
                    print token
                    response = redirect('/feed/')
                    print response
                    response.set_cookie(key='session_token', value=token.token)
                    print 'cookie set'
                    return response

        else :
                    print ' user invalid'
                    return render(request, 'Login.html',{'login':login})

    return render(request, 'Login.html',{'login':login})


def check_validation(request):
    if request.COOKIES.get('session_token'):
        session=session_token.objects.filter(token=request.COOKIES.get('session_token')).first()
        if session:
            return session.username
    else:
        return None


def feed(request):
    print 'feed called'
    user=check_validation(request)
    if user:
        print 'authentic user'
    else :
        print 'user not logged in'
        return redirect('/login/')

    return render(request, 'feed.html')

def upload(request):
    print 'upload called'
    user = check_validation(request)
    if user:
        print 'authentic user'
    else:
        print 'user not logged in '
        return redirect('/login/')
    return render(request,'upload.html')