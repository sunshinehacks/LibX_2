from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from LibX_2 import settings
import random
from home.models import UserProfile
from django.contrib.auth.hashers import make_password


# Create your views here.

def home(request):
    return render(request, 'home\home.html')

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
    return render(request,'home\login.html')      
        
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
                return render(request, "home\login.html")
        except User.DoesNotExist:
            messages.info(request, "Username not found")
            return render(request, "home\login.html")

    return render(request, "home\login.html")
    

def afterlogin(request):
        return render(request, 'home\loginafter.html') 

def logout(request):
    return render(request, 'home\logout.html')

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
