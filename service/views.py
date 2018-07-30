from django.shortcuts import render , redirect
from service.models import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User

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
    complete_post =my_user.post_set.all()
    complete_post = complete_post.order_by('date')

    context = dict(
        current_user = my_user,
        username = request.user.username,
        complete_post=complete_post
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


# Create your views here.
