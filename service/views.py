from django.shortcuts import render , redirect
from service.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
import re


def index(request):
    if request.user.is_authenticated:
        return redirect('home')
    return render(request,"index.html")

def register(request):
    if request.method == 'POST':
        post_form_data = request.POST
        data = dict(
            username=post_form_data.get('username'),
            email=post_form_data.get('email'),
            first_name=post_form_data.get('name'),
            password=post_form_data.get('password')
        )
        user = User.objects.create_user(**data)
        my_user = MyUser.objects.create(user_django=user)
        return redirect('login')
    return redirect('index')

def login(request):
    return render(request,"login.html")

def home(request):
    if not request.user.is_authenticated:
        return redirect('index')
    my_user = request.user.myuser
    complete_post = Post.objects.all()
    complete_post = complete_post.order_by('date')
    context = dict(
        current_user = my_user,
        username = request.user.username,
        complete_post=complete_post,
    )

    return render(request,"home.html",context)

def search(request):
    return render(request,"home.html")

def upload(request):
    return render(request,"home.html")

def profile(request, username):
    if not request.user.is_authenticated:
        return redirect('index')

def validate_user(request):
    return redirect('home')


def upload_lecture(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == 'GET':
        context = dict(username=request.user.username)
        return render(request, "new_post.html" , context)
    if request.method =='POST':
        username = request.user.username
        my_user = request.user.myuser
        last_lecture = Post.objects.filter(user=my_user).last()
        if last_lecture:
            lecture_id = last_lecture.id + 1
        else :
            lecture_id = 1
        title = request.POST['title']
        teacher = request.POST['teacher']
        min = request.POST['min']
        lecture_date = request.POST['startdate']
        photo = request.FILES['file']
        photo_name = username + '_lecture_' + str(lecture_id)
        fs = FileSystemStorage()
        url_lecture = fs.save(photo_name,photo)
        path_lecture = fs.url(url_lecture)
        fields = request.POST['fields']

        post = Post.objects.create(title = title,user = my_user,teacher = teacher,min = min ,lecture_date=lecture_date,main_image=path_lecture ,description= fields )
        return redirect('home')



# Create your views here.
