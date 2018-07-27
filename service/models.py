from ago import human
import pytz
from datetime import datetime
from django.db import models
from django.contrib.auth.models import User


class MyUser(models.Model):
    user_django=models.OneToOneField(User,on_delete=models.CASCADE)
# Create your models here.
