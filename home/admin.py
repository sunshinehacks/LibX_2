from django.contrib import admin
from .models import UserProfile
from .models import Book

myModels = [UserProfile, Book]
admin.site.register(myModels)

