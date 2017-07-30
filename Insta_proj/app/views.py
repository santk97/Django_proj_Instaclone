# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render , HttpResponse ,redirect
import datetime
from forms import signedup , login_form, posts , like , comment_form
from models import user_details ,session_token , post_model ,likes , comment
from django.contrib.auth.hashers import make_password ,check_password
from imgurpython import ImgurClient
import os

# Create your views here.

client_id='710fd5f2970325f'
client_secret='3426c4aa99f4b77d7da86bd929b106b5f71610c3'



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
                    #print str(token)
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
        post_obj = post_model.objects.all()

        for post in post_obj:
            existing_like=likes.objects.filter(post_id=post.id,username=user).first()

            if existing_like:
                post.has_liked=True
                post.save()

                print ' has liked changed to true'
            else:
                post.has_liked=False
                post.save()
                'has liked is taking default value'

        return render(request, 'feed.html', {'posts':post_obj})
    else :
        print 'user not logged in'
        return redirect('/login/')

    return render(request, 'feed.html')

def upload(request):
    print 'upload called'
    user = check_validation(request)
    if user:
        print 'authentic user'
        if request.method=='POST':
            print  ' post of upload called'
            post_obj = posts(request.POST,request.FILES)
            if post_obj.is_valid():
                 print 'form valid'
                 image=post_obj.cleaned_data.get('image')
                 caption=post_obj.cleaned_data.get('caption')
                 client =ImgurClient(client_id,client_secret)
                 #image_url=post_obj.cleaned_data.get('image_url')
                 post=post_model(username=user,image=image, caption=caption)
                 post.save()
                 path = (r'C:/Users/Sant Sharma/Desktop' + '/'+  post.image.url)
                 print path
                 post.image_url = client.upload_from_path(path, anon=True)['link']
                 print 'post sAVED'
                 print post.image_url
                 post.save()


            else:
                print 'post form invalid'


            return redirect( '/feed/')
        elif request.method=='GET':
            post_obj=posts()

    else:
        print 'user not logged in '
        return redirect('/login/')
    return render(request,'upload.html')

def like_view(request):
    print 'like view called'
    user=check_validation(request)
    if user and request.method=='POST':
        print ' user valid'
        like_obj=like(request.POST)

        if like_obj.is_valid():
            print ' like obj valid '
            post_id=like_obj.cleaned_data.get('post').id
            like_exist=likes.objects.filter(post_id=post_id,username=user).first()
            if like_exist:
                like_exist.delete()
                print ' like deleted'
            elif not like_exist:
                likes.objects.create(post_id=post_id,username=user)
                print ' like created'
            else :
                print ' error with like'

            return redirect('/feed/')
        else :
            print ' like obj invalid'
    else :
        print ' user invalid'
        return redirect('/login/')

    return redirect('/feed/')


def make_comment(request):
    print ' make comment called'
    user = check_validation(request)
    if user and request.method=='POST':
        print ' user valid and post called'
        comment_obj = comment_form(request.POST)
        if comment_obj.is_valid():
            print ' comment form valid'
            post_id=comment_obj.cleaned_data.get('post').id
            comment_text=comment_obj.cleaned_data.get('comment_text')
            cmmnt=comment.objects.create(username=user , post_id=post_id, comment_text=comment_text)
            cmmnt.save()
            print ' model of comment saved '
        else :
            print ' comment form invalid'
            return redirect('/feed/')

    else :
        print ' not logged in '
        return redirect ('/login/')

    return redirect('/feed/')
