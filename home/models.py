from django.db import models
from django.utils import timezone

class UserProfile(models.Model):
    first_name = models.CharField(max_length=25,)
    last_name = models.CharField(max_length=25)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=25)
    otp = models.CharField(max_length=25)
    otp2 = models.CharField(max_length=25,default='0000')
    status = models.BooleanField(default=False)
    
class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    publication_date = models.DateField()
    time_added = models.DateTimeField(default=timezone.now)

def __str__(self):
        return f'{self.first_name} {self.last_name}'


