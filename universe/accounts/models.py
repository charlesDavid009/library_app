from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models import Q

# Create your models here.


class Users(models.Model):
    """
    CREATING A NEW USER
    """
    username = models.CharField(max_length = 200, blank = False, null = True, unique = True)
    email = models.EmailField(blank = False, null = True, unique = True)
    password = models.CharField(max_length= 400,blank = False, null = True)
    confirm = models.CharField(max_length= 100, blank = False, null = True)
    created = models.DateTimeField(auto_now_add=True)

