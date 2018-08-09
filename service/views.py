from django.shortcuts import render , redirect
from service.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
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
    applications = Application.objects.filter(user=my_user)
    applications = [application.post.id for application in applications]

    context = dict(
        current_user = my_user,
        username = request.user.username,
        complete_post=complete_post,
        applications = applications
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

def lecture(request,id) :
    if not request.user.is_authenticated:
        return redirect('index')
    my_user = request.user.myuser
    post = Post.objects.filter(id=id).last()
    applications = Application.objects.filter(user=my_user)
    applications = [application.post.id for application in applications]


    context = dict(
        post = post,
        my_user = request.user.myuser,
        username=request.user.username,
        post_id = post.id,
        post_image = post.main_image,
        post_title = post.title ,
        post_description = post.description,
        post_lecturedate = post.lecture_date,
        post_min = post.min ,
        post_teacher = post.teacher,
        applications = applications
    )

    return render(request,"lecture.html",context)


@csrf_exempt
def apply(request):
    post_id =request.POST['post_id']
    post = Post.objects.get(id=post_id)
    my_user = request.user.myuser

    data = dict(
        user = my_user,
        post = post
    )
    like = Application.objects.create(**data)
    response = dict(message="OK" , likes_count=post.application_set.count())
    return JsonResponse(response)

@csrf_exempt
def unapply(request):
    post_id =request.POST['post_id']
    post = Post.objects.get(id=post_id)
    my_user = request.user.myuser
    data = dict(
        user = my_user,
        post = post
    )
    like = Application.objects.get(**data)
    like.delete()
    response = dict(message="OK" , likes_count=post.application_set.count())
#    email = EmailMessage('강의 취소 완료', 'body text', to=['yhkim@artience.co.kr'])
    #email.send()
    return JsonResponse(response)

def profile(request,username):
    if not request.user.is_authenticated:
        return redirect('index')
    my_user = request.user.myuser
    applications = Application.objects.filter(user=my_user)
    count = applications.count()
    complete_post = Post.objects.filter(application__user=request.user.myuser)
    complete_post = complete_post.order_by('date')
    applications = [application.post.id for application in applications]
    name = request.user.first_name


    context = dict(
        current_user = my_user,
        username = request.user.username,
        complete_post=complete_post,
        applications = applications,
        name = name,
        count = count
    )

    return render(request,"profile.html",context)

@csrf_exempt
def mail(request):
    post_id =request.POST['post_id']
    type =request.POST['type']
    post = Post.objects.get(id=post_id)
    if (type=="강의 신청") :
        email = EmailMessage('[Campus] Artience 사내 강의 신청 완료', post.title + " 강의가 신청 완료 되었습니다.", to=[request.user.email])
    else :
        email = EmailMessage('[Campus] Artience 사내 강의 취소 완료', post.title + " 강의가 취소 완료 되었습니다.", to=[request.user.email])
    response=dict(message="success")
    email.send()
    return JsonResponse(response)



# Create your views here.
