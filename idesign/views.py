from django.urls import path
from zipfile import ZipFile
from django.http import JsonResponse
from django.contrib.auth.models import User
from .filters import ProductFilter
from django.db.models import Q, F
from django.shortcuts import get_list_or_404, get_object_or_404
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth

from django.contrib import messages
import json
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
# Create your views here.
import requests
from .models import Web, Category, PostImage, Search, Slider, PostFile
from django.db import connection
from math import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# for email
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.template.loader import render_to_string
from .utils import account_activation_token
from django.urls import reverse
from django.contrib import auth
from django.core.mail import EmailMessage
from django.views.decorators.csrf import csrf_exempt
# Create your views here
import threading
# zip file
from io import BytesIO
import os
import zipfile
from pathlib import Path
# for password reset
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils import timezone
# --------------------zipfile---------------
from shutil import make_archive
from wsgiref.util import FileWrapper
import io

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


def get_category(request):
    categories = Category.objects.filter(parent_id__isnull=True)
    return categories


def get_subcategory(request):
    subcategories = []
    subcategories = Category.objects.all()
    # put condition in run time
    return subcategories


def get_subsubcategory(request):
    subsubcategories = []
    subcategories = get_subcategory(request)
    for subcategory in subcategories:
        subsubcategories = Category.objects.filter(parent_id=subcategory.id)
    return subsubcategories


def get_feature_products(request):
    feature_products = list(Web.objects.filter(Exclusive=True))
    feature_products = feature_products[:-4:-1]
    return feature_products


def get_latest_products(request):
    latest_products = list(Web.objects.all())
    latest_products = latest_products[:-9:-1]
    return latest_products


def filtering(request):
    products = Web.objects.all()
    filter = ProductFilter(request.GET, queryset=products)
    return filter


def home(request):

    data = {}
    data['sliders'] = Slider.objects.all()
    data['feature_products'] = get_feature_products(request)
    data['latest_products'] = get_latest_products(request)
    data['categories'] = get_category(request)
    data['subcategories'] = get_subcategory(request)

    return render(request, 'T-index.html', data)

from smoak import settings
from io import BytesIO
import boto3
def singal_product(request, id):
    
    newfile = []
    context = {}
    context["data"] = Web.objects.get(id=id)
    allimg = PostImage.objects.filter(parent_img_id=id)
    allfile = list(PostFile.objects.filter(parent_file_id=id))


   
    filename = context["data"].design_code+'.zip'
#     ZipFile = zipfile.ZipFile("./"+filename, "w")

#     byte = BytesIO()
    session = boto3.session.Session(aws_access_key_id=settings.AWS_ACCESS_KEY_ID, aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY)

    s3 = session.resource("s3")
    s3 = boto3.client("s3", region_name = "us-east-2")
    s3_resource = session.resource("s3")
    
#     bucket = s3.Bucket('tripple-run')
#     obj = bucket.Object('smsspamcollection.zip')
        
  
#     bucket = s3.lookup(settings.AWS_STORAGE_BUCKET_NAME)
#     print('bucket==',bucket)
#     zf = zipfile.ZipFile(byte, "w")
#     zipped_files = []
#     zip_filename = 'download_files.zip'
    
#     for index, fpath in enumerate(allfile):
#         path = fpath.file.name.split('/')
#         current_file = path[len(path)-1]

#         zipped_files.append(current_file)
#         print('dszfafad =',fpath.file.url)
#         key = bucket.put_object(fpath.file.url.split('.com')[1])
#         data = key.read()

#         open(current_file, 'wb').write(data)
#         zf.write(current_file)
#         os.unlink(current_file)
#     zf.close()
    
#     for a,fpath in enumerate(allfile):
#         print('zip111111 = ',fpath.file.url)
#         path = fpath.file.name.split('/')
#         current_file = path[len(path)-1]
#         print('cur',current_file)
# #         zipped_files.append(current_file)
#         ZipFile.write(current_file)
# #       ZipFile.write(a.file.url, os.path.relpath(a.file.path, './media/pics/Product_file'),
# #                       compress_type=zipfile.ZIP_DEFLATED)
# #     print('zip111111 = ', a.file.name)
#         os.unlink(current_file)
#     ZipFile.close()
   
#     print(a.file.path)
#     resp = HttpResponse(byte.getvalue(), content_type="application/x-zip-compressed")
#     resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename
    abc = []
    for a in allfile:
        abc.append(a.file.name)
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED, False) as zipper:
        
        print('a.file = = ', a.file.name)
        print('a.file.url = = ', a.file.url)
       

        infile_object = s3.get_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key = abc)
#             print('aaaaaaaaaaooo=',infile_object)

        infile_content = infile_object['Body'].read()
        

#             print('aaaaaaaaaafff=',infile_content)
        zipper.writestr(filename, infile_content)

    s3.put_object(Bucket=settings.AWS_STORAGE_BUCKET_NAME, Key='zipfiles/'+filename, Body=zip_buffer.getvalue())
    # get category tag
    categories = get_category(request)
    for category in categories:
        if context["data"].category_id == category.id:
            context["category"] = category
            # get related products
            related_design = list(Web.objects.filter(category_id=category.id))

    context["related_designs"] = related_design[::-1]
    context['feature_products'] = get_feature_products(request)
    context['categories'] = get_category(request)
    context['subcategories'] = get_subcategory(request)
    context['allimg'] = allimg
#     context['allfile'] = resp
    context['filename'] = filename

    return render(request, "T-singal-products.html",  context)

def newdef(request, slug):

    products = None
    subcategories = []
    subsubcategories = []

    if slug:
        alll = Web.get_all_products_by_categoryid(slug)
    else:
        alll = Web.objects.all()

    filtered_qs = ProductFilter(request.GET, queryset=alll)
    filtered_qs_form = filtered_qs.form
    filtered_qs = filtered_qs.qs

    # for new product on top
    filtered_qs = list(filtered_qs)
    filtered_qs = filtered_qs[::-1]

    products = Paginator(filtered_qs, 3)

    page = request.GET.get('page')

    try:
        aa = products.page(page)
    except PageNotAnInteger:
        aa = products.page(1)
    except EmptyPage:
        aa = products.page(products.num_pages)

    data = {}
    # data['products'] = aa
    data['categories'] = get_category(request)
    data['subcategories'] = get_subcategory(request)

    data['filter'] = aa
    data['filtered_qs_form'] = filtered_qs_form
    # print('you are : ', request.session.get('email'))
    return render(request, 'T-products.html', data)


def products(request):
    products = None
    data = {}

    filtered_qs = ProductFilter(request.GET, queryset=Web.objects.all())
    filtered_qs_form = filtered_qs.form
    filtered_qs = filtered_qs.qs

    # for new product on top
    filtered_qs = list(filtered_qs)
    filtered_qs = filtered_qs[::-1]
    # categoryID = request.GET.get("category")

    # if categoryID:
    #     products = Paginator(filtered_qs, 2)
    # else:
    products = Paginator(filtered_qs, 3)

    page = request.GET.get('page')

    try:
        aa = products.page(page)
    except PageNotAnInteger:
        aa = products.page(1)
    except EmptyPage:
        aa = products.page(products.num_pages)

    # data = {}
    allproducts = Web.objects.all()
    data['allproducts'] = allproducts
    # data['products'] = aa
    data['categories'] = get_category(request)
    data['subcategories'] = get_subcategory(request)
    data['filtered_qs_form'] = filtered_qs_form
    # print('you are : ', request.session.get('email'))

    data['filter'] = aa
    data['filtered_qs'] = filtered_qs

    return render(request, 'T-products.html', data)


def login(request):

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        try:
            user = auth.authenticate(username=User.objects.get(email=username), password=password)  
        except:
            pass
#             user = auth.authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                auth.login(request, user)

                # return HttpResponseRedirect(a)
                # return HttpResponseRedirect(request.path_info)
                # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                messages.success(request, "Login Successfull")
                return redirect('home')
            else:
                messages.error(
                    request, "Account is not active,Please check your email")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            messages.error(request, 'Invalid Credential')
            # return redirect('home')
            return render(request, 'T-login.html')
    else:
        data = {}
        data['categories'] = get_category(request)
        data['subcategories'] = get_subcategory(request)
        return render(request, 'T-login.html', data)


@ csrf_exempt
def register(request):
    if request.method == 'POST':
        # first_name = request.POST['first_name']
        # last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username taken')
                # return redirect('home')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'email taken')
                # return redirect('home')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                user = User.objects.create_user(
                    username=username, password=password1, email=email)
                # username=username, password=password1, email=email, first_name=first_name, last_name=last_name)
                user.is_active = True
                # SMOAK SMOAK SMOAK SMOAK SMOAK FALSE
                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }

                link = reverse('activate', kwargs={
                    'uidb64': email_body['uid'], 'token': email_body['token']})

                email_subject = 'Activate your account'

                activate_url = 'http://'+current_site.domain+link

                email = EmailMessage(
                    email_subject,
                    'Hi '+user.username + ', Please the link below to activate your account \n'+activate_url,
                    'tripplerun.official@gmail.com',
                    [email],
                )
                # email.send(fail_silently=False)
                EmailThread(email).start()

                user.save()
                messages.success(
                    request, 'Please check Your Email to Verify Your Email Id')
                return redirect('login')

        else:
            messages.error(request, 'Password not matching')
            # return redirect('home')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        return redirect('/')
    else:
        data = {}
        data['categories'] = get_category(request)
        data['subcategories'] = get_subcategory(request)
        return render(request, 'T-register.html', data)


def activate(request, uidb64, token):
    try:
        id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=id)

        if not account_activation_token.check_token(user, token):
            return redirect('login'+'?message='+'User activated')
            # return redirect('login'+'?message='+'User already activated')
            # SMOAK SMOAK SMOAK SMOAK 

        if user.is_active:
            return redirect('login')
        user.is_active = True
        user.save()

        messages.success(request, 'Account activated successfully')
        return redirect('login')

    except Exception as ex:
        pass

    return redirect('login')
# from validate_email import validate_email


def forgot(request):
    if request.method == 'POST':
        email = request.POST['email']

        context = {
            'values': request.POST
        }

        # if not validate_email(email):
        current_site = get_current_site(request)
        user = User.objects.filter(email=email)

        if user.exists():

            email_contents = {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0]),
            }

            link = reverse('setnewpassword', kwargs={
                'uidb64': email_contents['uid'], 'token': email_contents['token']})

            email_subject = 'Pasword Reset Instructions'

            reset_url = 'http://'+current_site.domain+link

            email = EmailMessage(
                email_subject,
                'Hi there, Please click the link below to reset your account password \n'+reset_url,
                'tripplerun.official@gmail.com',
                [email],
            )
            # email.send(fail_silently=False)
            EmailThread(email).start()

        messages.success(
            request, 'We have successfully sent password reset link to your email.')

        return render(request, 'T-forgot.html')
    return render(request, 'T-forgot.html')


def setnewpassword(request, uidb64, token):
    context = {
        'uidb64': uidb64,
        'token': token
    }

    try:
        user_id = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=user_id)

        if not PasswordResetTokenGenerator().check_token(user, token):
            messages.success(
                request, 'Password Reset link expire, Please request a new link.')
            return render(request, 'T-forgot.html')
    except Exception as identifier:
        pass

    if request.method == 'POST':
        context = {
            'uidb64': uidb64,
            'token': token
        }
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if password1 != password2:
            messages.error(request, 'Password not matching')
            return render(request, 'T-setpassword.html', context)

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password1)
            user.save()
            messages.success(
                request, 'Password Reset successfully, Please login with your new password')
            return render(request, 'T-login.html')
        except Exception as identifier:
            messages.info(
                request, 'Something Went Wrong, Please try again')
            return render(request, 'T-setpassword.html', context)

    return render(request, 'T-setpassword.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def search(request):
    if request.method == 'GET':  # this will be GET now
        # do some research what it does
        data = {}
        searchquery = request.GET.get('q', '')

        if searchquery:
            alll = Web.objects.filter(
                Q(name__icontains=searchquery) | Q(design_code__icontains=searchquery) | Q(area__icontains=searchquery))

        else:
            products = Web.objects.all()

        filtered_qs = ProductFilter(request.GET, queryset=alll)
        filtered_qs_form = filtered_qs.form
        filtered_qs = filtered_qs.qs

        # for new product on top
        filtered_qs = list(filtered_qs)
        filtered_qs = filtered_qs[::-1]

        products = Paginator(filtered_qs, 3)

        page = request.GET.get('page')

        try:
            aa = products.page(page)
        except PageNotAnInteger:
            aa = products.page(1)
        except EmptyPage:
            aa = products.page(products.num_pages)

        search = Search()
        Search.objects.get_or_create(keyword=searchquery)
        Search.objects.filter(keyword=searchquery).update(count=F('count') + 1)

        data['filter'] = aa
        data['filtered_qs_form'] = filtered_qs_form
        data['query'] = searchquery
        data['categories'] = get_category(request)
        data['subcategories'] = get_subcategory(request)
        data['latest_products'] = get_latest_products(request)
        return render(request, 'T-search_result.html', data)

        if len(searchquery) > 100:
            products = Web.objects.none()
            data['products'] = products
            data['latest_products'] = get_latest_products(request)
            return render(request, 'T-search_result.html', data)
    else:
        return render(request, "T-search_result.html", {})


# def product_list(request):

#     films = Web.objects.all()
#     filter = ProductFilter(request.GET, queryset=films)
#     return render(request, 'demo.html', {'filter': filter})


def search1(request, query):
    if request.method == 'GET':  # this will be GET now
        # do some research what it does
        data = {}
        searchquery = query

        if searchquery:
            alll = Web.objects.filter(
                Q(name__icontains=query) | Q(design_code__icontains=query) | Q(area__icontains=searchquery))
        else:
            alll = Web.objects.all()

        filtered_qs = ProductFilter(request.GET, queryset=alll)
        filtered_qs_form = filtered_qs.form
        filtered_qs = filtered_qs.qs

        # for new product on top
        filtered_qs = list(filtered_qs)
        filtered_qs = filtered_qs[::-1]

        products = Paginator(filtered_qs, 3)

        page = request.GET.get('page')

        try:
            aa = products.page(page)
        except PageNotAnInteger:
            aa = products.page(1)
        except EmptyPage:
            aa = products.page(products.num_pages)

        # a = request.META.get('HTTP_REFERER')
        # print(a.request.GET.get('q'))
        # print(type(a))

        # alll = Web.objects.all()
        # filter = ProductFilter(request.GET, queryset=alll)

        data['filter'] = aa
        data['filtered_qs_form'] = filtered_qs_form

        data['query'] = query
        data['categories'] = get_category(request)
        data['subcategories'] = get_subcategory(request)
        data['latest_products'] = get_latest_products(request)
        return render(request, 'T-search_result.html', data)

        if len(searchquery) > 100:
            products = Web.objects.none()
            data['products'] = products
            data['latest_products'] = get_latest_products(request)
            return render(request, 'T-search_result.html', data)
    else:
        return render(request, "T-search_result.html", {})


# @ csrf_exempt
# def wishlist(request, pk):
#     if request.method == 'POST':
#         post = get_object_or_404(Web, id=request.POST.get('wish'))
#         liked = False
#         if post.wishlist.filter(id=request.user.id).exists():
#             post.wishlist.remove(request.user)
#             liked = False
#         else:
#             post.wishlist.add(request.user)
#             liked = True

#         return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# def removewishlist(request, pk):
#     post = get_object_or_404(Web, pk=request.POST.get('removewish'))
#     post.wishlist.remove(request.user)
#     return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# def getwishlist(request):
    # if request.GET.get('wish'):
    #     post = get_object_or_404(Web, id=request.POST.get('wish'))
    #     liked = False
    #     if post.wishlist.filter(id=request.user.id).exists():
    #         post.wishlist.remove(request.user)
    #         liked = False
    #     else:
    #         post.wishlist.add(request.user)
    #         liked = True
    #     return render(request, 'T-wishlist.html')

    # abc2 = []

    # abc = Web.wishlist.through.objects.filter(user_id=request.user.id)
    # for objects in abc:
    #     abc2.append(list(Web.objects.filter(id=objects.web_id)))

    # data = {}
    # data['wishlist'] = abc2

    # return render(request, 'T-wishlist.html', data)
    # return render(request, 'T-wishlist.html')


# @csrf_exempt
# def ggetwishlist(request, pk):
#     if request.GET.get('wish'):
#         post = get_object_or_404(Web, id=request.POST.get('wish'))
#         liked = False
#         if post.wishlist.filter(id=request.user.id).exists():
#             post.wishlist.remove(request.user)
#             liked = False
#         else:
#             post.wishlist.add(request.user)
#             liked = True
#         return render(request, 'T-wishlist.html')

#     abc2 = []

#     abc = Web.wishlist.through.objects.filter(user_id=request.user.id)
#     for objects in abc:
#         abc2.append(list(Web.objects.filter(id=objects.web_id)))

#     data = {}
#     data['wishlist'] = abc2

#     return render(request, 'T-wishlist.html', data)
