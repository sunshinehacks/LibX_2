# from django.contrib import admin
# from .models import UserProfile,Book,BookRequest

# class BookAdmin(admin.ModelAdmin):
#     list_display = ('name','isbn','author','category','pdf_file')

# myModels = [UserProfile, Book,BookAdmin,BookRequest]
# admin.site.register(myModels)

from django.contrib import admin
from .models import UserProfile, Book, BookRequest

class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'isbn', 'author', 'category', 'pdf_file')

admin.site.register(UserProfile)
admin.site.register(Book, BookAdmin)
admin.site.register(BookRequest)
