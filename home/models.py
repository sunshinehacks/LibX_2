from django.db import models
from datetime import datetime,timedelta

class UserProfile(models.Model):
    first_name = models.CharField(max_length=25,)
    last_name = models.CharField(max_length=25)
    username = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=25)
    otp = models.CharField(max_length=25)
    otp2 = models.CharField(max_length=25,default='0000')
    status = models.BooleanField(default=False)
def _str_(self):
        return f'{self.first_name} {self.last_name}'
def username(self):
    return self.username
def email(self):
    return self.email

class Book(models.Model):
    catchoice= [
        ('education', 'Education'),
        ('entertainment', 'Entertainment'),
        ('comics', 'Comics'),
        ('biography', 'Biographie'),
        ('history', 'History'),
        ]
    name=models.CharField(max_length=30,default='bookname')
    isbn=models.PositiveIntegerField(default='0')
    author=models.CharField(max_length=40)
    category=models.CharField(max_length=30,choices=catchoice,default='education')
    pdf_file=models.FileField(upload_to="pdf/",max_length=250,null=True,default=None)
    def _str_(self):
        return str(self.name)+"["+str(self.isbn)+']'


def get_expiry():
    return datetime.today() + timedelta(days=15)

class IssuedBook1(models.Model):
    #moved this in forms.py
    #enrollment=[(student.enrollment,str(student.get_name)+' ['+str(student.enrollment)+']') for student in StudentExtra.objects.all()]
    username=models.CharField(max_length=30)
    #isbn=[(str(book.isbn),book.name+' ['+str(book.isbn)+']') for book in Book.objects.all()]
    isbn=models.CharField(max_length=30)
    issuedate=models.DateField(auto_now=True)
    expirydate=models.DateField(default=get_expiry)
    
    def _str_(self):
        return self.username


class BookRequest(models.Model):
    book_name = models.CharField(max_length=255)
    user_name = models.CharField(max_length=255)

    
class Task(models.Model):
    tasktitle = models.CharField(max_length = 200)
    taskdescription = models.TextField()
    def _str_(self):
        return self.tasktitle   
