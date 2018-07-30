from ago import human
import pytz
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):
    user_django=models.OneToOneField(User,on_delete=models.CASCADE)
    photo = models.CharField(null=True , max_length=200)
    description = models.CharField(null=True,max_length=200)
# Create your models here.

class Post(models.Model):
    title = models.CharField(null=True,max_length=200)
    description = models.CharField(null=True,max_length=200)
    date = models.DateTimeField(default=datetime.now())
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    photo= models.CharField(max_length=200)
