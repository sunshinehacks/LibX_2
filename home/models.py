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

# from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
# from django.db import models

# class UserProfileManager(BaseUserManager):
#     def create_user(self, email, username, password=None, **extra_fields):
#         if not email:
#             raise ValueError('The Email field must be set')
#         email = self.normalize_email(email)
#         user = self.model(email=email, username=username, **extra_fields)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user

#     def create_superuser(self, email, username, password=None, **extra_fields):
#         extra_fields.setdefault('is_staff', True)
#         extra_fields.setdefault('is_superuser', True)

#         if extra_fields.get('is_staff') is not True:
#             raise ValueError('Superuser must have is_staff=True.')
#         if extra_fields.get('is_superuser') is not True:
#             raise ValueError('Superuser must have is_superuser=True.')

#         return self.create_user(email, username, password, **extra_fields)


# class UserProfile(AbstractUser, PermissionsMixin):
#     first_name = models.CharField(max_length=25)
#     last_name = models.CharField(max_length=25)
#     username = models.CharField(max_length=20, unique=True)
#     email = models.EmailField(unique=True)
#     password = models.CharField(max_length=25)
#     otp = models.CharField(max_length=25)
#     otp2 = models.CharField(max_length=25, default='0000')
#     status = models.BooleanField(default=False)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)

#     objects = UserProfileManager()

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = ['username']

#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'
