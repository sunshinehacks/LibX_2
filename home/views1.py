from django.conf import settings as st
from django.shortcuts import redirect, render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import HttpResponseRedirect,HttpResponse,FileResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required,user_passes_test
from django.core.mail import send_mail
from LibX_2 import settings 
from .models import Book
# from .models import User
from .models import IssuedBook1
from .models import BookRequest
from .models import Task as TaskModel
from forms.task import TaskForm 
from forms.book import BookForm 
from forms.book import IssuedBookForm 
import random
from home.models import UserProfile
from datetime import datetime,timedelta,date
from forms.book import BookRequestForm
import pandas as pd
from django.contrib.auth.hashers import make_password
import csv
import os

# Create your views here.
def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()

def home(request):
    return render(request, 'home.html')

#---------------------------------------REGISTRATION VIEW--------------------------------------------------#
user=""
def register(request):
    
    # WE WILL GET THE USER DETAILS HERE FROM THE FORM
    if request.method == "POST":
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST.get('pass1')
        pass2= request.POST.get('pass2')
        request.session["username"] = username
        request.session["password"] = pass1
        request.session["email"] = email
        request.session["fname"] = fname
    # FEW VALIDATIONS I SHOULD DO BEFORE REGISTERING
        if pass1 == pass2:
            if User.objects.filter(username=username).exists():
                messages.info(request, "USER ALREADY EXIST")
                return redirect('home:register')
                 
            elif User.objects.filter(email=email).exists():
                messages.info(request, "EMAIL ALREADY EXIST")
                return redirect('home:register')
        
            elif len(username)>15:
                messages.info(request, "Username Too Long")
            
            else:
                messages.info(request, "CHECK YOUR EMAIL AND ENTER OTP")
                # FINALLY HERE WE TAKE ALL THE DETAILS AND CREATE THE USER
                user = User.objects.create_user(username,email,pass1)
                user.first_name = fname
                user.last_name = lname
                user.is_active = False
                user.save()
                send_otp(request) # SENDS OTP TO CONFIRM THE USER
                send_email(fname, email) # SENDS THE WELCOME EMAIL
                user_profile = UserProfile.objects.create(
                    first_name=fname,
                    last_name=lname,
                    username=username,
                    email=email,
                    password=pass1,
                    otp=request.session["otp"], # you need to generate and set the OTP value here
                )
                user_profile.save()
                return render(request,'email_confirmation.html',{"email":email,"fname":fname})
        else:
            messages.info(request, "PASSWORD DONT MATCH")
            return redirect('home:register')
    return render(request,'login.html')      
        
def send_successful_registration_email(fname, email):
    #Successful Registration Email.
    subject = "Successful Registration at LIBX"
    message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #6A0DAD;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" style="max-width: 600px; margin-top: 50px; border: 3px solid white; background-color: white; border-radius: 10px;">
                    <tr>
                        <td style="padding: 40px 30px 40px 30px; text-align: center;">
                            <h2 style="color: #6A0DAD; font-size: 24px; margin-bottom: 30px;">Successful Registration at LIBX</h2>
                            <p style="color: #6A0DAD; font-size: 18px;">Hello {fname}!</p>
                            <p style="color: #6A0DAD; font-size: 16px;">Congratulations! You have successfully registered at LIBX.</p>
                            <p style="color: #6A0DAD; font-size: 16px;">An exciting journey awaits you. Get started now!</p>
                            <p style="color: #6A0DAD; font-size: 16px;">Thank you for choosing LIBX.</p>
                        </td>
                    </tr>
                </table>
            </body>
        </html>
    """
    from_email = settings.EMAIL_HOST_USER
    to_email = email
    send_mail(subject, None, from_email, [to_email], html_message=message, fail_silently=True)




def send_email(fname, email):
    # Welcome Email
    subject = "Welcome To LIBX"
    message = f"""
        <html>
            <body style="font-family: Arial, sans-serif;">
                <div style="max-width: 600px; margin: 20px auto; padding: 20px; background-color: #f9f9f9; border-radius: 10px;">
                    <h2 style="color: #6A0DAD; text-align: center;">Welcome to LIBX</h2>
                    <p style="text-align: center; font-size: 18px;">Hello {fname}!</p>
                    <p style="text-align: center; font-size: 16px;">Welcome to LIBX, your one-stop solution for books and task management.</p>
                    <p style="text-align: center; font-size: 16px;">Thank you for registering. Please confirm your email address. Check your email for further instructions.</p>
                </div>
            </body>
        </html>
    """
    from_email = settings.EMAIL_HOST_USER
    to_email = email
    send_mail(subject, None, from_email, [to_email], html_message=message, fail_silently=True)

def send_otp(request):
    s=""
    for x in range(0,6):
        s+=str(random.randint(0,9))
    request.session["otp"]=s
    html_message = f"""
    <html>
        <body style="margin: 0; padding: 0; background-color: #6A0DAD;">
            <table align="center" border="0" cellpadding="0" cellspacing="0" style="max-width:600px; margin-top:50px; border: 3px solid white; background-color: white; border-radius: 10px;">
                <tr>
                    <td style="padding: 40px 30px 40px 30px; text-align: center;">
                        <h2 style="color: #6A0DAD; font-size: 24px; margin-bottom: 30px;">OTP for Registration</h2>
                        <p style="color: #6A0DAD; font-size: 18px;">Your OTP is: <span style="color: #6A0DAD; font-weight: bold;">{s}</span></p>
                        <p style="color: #6A0DAD; font-size: 14px;">This OTP is valid for a limited time.</p>
                    </td>
                </tr>
            </table>
        </body>
    </html>
    """
    send_mail(
        "OTP FOR REGISTER",
        s,
        'canvais1216@gmail.com',  # Replace with your actual email
        [request.session['email']],
        fail_silently=False,
        html_message=html_message
    )
    messages.info(request, "OTP SENT")
    return render(request, "email_confirmation.html")

def otp_verify(request):
    #OLD VIEW
    if request.method == 'POST': 
        otp_ = request.POST.get("otp")
    if otp_ == request.session["otp"]:
        # encryptedpassword=make_password (request.session['password']) 
        user = User.objects.get(email=request.session['email'])
        user.is_active = True
        user.save()
        send_successful_registration_email(fname=request.session['fname'], email=request.session['email'])
        messages.info(request, 'signed in successfully...')
        return redirect('home:afterlogin')
    else:
        messages.error (request, "otp doesn't match") 
        return render(request, 'email_confirmation.html')


def auth(request):
    if request.method == "POST":
        username = request.POST.get('username')
        pass1 = request.POST.get('pass1')
        try:
            user1 = User.objects.get(username=username)
            user = authenticate(username=username, password=pass1)
            if user is not None:
                login(request, user)
                fname = user.first_name
                return redirect('home:afterlogin')  # Replace 'home:afterlogin' with your desired redirect path
            else:
                messages.info(request, "Wrong PASSWORD")
                return render(request, "login.html")
        except User.DoesNotExist:
            messages.info(request, "Username not found")
            return render(request, "login.html")

    return render(request, "login.html")
    
@login_required
def afterlogin(request):
        if not request.session.get('message_shown', False):
            messages.info(request, "Login Successful")
            request.session['message_shown'] = True
        return render(request, 'home/loginafter.html')

@login_required
def userafterlogin(request):
        return render(request, 'home/userafterlogin.html') 

@login_required
def feedback(request):
        return render(request, 'feedback.html')

@login_required
def contactus(request):
        return render(request, 'contactus.html')

def logout(request):
    if request.user.is_authenticated:
        settings.AUTO_LOGOUT(request)
        return render(request, 'logout.html')
    else:
        messages.info(request, "LOGIN FIRST")
        return render(request, 'home.html')

def forgotpass(request):
    send_otp_fp(request)
    return render(request, 'forgotpass.html')

def send_otp_fp(request):
    error_message = None
    otp=""
    for x in range(0,6):
        otp+=str(random.randint(0,9))
    request.session["otp"]=otp
    email = request.POST.get('email')
    user_email = UserProfile.objects.filter(email=email)
    if user_email:
        user = UserProfile.objects.get(email=email)
        user.otp2 = otp
        user.save()
        request.session['email'] = request.POST['email']
        
        html_message = f"""
    <html>
        <body style="margin: 0; padding: 0; background-color: #6A0DAD;">
            <table align="center" border="0" cellpadding="0" cellspacing="0" style="max-width:600px; margin-top:50px; border: 3px solid white; background-color: white; border-radius: 10px;">
                <tr>
                    <td style="padding: 40px 30px 40px 30px; text-align: center;">
                        <h2 style="color: #6A0DAD; font-size: 24px; margin-bottom: 30px;">OTP for Password Reset</h2>
                        <p style="color: #6A0DAD; font-size: 18px;">Your OTP is: <span style="color: #6A0DAD; font-weight: bold;">{otp}</span></p>
                        <p style="color: #6A0DAD; font-size: 14px;">This OTP is valid for a limited time.</p>
                    </td>
                </tr>
            </table>
        </body>
    </html>
    """
        send_mail(
            "Password Reset OTP",
            otp,
            'canvais1216@gmail.com',  # Replace with your actual email
            [request.session['email']],
            fail_silently=False,
            html_message=html_message
        )
        messages.success(request,'OTP SENT TO EMAIL')
        return redirect('home:enter_otp_fp')
    else:
        error_message = "INVALID EMAIL PLEASE ENTER CORRECT EMAIL"
        return render(request,'forgotpass.html')

def enter_otp_fp(request):
    error_message = None
    if request.session.has_key('email'):
        email =request.session['email']
        user = UserProfile.objects.filter(email=email)
        for u in user:
            user_otp = u.otp2
        if request.method == "POST":
            otp = request.POST.get('otp')
            if not otp:
                error_message = 'OTP IS REQUIRED'
                return render(request,'forgot_pass_otp.html')
            elif not user_otp == otp:
                error_message = 'OTP IS WRONG'
                print("<script>alert('WRONG OTP');</script>")
                return render(request,'forgot_pass_otp.html')
            if not error_message:
                 return redirect('home:pass_reset')
                # return render(request,'passwordreset.html')
        else:
            return render(request,'forgot_pass_otp.html')
    else:
        return render(request,'forgotpass.html')

def pass_reset(request):
    error_message = None
    if 'email' in request.session:
        email = request.session['email']
        try:
            user = UserProfile.objects.get(email=email)
            user_django = User.objects.get(email=email)
            username =  user.username
            if request.method == "POST":
                new_pass = request.POST.get('new_password')
                new_pass2 = request.POST.get('reenter_password')
                if not new_pass:
                    error_message = 'Please enter a new password'
                elif not new_pass2:
                    error_message = 'Please re-enter the password'
                elif new_pass == user.password:
                    error_message = 'This password already exists'
                elif new_pass != new_pass2:
                    error_message = 'Passwords do not match'

                if not error_message:
                    user.password = new_pass
                    user.save()

                    # Updating password for Django User model
                    user_django.set_password(new_pass)
                    user_django.save()
                    send_successful_passreset_email(username,email=request.session['email'])
                    messages.success(request, 'Password changed successfully')
                    return redirect('home:auth')  # Assuming there's a route named 'home:auth'

            # Handle other cases or errors appropriately
            return render(request, 'passwordreset.html')

        except UserProfile.DoesNotExist:
            messages.error(request, 'User does not exist')
            return render(request, 'passwordreset.html')

    return render(request, 'passwordreset.html')

def send_successful_passreset_email(username,email):
    #Successful Registration Email.
    subject = "Successful Password Reset at LIBX"
    message = f"""
        <html>
            <body style="font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #6A0DAD;">
                <table align="center" border="0" cellpadding="0" cellspacing="0" style="max-width: 600px; margin-top: 50px; border: 3px solid white; background-color: white; border-radius: 10px;">
                    <tr>
                        <td style="padding: 40px 30px 40px 30px; text-align: center;">
                            <h2 style="color: #6A0DAD; font-size: 24px; margin-bottom: 30px;">Successful Password Reset at LIBX</h2>
                            <p style="color: #6A0DAD; font-size: 18px;">Hello {username}!</p>
                            <p style="color: #6A0DAD; font-size: 16px;">Congratulations! You have successfully changed your Password at LIBX.</p>
                            <p style="color: #6A0DAD; font-size: 16px;">Dont stop your work. Re-start your journey now!</p>
                            <p style="color: #6A0DAD; font-size: 16px;">Thank you for choosing LIBX.</p>
                        </td>
                    </tr>
                </table>
            </body>
        </html>
    """
    from_email = settings.EMAIL_HOST_USER
    to_email = email
    send_mail(subject, None, from_email, [to_email], html_message=message, fail_silently=True)

#Edit Profile In Django
@login_required
def edit_profile(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user_profile = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            return redirect('home:auth')  # Handle the case where the user is not found

        # Use the entered email to fetch the corresponding UserProfile
        if 'first_name' in request.POST:
            user_profile.first_name = request.POST['first_name'] or user_profile.first_name

        if 'last_name' in request.POST:
            user_profile.last_name = request.POST['last_name'] or user_profile.last_name

        if 'password' in request.POST:
            user_profile.password = request.POST['password'] or user_profile.password

        user_profile.save()
        return redirect('home:auth')  # Change 'profile' to the name of your profile view
    return render(request, 'edit_profile.html')


def viewbook_view(request):
    books=Book.objects.all()
    return render(request,'library1/viewbook.html',{'books':books})

def viewbookuser_view(request):
    books=Book.objects.all()
    return render(request,'library1/viewbookuser.html',{'books':books})

def addbook_view(request):
    if request.method == 'POST':
        nm = request.POST['name']
        author = request.POST['author']
        isbn = request.POST['isbn']
        category = request.POST['category']
        pdf_file = request.FILES['pdf_file']

        if pdf_file.name.endswith(".pdf"):
            filename = pdf_file.name
            upload_folder = os.path.join(st.MEDIA_ROOT , "books_pdfs")
            os.makedirs(upload_folder , exist_ok=True)
            filepath = os.path.join(upload_folder , filename)
            with open(filepath , "wb+") as destination:
                for chunk in pdf_file.chunks():
                    destination.write(chunk)
        else:
            messages.error(request , "Error in uploading")
            return HttpResponse("Error in uploading the file")

        try:
            book = Book.objects.create(
                name = nm,
                author = author,
                isbn = isbn,
                category = category,
                pdf_file = filepath,
            )
            if book:
                print("Saved !!")
            else :
                return HttpResponse("not saved !!")
            return redirect('home:viewbook_view')       
        except Exception as e:
            print(e)
            return HttpResponse("errror aaya >>>" , e)
    return render(request, "library1/addbook.html")

def updatebook_view(request):
    if request.method == 'POST':
        nm = request.POST['name']
        author = request.POST['author']
        isbn = request.POST['isbn']
        category = request.POST['category']
        pdf_file = request.FILES['pdf_file']

        if pdf_file.name.endswith(".pdf"):
            filename = pdf_file.name
            upload_folder = os.path.join(st.MEDIA_ROOT , "books_pdfs")
            os.makedirs(upload_folder , exist_ok=True)
            filepath = os.path.join(upload_folder , filename)
            with open(filepath , "wb+") as destination:
                for chunk in pdf_file.chunks():
                    destination.write(chunk)
        else:
            messages.error(request , "Error in uploading")
            return HttpResponse("Error in uploading the file")

        try:
            book = Book.objects.update(
                name = nm,
                author = author,
                isbn = isbn,
                category = category,
                pdf_file = filepath,
            )
            if book:
                print("Saved !!")
            else :
                return HttpResponse("not saved !!")
            return redirect('home:viewbook_view')       
        except Exception as e:
            print(e)
            return HttpResponse("errror aaya >>>" , e)
        
        
    else:
        return HttpResponse("Invalid request method")   

def issuebook_view(request):
    form=IssuedBookForm()
    if request.method=='POST':
        #now this form have data from html
        form=IssuedBookForm(request.POST)
        if form.is_valid():
            obj=IssuedBook1()
            obj.username=request.POST.get('username2')
            obj.isbn=request.POST.get('isbn2')
            
            obj.save()
            return render(request,'library1/bookissued.html')
    return render(request,'library1/issuebook.html',{'form':form})


def viewissuedbook_view(request):
    issuedbooks=IssuedBook1.objects.all()
    
    li=[]
    
    for ib in issuedbooks:
        issdate=str(ib.issuedate.day)+'-'+str(ib.issuedate.month)+'-'+str(ib.issuedate.year)
        expdate=str(ib.expirydate.day)+'-'+str(ib.expirydate.month)+'-'+str(ib.expirydate.year)
        #fine calculation
        days=(date.today()-ib.issuedate)
        print(date.today())
        d=days.days
        fine=0
        if d>15:
            day=d-15
            fine=day*10


        books=list(Book.objects.filter(isbn=ib.isbn))
        users=list(IssuedBook1.objects.filter(username=ib.username))
        
               
        i=0
        for l in books:
            t=(users[i].username,books[i].name,books[i].author,issdate,expdate,fine,books[i].pdf_file)
            
            i=i+1
            li.append(t)

    return render(request,'library1/viewissuedbook.html',{'li':li})

def viewissuedbookbyuser(request):
    user = User.objects.filter(id=request.user.id)
    issuedbook = IssuedBook1.objects.filter(username=user[0].username)

    li1 = []
    li2 = []

    for ib in issuedbook:
        books = Book.objects.filter(isbn=ib.isbn)
        for book in books:
            t = (request.user, user[0].email, book.name, book.author, book.pdf_file)
            li1.append(t)

        issdate = f"{ib.issuedate.day}-{ib.issuedate.month}-{ib.issuedate.year}"
        expdate = f"{ib.expirydate.day}-{ib.expirydate.month}-{ib.expirydate.year}"

        # Fine calculation
        days = (date.today() - ib.issuedate)
        print("Today's date:", date.today())
        d = days.days
        fine = 0

        if d > 15:
            day = d - 15
            fine = day * 10

        t = (issdate, expdate, fine)
        li2.append(t)

    print("li1:", li1)
    print("li2:", li2)

    return render(request, 'library1/viewissuedbookbyuser.html', {'li1': li1, 'li2': li2})

def viewuser_view(request):
    users=UserProfile.objects.all()
    return render(request,'library1/viewuser.html',{'users':users})

def requestbook(request):
    requested_books = BookRequest.objects.all()
    return render(request, 'home/req.html', {'requested_books': requested_books})
      
def delete_requests_view(request):
    if request.method == 'POST':
        request_id = request.POST.get('delete_request')
        if request_id:
            try:
                book_request = BookRequest.objects.get(pk=request_id)
                book_request.delete()
            except BookRequest.DoesNotExist:
                pass  # Handle the case where the request doesn't exist

    return redirect('home:requestbook')

def book_request_view(request):
    if request.method == 'POST':
        form = BookRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home:book_request_view')  # Redirect to the admin page for requested books
    else:
        form = BookRequestForm()

    return render(request, 'home/book_request_form.html',{'form':form})

def bulk_Upload_book(request):
    return render(request,"library1/bulkupload.html")

def upload_csv_book(request):
    if request.method=='POST':
        file = request.FILES['csv_file']
        if file.name.endswith('.csv') and file is not None:
            df = pd.read_csv(file)
            for _,row in df.iterrows():
                name = row['name']
                isbn = row['isbn']
                author = row['author']
                category = row['category']
                pdf_file = row['pdf_file']
                Book.objects.create(name=name,isbn=isbn,author=author,category=category,pdf_file=pdf_file)
            #print("uploaded succesfully")
            messages.success(request,"Data uploaded successfully!")
            return redirect("home:viewbook_view")
        else:
            messages.error(request,"cant upload file")
            return redirect("home:viewbook_view")
        
def viewTask(request):
    # dictionary for initial data with fields names as keys
    context ={}
    #add the dictionary during initialization
    context["tasks"] = TaskModel.objects.all()
    return render(request, "task/viewtask.html", context)

def addTask(request):
    # dictionary for initial data with fields names as keys
    context ={}
    
    #add the dictionary during initialization
    form = TaskForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.add_message(request, messages.INFO, 'successfully created form')
        return redirect("home:viewTask")
    context['form']= form
    return render(request, "task/addtask.html",context)


def updateTask(request, id):
    # dictionary for initial data with fields names as keys
    context ={}
    
    #fetch the object related to passed id
    obj = get_object_or_404(TaskModel,id = id)

    #pass the object as instance in form
    form = TaskForm(request.POST or None, instance = obj)
    
    #save the data from the form and redirect to detail_view
    if form.is_valid():
        form.save()
        return redirect("home:viewTask")
    #add from dictionary to context
    context['form']= form
    return render(request, "task/edittask.html", context)


def deleteTask(request,id):
    # dictionary for initial data with fields names as keys
    context ={}
    
    #fetch the object related to passed id
    obj = get_object_or_404(TaskModel,id = id)
    if request.method =="GET":
        #delete object
        obj.delete()
        return redirect("home:viewTask")
    return render(request,  "task/viewtask.html", context)

def bulk_upload_task(request):
    return render(request,"task/bulkUpload.html")

def upload_csv(request):
    
    if("GET" == request.method):
        return HttpResponse("Not valid method")
    csv_file=request.FILES["csv_file"]
    
    if not csv_file.name.endswith('.csv'):
        return HttpResponse("File not valid")
    
    if csv_file.multiple_chunks():
        return HttpResponse("Uploaded file is big")

    file_data = csv_file.read().decode("utf-8")
    lines = file_data.split("\n")
    c=len(lines)
    #return HttpResponse(lines[0])
    for i in range(0,c-1):
        fields = lines[i].split(",")
        data_dict = {}
        data_dict["tasktitle"] = fields[0]
        data_dict["taskdescription"] = fields[1]

        #return HttpResponse(fields[1])
        cform=TaskForm(data_dict)
        if cform.is_valid():
            cform.save()

    return redirect("home:viewTask")

def download_book_csv(request):
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=book.csv'
    writer = csv.writer(response)
    writer.writerow(['name','isbn','author','category','pdf_file'])
    for book in Book.objects.all():
        writer.writerow([book.name,book.isbn,book.author,book.category,book.pdf_file])
    return response


def download_task_csv(request):
    response = HttpResponse('text/csv')
    response['Content-Disposition'] = 'attachment; filename=task.csv'
    writer = csv.writer(response)
    writer.writerow(['Title','Description'])
    for data in TaskModel.objects.all():
        writer.writerow([data.tasktitle,data.taskdescription])
    return response
