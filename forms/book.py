from django import forms
from home.models import Book
from home.models import UserProfile
from django.contrib.auth.models import User
from home.models import BookRequest

class BookRequestForm(forms.ModelForm):
    book_name = forms.ModelChoiceField(queryset=Book.objects.all(), empty_label="Name and isbn",to_field_name="isbn",label='Name and Isbn')
    class Meta:
        model = BookRequest
        fields = ['book_name', 'user_name']

#create a form
class BookForm(forms.ModelForm):
    class Meta:
        model=Book
        fields=['name','isbn','author','category','pdf_file']


class IssuedBookForm(forms.Form):
    #to_field_name value will be stored when form is submitted.....__str__ method of book model will be shown there in html
    isbn2=forms.ModelChoiceField(queryset=Book.objects.all(),empty_label="Name and isbn", to_field_name="isbn",label='Name and Isbn')
    username2=forms.ModelChoiceField(queryset=User.objects.all(),empty_label="Username",to_field_name='username',label='username')
