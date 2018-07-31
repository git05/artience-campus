from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns= [
    path('',views.index,name="index"),
    path('register/',views.register,name="register"),
    path('login/',auth_views.LoginView.as_view(template_name='login.html', redirect_authenticated_user=True),name="login"),
    path('home/',views.home,name="home"),
    path('search/',views.search,name="search"),
    path('upload/',views.upload,name="upload"),
    path('profile/<str:username>',views.profile,name="profile"),
    path('logout/',auth_views.LogoutView.as_view(),name="logout"),
    path('loginuser/',views.login,name="validate"),

]
