from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.http.request import HttpRequest
from random import choice
from django.contrib.auth import login, logout, authenticate
from . import models
import re, os,time
from . import  sendEmail
from helthcare.validator import Validator
from django.conf import settings
from datetime import datetime
from django.utils import timezone


send_email = sendEmail.Email()

signupuser_pages_token = []
signup_data = {}


# Create your views here.
def check(email):
    if(re.fullmatch(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b', email)):
        True
    else:
        False

def home(request: HttpRequest):
    if request.user.is_anonymous:
        return redirect("/login")


    context = {
        "full_name" : f"{request.user.first_name} {request.user.last_name}"
    }

    context["user"] = request.user

    category = request.GET.get("catg")
    print(f"get_catgory => {category}")

    selected_catg = None
    if category != None:
        selected_catg = models.Catgory.objects.get(id=category)
        if selected_catg:
            print(f"selected => {category}")
            context["selected_catg"] = selected_catg

    context["catgory_obj"] = models.Catgory.objects.all()
    if selected_catg:
        blogs_obj = models.Blog.objects.filter(catgory=selected_catg, is_draft=False)
    else:
        blogs_obj = models.Blog.objects.all().exclude(is_draft=True)
    print(f"blog==> {blogs_obj}")

    context["blogs_obj"] = blogs_obj
    context["user"] = request.user

    return render(request, "home.html", context=context)


def myblog(request: HttpRequest):
    if request.user.is_anonymous:
        return redirect("/login")

    if not request.user.is_doctor:
        return redirect("/")


    context = {}
    context["user"] = request.user
    context["blogs_obj"] = models.Blog.objects.filter(user=request.user).exclude(is_draft=True)

    return render(request, "myblog.html", context=context)


def draft(request: HttpRequest):
    if request.user.is_anonymous:
        return redirect("/login")

    if not request.user.is_doctor:
        return redirect("/")


    context = {}
    context["user"] = request.user
    context["blogs_obj"] = models.Blog.objects.filter(user=request.user).exclude(is_draft=False)

    return render(request, "draft.html", context=context)

def view_blog(request: HttpRequest):
    if request.user.is_anonymous:
        return redirect("/login")


    blog_id = request.GET.get("blog")
    title = request.GET.get("title")

    print(f"blogid==> {blog_id}")

    print(f"title==> {title}")

    context = {}
    context["user"] = request.user

    if blog_id == None:
        return HttpResponse("None is found as blog")

    blog = models.Blog.objects.get(id=blog_id)
    context["blog"] = blog

    print(f"blog ==> {blog}")
    if not blog:
            return HttpResponse("Hey, what are you doing, just follow the likn")

    return render(request, "detailedpost.html", context=context)



def write_blog(request: HttpRequest):
    if request.user.is_anonymous:
        return redirect("/login")

    if not request.user.is_doctor:
        return redirect("/")

    edit_blog_id = request.GET.get("blog")


    if request.method == "POST":
        title = request.POST.get("title", "")
        catgory = request.POST.get("catgory", "")
        summary = request.POST.get("summary", "")
        content = request.POST.get("content", "")
        blog_id = request.POST.get("blogid", None)
        action = request.POST.get("action")

        print(f"Action===> {action}")

        is_draft = False
        if action == "Draft":
            is_draft = True


        print(f"title ==> {title}")
        print(f"catgory ==> {catgory}")
        print(f"summary ==> {summary}")
        print(f"content ==> {content}")
        print(f"is_draft ==> {is_draft}")

        try:
            int(blog_id)
        except:
            blog_id = None


        updated = timezone.now()
        catgory = models.Catgory.objects.get(id=catgory)

        print("block--> ", blog_id)
        blog = None
        if blog_id != None:
            print("blogid--> ", blog_id)
            blog = models.Blog.objects.get(id = blog_id)

            if blog.user != request.user:
                return HttpResponse("This doesn't belogs to you")

            if not blog.is_draft:
                return HttpResponse("Can't edit the blog wich is already plosted, only drafts can be edited")



        if blog:
            blog.title = title
            blog.catgory = catgory
            blog.summary = summary
            blog.content = content
            blog.updated = updated
            blog.is_draft = is_draft
            blog.save(update_fields=['title', 'catgory', 'summary', 'content', 'updated', 'is_draft'])

        else:
            blog = models.Blog(user = request.user, catgory = catgory,
                            title = title, summary = summary,
                            content = content, updated = updated,
                            is_draft = is_draft)
            blog.save()




        file = request.FILES.get("file")

        if file:
            file_name = f"blog_{blog.id}_{request.user.email}{os.path.splitext(file.name)[1]}"
            full_path = f"{settings.BASE_DIR}/static/blog/{file_name}"

            with open(full_path, 'wb') as dest:
                for chunk in file.chunks():
                    dest.write(chunk)
            blog.file = file_name
            blog.save(update_fields=['file'])

        edit_blog_id = None




    context = {"full_name" : f"{request.user.first_name} {request.user.last_name}"}


    context["update" ] = "No Update"
    context["profile"] =  request.user.propath
    context["catgory_obj"] = models.Catgory.objects.all()

    if edit_blog_id != None:
        blog_obj = models.Blog.objects.get(id=edit_blog_id)
        if blog_obj and blog_obj.user == request.user:
            if blog_obj.is_draft:
                context["title" ] = blog_obj.title
                context["update" ] = blog_obj.updated
                context["summary" ] = blog_obj.summary
                context["image" ] = blog_obj.file
                context["selected_catgory" ] = blog_obj.catgory
                context["content" ] = blog_obj.content
                context["blogid"] = blog_obj.id

            else:
                return HttpResponse("Can't edit the blog wich is already plosted, only drafts can be edited")

    context["user"] = request.user
    return render(request, "blog.html", context=context)


def signup(request: HttpRequest):
    if request.user.is_anonymous:
        return redirect("/login")


def logout_user(request: HttpRequest):
    logout(request)
    return redirect("/login")


def forgot(request: HttpRequest):
    return HttpResponse("<h1>Under development...</h1>")





#____LOGIN________PAGE_______________________________
def login_user(request):
    if request.user.is_authenticated:
        return redirect('/')

    context={}
    if request.method=="POST" :
        ## Check if user has entrered correct credentials
        username=request.POST.get("email")
        password=request.POST.get("password")
        print("user==>",username,"pass==>",password)

        user = authenticate(username=username, password=password)
        if user is not None:
            login( request , user)
            return redirect('/')

        else:
            # No backend authenticated the credentials
            profile_obj = models.MyUser.objects.filter(email=username).first()
            if not profile_obj:
                context["message"]="The username you entered doesn't belong to an account. Please check your username and try again."
            else:
                context["prefix"]=f"Sorry! {profile_obj.first_name},"
                context["message"]="your password was incorrect. Please double-check your password."
            return render(request , "login.html" , context)

    return render(request , "login.html" , context)


def logout_user(request):
    logout(request)
    return redirect('/login')


def genSessionId(len_ = 50, idList= []):
    data = "zxcvbnmasdfghjklqwertyuiop1234567890ZXCVBNMASDFGHJKLQWERTYUIOP"
    id_ = ""
    for i in range(len_):
        id_ += choice(data)

    if id_ in idList:
        genSessionId(len_, idList)
    else:
        return id_

def getOtp(len_=8):
    otp = ""
    for i in range(len_):
        otp += choice("0493826571")
    return otp



def signupuser(request : HttpRequest):

    action = request.GET.get('action', '')
    token = request.GET.get("token", None)
    if token == None:
        if request.method == "POST":
            print("toke is  got from post request")
            token = request.POST.get("token")

    context = {}

    print(f"actionn===> {action}")
    print(f"token==> {token}")

    print(f"tokenList==> {signupuser_pages_token}")


    if token not in signupuser_pages_token:
        fro_m = request.GET.get('from', None)
        if fro_m == "fetch":
            return JsonResponse({"error" : "Page Authentication error. Please try again.", "status" : "error", "error_code" : 0})


        tokenid = genSessionId(idList=signupuser_pages_token)
        signupuser_pages_token.append(tokenid)
        context["token"] = tokenid
        print("token noot in")

        context["message"] = "This action requires email verification. An OTP is send to your email to verify your email id."
        context["prefix"] = "Hey!, "


        return render(request, "signupuser.html", context=context)

    signupuser_pages_token.remove(token)
    print("removing  token")


    if action == "addemail":
        print("add action email")

        email = request.GET.get("val")

        print(f"Emil==> {email}")
        tokenid = genSessionId(idList=signupuser_pages_token)
        signupuser_pages_token.append(tokenid)

        new_authkey = genSessionId(idList=list(signup_data))
        otp = getOtp(6)

        print(f"OTP==> {otp}")


        signup_data[new_authkey] = {
            "email" : email,
            "email_veried" : 0,
            "otp" : otp,
            "otp_time" : time.time(),
            "token" : tokenid,
            "trytime" : 0,
        }

        page = send_email.send_otp("User", otp)
        st = send_email.send(email, "Verify Email", page)
        if st:
            print("Email is send")

            data = {"token" : tokenid, "status" : "validemail", "auth" : new_authkey}
        else:
            data = {"error" : "Error in sending OTP to this email id. Please try later.", "status" : "error"}

        return JsonResponse(data)

    elif action == "verifyotp":
        print("add action email")


        otp = request.GET.get("val")
        authkey = request.GET.get("auth")


        if authkey in  signup_data:

            print(f"Email=====> {signup_data[authkey]['email']}")
            if token != signup_data[authkey]['token']:
                return JsonResponse({"error" : "Page Authentication error. Please try again.", "status" : "error", "error_code" : 0})

            tokenid = genSessionId(idList=signupuser_pages_token)

            print(f"trytime===> {signup_data[authkey]['trytime']}")



            if signup_data[authkey]["trytime"] > 2:
                return JsonResponse({"error" : "Blocked this id due to too many attempts. Please use another email id.", "status" : "error",  "error_code" : 0})



            if otp != signup_data[authkey]["otp"]:
                signupuser_pages_token.append(tokenid)
                signup_data[authkey]['token'] = tokenid

                signup_data[authkey]["trytime"] = signup_data[authkey]["trytime"] + 1
                if (3 - signup_data[authkey]['trytime']) == 0:
                    chance = "no chance"
                elif (3 - signup_data[authkey]['trytime']) == 1:
                    chance = f"{(3 - signup_data[authkey]['trytime'])} chance"
                else:
                    chance = f"{(3 - signup_data[authkey]['trytime'])} chances"

                return JsonResponse({"status" : "error", "token" : tokenid,  "error" : f"The OTP you've entered is incorrect. Please try again. You have {chance} is left.",  "error_code" : 1})


            if (time.time() - signup_data[authkey]["otp_time"]) > 120:

                signupuser_pages_token.append(tokenid)
                signup_data[authkey]['token'] = tokenid

                signup_data[authkey]["trytime"] = signup_data[authkey]["trytime"] + 1

                otp = getOtp(6)
                signup_data[authkey]["otp"] = otp
                signup_data[authkey]["otp_time"] = time.time()

                if (3 - signup_data[authkey]['trytime']) == 0:
                    chance = "no chance"
                elif (3 - signup_data[authkey]['trytime']) == 1:
                    chance = f"{(3 - signup_data[authkey]['trytime'])} chance"
                else:
                    chance = f"{(3 - signup_data[authkey]['trytime'])} chances"

                page = send_email.send_otp("User", otp)

                st = send_email.send(signup_data[authkey]["email"], "Verify Email (sent again)", page)
                if not st:
                    return JsonResponse({"error" : "Error in sending email to this email. Please try again or later.", "status" : "error", "error_code" : 0})

                return JsonResponse({"status" : "error", "token" : tokenid,  "error" : f"The OTP entered is expired. A new OTP is sent again to your email. Please check and enter it. Your have only  {chance} is left.", "error_code" : 2})


            data = {
                "status" : "validotp",
                "token" : tokenid,
            }

            # # remove any prev data with same id
            email = signup_data[authkey]["email"]
            # for keys in signup_data:
            #     if keys != authkey:
            #         if signup_data[keys]["email"] == email:
            #             signup_data.pop(keys)
            #             print("=============> ID is removed")  getting an error: data changed duing etration

            userObj = models.MyUser.objects.filter(email = email).first()
            print(f"UserObject===> {userObj}")
            if userObj != None:
                return JsonResponse({"status" : "error", "error" : f'This email address is already registered. If this belogs to you, click on  <a href="/passwordReset?email={email}">Forgot Password</a> to change password or <a style="color : green;" href="/contacts">Contact</a> to the admin if any issue.', "error_code" : 0})


            signup_data[authkey]["otp"] = "verified"
            signup_data[authkey]["email_veried"] = 1
            signup_data[authkey]["token"] = tokenid

            signupuser_pages_token.append(tokenid)

            print("opt verified...")
            return JsonResponse(data)


    if request.method == "POST":
        print("post mehhtods is here")
        action = request.POST.get("postaction")

        if action == "username":

            username = request.POST.get("username")
            email = request.POST.get("email")
            authkey = request.POST.get("authkey")
            token = request.POST.get("token")

            if authkey not in  signup_data:
                return JsonResponse({"error" : "invalid auth"})

            print(f"username Email=====> {signup_data[authkey]['email']}")
            if token != signup_data[authkey]['token']:
                return JsonResponse({"error" : "invalid token"})

            if email != signup_data[authkey]['email']:
                return JsonResponse({"error" : "invalid email"})

            if not signup_data[authkey]['email_veried']:
                return JsonResponse({"error" : "invalid not verified"})

            print(f"email==> {email} ")
            print(f"Username==> {username} ")
            print(f"authkey==> {authkey} ")

            tokenid = genSessionId(idList=signupuser_pages_token)

            signup_data[authkey]["token"] = tokenid
            signup_data[authkey]["username"] = username

            signupuser_pages_token.append(tokenid)

            context["token"] = tokenid
            context["authkey"] = authkey

            return render(request, "userdetail.html", context=context)


        elif action == "userdetails":

            fname = request.POST.get("fname")
            lname = request.POST.get("lname", "")
            authkey = request.POST.get("authkey")
            token = request.POST.get("token")
            line1 = request.POST.get("line1")
            city = request.POST.get("city")
            pincode = request.POST.get("zip")
            state = request.POST.get("state")

            if authkey not in  signup_data:
                return JsonResponse({"error" : "invalid auth"})

            if token != signup_data[authkey]['token']:
                return JsonResponse({"error" : "invalid token"})

            print(f"fname ==>{fname}")
            print(f"lname ==>{lname}")
            print(f"line1 ==>{line1}")
            print(f"city ==>{city}")
            print(f"state ==>{state}")
            print(f"email ==>{signup_data[authkey]['email']}")

            tokenid = genSessionId(idList=signupuser_pages_token)

            signup_data[authkey]["token"] = tokenid
            signupuser_pages_token.append(tokenid)

            signup_data[authkey]["fname"] = fname
            signup_data[authkey]["lname"] = lname
            signup_data[authkey]["line1"] = line1
            signup_data[authkey]["city"] = city
            signup_data[authkey]["pincode"] = pincode
            signup_data[authkey]["state"] = state

            context["token"] = tokenid
            context["authkey"] = authkey
            context["fname"] = fname
            context["message"] = "Please create a password that is at least 8 characters in length"
            context["prefix"] = f"Hey {fname}! , "

            return render(request, "password.html", context=context)


        elif action == "passwd":

            passwd = request.POST.get("passwd")
            confirmpasswd = request.POST.get("confirmpasswd")
            authkey = request.POST.get("authkey")
            token = request.POST.get("token")

            if authkey not in  signup_data:
                return JsonResponse({"error" : "invalid auth"})

            if token != signup_data[authkey]['token']:
                return JsonResponse({"error" : "invalid token"})


            if passwd == confirmpasswd:
                passwd_val = Validator(passwd = passwd, email=signup_data[authkey]['email'], name=f"{signup_data[authkey]['fname']} {signup_data[authkey]['lname']}", username=signup_data[authkey]['username'])

                error = passwd_val.validate()

            else:
                error = "Please make sure your passwords match"

            if error:
                tokenid = genSessionId(idList=signupuser_pages_token)
                signupuser_pages_token.append(tokenid)
                signup_data[authkey]['token'] = tokenid


                context["message"] = error

                context["token"] = tokenid
                context["authkey"] = authkey
                context["passwd"] = confirmpasswd

                context["fname"] = f"Hey {signup_data[authkey]['fname']}!"

                return render(request, "password.html", context=context)



            email = signup_data[authkey]['email']
            username = signup_data[authkey]['username']
            fname = signup_data[authkey]['fname']
            lname = signup_data[authkey]['lname']
            line1 = signup_data[authkey]['line1']
            city = signup_data[authkey]['city']
            pincode = signup_data[authkey]['pincode']
            state = signup_data[authkey]['state']

            print("User Detials")
            print(f"email ==> {email}")
            print(f"username ==> {username}")
            print(f"fname ==> {fname}")
            print(f"lname ==> {lname}")
            print(f"passwd ==> {passwd}")
            print(f"confirmpasswd ==> {confirmpasswd}")


            e_st = False

            userObj = models.MyUser.objects.filter(email = email).first()
            if userObj != None:
                e_st = True

            userObj = models.MyUser.objects.filter(username = username).first()
            if userObj != None:
                e_st = True

            if  e_st:
                return JsonResponse({"Error" : "email or phone is already associated to  antoher account"})

            profile = "man.png"

            singup = models.MyUser(email=email, username=username, first_name=fname, last_name=lname, propath=profile)
            singup.set_password(confirmpasswd)
            singup.save()

            login( request , singup)

            return  redirect('/profile')

    return render(request, "signupuser.html", context=context)




def profile_img(request : HttpRequest):
    if request.method == "POST":
        if request.user.is_anonymous:
            return HttpResponse(status=500)

        email = request.user.email
        file_data = request.POST.get("photo")
        is_doc = request.POST.get('doctor')
        print(f"Is==>", is_doc)

        if is_doc == "on":
            is_doc = True
        else:
            is_doc = False

        print(f"Is==>", is_doc)

        file = request.FILES['photo']
        file_name = f"{email}_profile{os.path.splitext(file.name)[1]}"
        full_path = f"{settings.BASE_DIR}/static/img/{file_name}"

        try:
            if os.path.exists(request.user.propath):
                if file_name != request.user.propath:
                    os.remove(request.user.propath)
                    print("File is delete")
                else:
                    print("File is overwrite")
            else:
                print("File  notfound")
        except Exception as e:
            print(f"Error at removing file: {e}")


        with open(full_path, 'wb') as dest:
            for chunk in file.chunks():
                dest.write(chunk)


        request.user.propath = file_name
        request.user.is_doctor = is_doc
        request.user.save(update_fields=['propath', 'is_doctor'])
        return HttpResponse(status=204)


    context = {
        "profile" : "man.png",
        "is_doc" : ''}
    if not request.user.is_anonymous:
        context["profile"] = request.user.propath
        if request.user.is_doctor:
            context["is_doc"] = 'checked'

    return render(request, "profile.html", context=context)



def test_page(request : HttpRequest):
    print("test ing")

    if request.method == "POST":
        if request.user.is_anonymous:
            return HttpResponse(status=500)

        email = request.user.email
        file_data = request.POST.get("photo")
        is_doc = request.POST.get('doctor')

        if is_doc == "on":
            is_doc = True
        else:
            is_doc = False

        print(f"Is==>", is_doc)

        file = request.FILES['photo']
        file_name = f"{email}_profile{os.path.splitext(file.name)[1]}"
        full_path = f"{settings.BASE_DIR}/static/img/{file_name}"

        try:
            if os.path.exists(request.user.propath):
                if file_name != request.user.propath:
                    os.remove(request.user.propath)
                    print("File is delete")
                else:
                    print("File is overwrite")
            else:
                print("File  notfound")
        except Exception as e:
            print(f"Error at removing file: {e}")


        with open(full_path, 'wb') as dest:
            for chunk in file.chunks():
                dest.write(chunk)


        request.user.propath = file_name
        request.user.is_doctor = is_doc
        request.user.save(update_fields=['propath', 'is_doctor'])
        return HttpResponse(status=204)


    context = {
        "profile" : "man.png",
        "is_doc" : ''}
    if not request.user.is_anonymous:
        context["profile"] = request.user.propath
        if request.user.is_doctor:
            context["is_doc"] = 'checked'

    return render(request, "profile.html", context=context)

