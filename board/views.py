from django.shortcuts import render, redirect
from board.forms import PostForm
from django.contrib.auth.models import User

def new_post(request):

    if not request.user.is_authenticated:
        return redirect('index')
    form = PostForm()
    my_user = request.user.myuser
    context = dict(
        current_user = my_user,
        username = request.user.username,
        form = form
    )

    return render(request, 'new_post.html',context)

# Create your views here.
