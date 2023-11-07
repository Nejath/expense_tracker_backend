from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth.models import AbstractUser




class CustomUser(AbstractUser):
    email=models.EmailField(blank=True,null=True,unique=True)
    username = models.CharField(max_length=20,unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


# class Student(models.Model):
#     name=models.CharField(max_length=30)
#     age=models.IntegerField()
#     place=models.CharField(max_length=30)
#
#
#
# @receiver(post_save,sender=Student)
# def student_created(sender,instance,created,**kwargs):
#     if created:
#         m="a student is joined"
#         print(m,sender,instance)

