# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render , HttpResponse ,redirect
import datetime
from forms import signedup , login_form, posts , like , comment_form , tag_form
from models import user_details ,session_token , post_model ,likes , comment
from django.contrib.auth.hashers import make_password ,check_password
from imgurpython import ImgurClient
from django.core.mail import EmailMessage
from clarifai.rest import ClarifaiApp
# Create your views here.

#clarifai App keys
app = ClarifaiApp(api_key='ab7a257992dd4a39a6cce25e706ae0bc')
model=app.models.get("general-v1.3")

#Imgur Api keys
client_id='710fd5f2970325f'
client_secret='3426c4aa99f4b77d7da86bd929b106b5f71610c3'


#sign up view
#html file - sign_up.html
def sign_up(request):
    print 'success'
    #getting current date and time
    today=datetime.datetime.now()
    if request.method=='GET':
        signedup_obj = signedup()
    elif request.method=='POST':
        print 'POST called'
        signedup_obj=signedup(request.POST)
        if signedup_obj.is_valid():
            #getting detials from the form
            name = signedup_obj.cleaned_data.get('name') #.get('name')
            print name
            username=signedup_obj.cleaned_data.get('username') #.get('username')
            mail=signedup_obj.cleaned_data.get('email')  #.get('email')
            password=signedup_obj.cleaned_data.get('password')   #.get('password')
            #creating a new entry on the user model
            user=user_details(name=name,username=username,password=make_password(password),email=mail,)
            user.save()
            user.is_active=False
            user.save()
            # sending a activation link to the user
            try:
                email = EmailMessage('Activation Link', 'You just signed Up for InstaCLone ....'
                                                    '.click on the link below to get your account activated \n\n '
                                                    'http://127.0.0.1:8000/activate/?username='+(username), to=[mail])
                email.send()
                print ' Activation mail sent '
            except:
                print ' network error in sending the mail'
            return  render(request,'activate_link.html')
        else:
            print 'Validation failed'
    return render(request, 'sign_up.html',{'today':today,'signed_obj':signedup_obj})

#redirected to this from the activation link
def activate(request):
    print 'Activate called'
    user=request.GET.get('username')
    user_obj=user_details.objects.filter(username=user).first()
    print user_obj
    print user_obj.name
    print user_obj.email
    print user_obj.is_active
    # changing the is active field to true for activated users
    if user_obj.is_active==False:
        user_obj.is_active=True
        user_obj.save()
    else :
        print ' user has been alreay activated'

    return render(request, 'activate.html',{'user':user_obj.name})

#rendering the sign_up_Succes.html [age on the succesfull sign up of user
def signup_success(request):
    print ' sign up success called '
    return  render(request , 'sign_up_succes.html')


#login view called which renders the login.html

def login(request):
    if request.method=='GET':
        login=login_form()
    if request.method=='POST':
        login=login_form(request.POST)
        print 'post called'
        if login.is_valid():
            print 'login valid'
            #getting the entered user and password from the form
            username=login.cleaned_data.get('username')
            password=login.cleaned_data.get('password')
            print username
            user=user_details.objects.filter(username=username).first()
            print user
            if user.is_active==True:
                #using the check password method for checking entered password and the crypted password
                if check_password(password,user.password):
                    print 'user valid'
                    print user.email
                    try:
                        email = EmailMessage('Logged in..',
                                             'You just logged into your account ....report if it was not you ....',
                                             to=[user.email])
                        email.send()
                    except:
                        print ' network error in sending mail '

                    #create a cookie on succesfull loging in
                    token=session_token(username=user)
                    token.create_token()
                    token.save()
                    response = redirect('/feed/')
                    print response
                    response.set_cookie(key='session_token', value=token.token)
                    print 'cookie set'
                    return response
        else :
            #on insuccesfull login redirect back to the login page
                    print ' user invalid...Not Activated'
                    return render(request, 'Login.html',{'login':login})
    return render(request, 'Login.html',{'login':login})


#this method checks if user is alredy login or has a cookie created
def check_validation(request):
    if request.COOKIES.get('session_token'):
        session=session_token.objects.filter(token=request.COOKIES.get('session_token')).first()
        if session:
            return session.username
    else:
        return None


#the feed method displays the posts of the user from the feed.html
def feed(request):
    print 'feed called'
    user=check_validation(request)
    if user:
        #if user is valid getting all the posts from the user
        print 'authentic user'
        post_obj = post_model.objects.all()
        user_now=user_details.objects.filter(username=user).first()
        print 'welcome' , user_now.name
        for post in post_obj:
            existing_like=likes.objects.filter(post_id=post.id,username=user).first()
            # this code checks for existing like and cretes one if not present
            if existing_like:
                post.has_liked=True
                post.save()
                print ' has liked changed to true'
            else:
                post.has_liked=False
                post.save()
                'has liked is taking default value'
        return render(request, 'feed.html', {'posts':post_obj,'user':user_now.name})
    else :
        print 'user not logged in'
        return redirect('/login/')
    return render(request, 'feed.html')


# this method is used when the user wants to upload a post
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
                 #getting the path and the caption from the form
                 image=post_obj.cleaned_data.get('image')
                 caption=post_obj.cleaned_data.get('caption')
                 client =ImgurClient(client_id,client_secret)
                 print ' mail of the user who has uploaded the pic ' , user.email
                 #image_url=post_obj.cleaned_data.get('image_url')
                 post=post_model(username=user,image=image, caption=caption)
                 post.save()
                 path = (r'C:/Users/Sant Sharma/Desktop' + '/'+  post.image.url)
                 print path
                 #using the imgur API to upload the posts to the imgur servers
                 post.image_url = client.upload_from_path(path, anon=True)['link']
                 print 'post sAVED'
                 print post.image_url
                 # using the clarifai API to create tags for posts uploaded by the user and storing them
                 print ' using clarifai'
                 tags = model.predict_by_url(url=post.image_url)
                 post.tag1=tags['outputs'][0]['data']['concepts'][0]['name']
                 post.tag2 = tags['outputs'][0]['data']['concepts'][1]['name']
                 post.tag3 = tags['outputs'][0]['data']['concepts'][2]['name']
                 #list = []

                 #for temp in tags['outputs'][0]['data']['concepts']:
                  #   if temp['value'] > 0.95:
                   #      print ' The image has the following tags'
                    #     print temp['name']
                     #    list.append(temp['name'])

                 #post.tags=' '.join(list)
                 post.save()
                 # sending a mail to the user when he/she uploads the pic
                 try:
                    email = EmailMessage('Uploaded a pic ',
                                      'You just uploded a pic from your account .....image url \n \n'+post.image_url+'\n   with the caption \n \n ' + post.caption, to=[user.email])
                    email.send()
                 except:
                     print ' network error in sending mail'
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


# this method is called when the user likes a post
def like_view(request):
    print 'like view called'
    user=check_validation(request)
    if user and request.method=='POST':
        print ' user valid'
        like_obj=like(request.POST)
        if like_obj.is_valid():
            print ' like obj valid '
            post_id=like_obj.cleaned_data.get('post')
            like_exist=likes.objects.filter(post=post_id,username=user).first()
            if like_exist:
                like_exist.delete()
                print ' like deleted'
            elif not like_exist:
                likes.objects.create(post_id=post_id,username=user)
                print ' like created'
                print ' like by  ', user, 'on ', post_id
                print ' like was made on ', post_id.username.email
                # sending a mail when a post id liked
                try:
                    email = EmailMessage('Liked your pic', user +
                                         '  has just posted a like on your pic ....please check it out \n ',
                                         to=[post_id.username.email])
                    email.send()
                except:
                    print ' network error in sending mail '
            else :
                print ' error with like'

            return redirect('/feed/')
        else :
            print ' like obj invalid'
    else :
        print ' user invalid'
        return redirect('/login/')
    return redirect('/feed/')


#this method is caled when the user makes a comment
def make_comment(request):
    print ' make comment called'
    user = check_validation(request)
    if user and request.method=='POST':
        print ' user valid and post called'
        comment_obj = comment_form(request.POST)
        if comment_obj.is_valid():
            print ' comment form valid'
            post_id=comment_obj.cleaned_data.get('post')
            comment_text=comment_obj.cleaned_data.get('comment_text')
            #user_temp = user_details.objects.filter(post_id=post_id, )
            print 'email of the user who hsa posted  comment', user.email
            cmmnt=comment.objects.create(username=user , post=post_id, comment_text=comment_text)
            cmmnt.save()
            print ' model of comment saved '
            print ' comment was made by  ', user , 'on ' , post_id
            print ' comment was made on ' ,post_id.username.email
            # the user is sent a mail whose post is commented upon
            try:
                email = EmailMessage('Comment made', user+
                                     '  has just posted a comment on your pic ....please check it out \n Comment:'+comment_text,
                                     to=[post_id.username.email])
                email.send()
            except:
                print ' network error in sending mail '
        else :
            print ' comment form invalid'
            return redirect('/feed/')
    else :
        print ' not logged in '
        return redirect ('/login/')
    return redirect('/feed/')


# this method is called when the user logs out
# also the cookie cretaed is deleted
def logout(request):
    HttpResponse("<h1> Logging out .....</h1>")
    user=check_validation(request)
    if user:
        token = session_token.objects.filter(username=user)
        token.delete()
        return redirect('/login/')
    else:
        return  redirect('/login/')


def user_info(request):
    return  render(request,'user_info.html')

# this method is caleed when a user wants to see uploads from a particular user
def userfeed(request):
    print 'USerfeed called'
    user_search = request.GET.get('username')
    userss=user_details.objects.filter(username=user_search).first()
    print 'user search is',userss.username
    print 'user name is ',userss.name

    if userss:
        print ' user found'
        user = check_validation(request)
        if user:
            print 'authentic user'
            #print 'user search is ', user_search
            post_obj = post_model.objects.filter(username=userss).all()
            for post in post_obj:
                #using filter to select the particular user from alll the objects
                existing_like = likes.objects.filter(post_id=post.id, username=user).first()
                if existing_like:
                    post.has_liked = True
                    post.save()
                    print ' has liked changed to true'
                else:
                    post.has_liked = False
                    post.save()
                    'has liked is taking default value'
            print 'user search is (passing to html) ', userss
            return render(request, 'userfeed.html', {'posts': post_obj, 'username': userss})
        else:
            print 'user not logged in'
            return redirect('/login/')
    else:
        print ' no such user found'
    return render(request, 'userfeed.html')

    return HttpResponse('<h1>hii</h1>')


# this method is called whenthe user wants to search for an image based on the tags of the post
def buynsell(request):
    img_url='http://www.rasmussen.edu/images/blogs/1325623457-examining-search-terms.jpg'
    if request.method=="POST":
        tag_form_obj=tag_form(request.POST)
        if tag_form_obj.is_valid():
            print ' tag form is valid'
            tag=tag_form_obj.cleaned_data['tag1']
            #print ' tag is ', tag
            # filter objects from the posts where tags match the tag of the post
            post_obj1=post_model.objects.filter(tag1=tag).first()
            if post_obj1:

                print 'tag1 found'
                print post_obj1.image_url
                img_url=post_obj1.image_url

            post_obj2=post_model.objects.filter(tag2=tag).first()
            if post_obj2:
                print post_obj2.image_url

                print 'tag2 found'
                img_url=post_obj2.image_url

            post_obj3=post_model.objects.filter(tag3=tag).first()
            if post_obj3:
                print post_obj3.image_url
                img_url=post_obj3.image_url
                print 'tag3 found'
            return render(request, 'buynsell.html', {'url': img_url})

        else :
            print ' tag form is invalid'
    return render (request,'buynsell.html', {'url': img_url} )