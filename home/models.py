from django.db import models

class UserProfile(models.Model):
    first_name = models.CharField(max_length=25,)
    last_name = models.CharField(max_length=25)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=25)
    otp = models.CharField(max_length=25)
    otp2 = models.CharField(max_length=25,default='0000')
    status = models.BooleanField(default=False)
    
def __str__(self):
        return f'{self.first_name} {self.last_name}'


